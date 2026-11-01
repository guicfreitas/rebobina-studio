#!/usr/bin/env python3
"""Mistura os efeitos sonoros de um episódio, cada um no instante da animação que ele acompanha.

Uso:
    python3 ferramentas/sfx.py --listar
    python3 ferramentas/sfx.py episodios/004-guerra-dos-emus

Entrada:  <ep>/sfx.json, escrito pelo animador. Cada efeito acompanha uma palavra da fala ou o início da cena:
    [{"som": "carimbo", "cena": "c05", "palavra": "major", "desloca": -0.05, "volume": 0.4},
     {"som": "swoosh", "cena": "c06", "em": 0.05},
     {"som": "maquina", "cena": "c07", "palavra": "mil", "n": 2, "dur": 0.8}]
    "n" = qual ocorrência da palavra na cena; "dur" corta o som (com fade); "volume" padrão 0.35.
Saída:    <ep>/assets/sfx/efeitos.wav, na duração do vídeo. Rode depois do narrar.py e antes do montar.py.
Sons:     canal/sfx/ (licenças em canal/sfx/fontes.json). O render não usa rede.
"""
import json, re, subprocess, sys, unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SONS = RAIZ / "canal" / "sfx"
VOLUME = 0.35
INTERVALO_MIN = 0.35  # efeitos mais próximos que isso viram ruído


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def arquivo(som):
    achados = sorted(SONS.glob(f"{som}.*"))
    achados = [a for a in achados if a.suffix in (".mp3", ".wav", ".ogg", ".flac")]
    if not achados:
        sys.exit(f'✗ som "{som}" não existe em canal/sfx/. Veja: ferramentas/sfx.py --listar')
    return achados[0]


def instante(cue, tempos):
    cena = next((c for c in tempos["cenas"] if c["id"] == cue["cena"]), None)
    if not cena:
        sys.exit(f'✗ cena {cue["cena"]} não existe em tempos.json')
    if "palavra" not in cue:
        return cena["inicio"] + cue.get("em", 0) + cue.get("desloca", 0)
    alvo, n, k = norm(cue["palavra"]), cue.get("n", 1), 0
    for w in tempos["palavras"]:
        if w["cena"] == cue["cena"] and norm(w["text"]).startswith(alvo):
            k += 1
            if k == n:
                return w["start"] + cue.get("desloca", 0)
    sys.exit(f'✗ palavra "{cue["palavra"]}" (#{n}) não está na fala de {cue["cena"]}')


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--listar":
        fontes = json.loads((SONS / "fontes.json").read_text())
        for som, info in sorted(fontes.items()):
            print(f"{som}: {info.get('descricao', '')}")
        return
    ep = Path(sys.argv[1]).resolve()
    cues = json.loads((ep / "sfx.json").read_text())
    tempos = json.loads((ep / "tempos.json").read_text())
    total = tempos["duracao_video"]
    pos = sorted(((max(instante(c, tempos), 0), c) for c in cues), key=lambda p: p[0])
    for (a, ca), (b, cb) in zip(pos, pos[1:]):
        if b - a < INTERVALO_MIN:
            print(f'⚠ {ca["som"]} e {cb["som"]} a {b - a:.2f} s um do outro (t={a:.2f})')
    entradas, filtros = [], []
    for i, (t, c) in enumerate(pos):
        entradas += ["-i", str(arquivo(c["som"]))]
        corte = ""
        if "dur" in c:
            corte = f"atrim=0:{c['dur']},afade=t=out:st={max(c['dur'] - 0.08, 0)}:d=0.08,"
        filtros.append(f"[{i}:a]aresample=44100,aformat=channel_layouts=stereo,{corte}"
                       f"volume={c.get('volume', VOLUME)},adelay={int(t * 1000)}:all=1[s{i}]")
    mix = "".join(f"[s{i}]" for i in range(len(pos)))
    filtro = ";".join(filtros) + f";{mix}amix=inputs={len(pos)}:normalize=0,alimiter=limit=0.7,apad=whole_dur={total}[f]"
    pasta = ep / "assets" / "sfx"
    pasta.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *entradas, "-filter_complex", filtro,
                    "-map", "[f]", "-t", str(total), str(pasta / "efeitos.wav")], check=True)
    print(f"✓ {len(pos)} efeitos em {pasta / 'efeitos.wav'} · rode montar.py e o render")


if __name__ == "__main__":
    main()
