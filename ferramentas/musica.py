#!/usr/bin/env python3
"""Escolhe e prepara a trilha de um episódio (catálogo público de Kevin MacLeod, incompetech.com, CC BY 4.0).

Uso:
    python3 ferramentas/musica.py --buscar "noir suspense" [--sentimento Mysterious] [--min 90]
    python3 ferramentas/musica.py episodios/002-guerra-dos-mundos "Spy Glass" [--volume -27]

Rode depois do narrar.py (a trilha é cortada na duração do vídeo e abaixa sozinha quando a voz fala) e antes
do montar.py. Saída:  <ep>/assets/musica/trilha.wav  e  <ep>/musica.json  (título, ISRC, crédito obrigatório).
Licença: a descrição precisa do crédito; o pacote_publicacao.py já o coloca nos textos.
"""
import argparse, json, subprocess, sys, urllib.parse
from pathlib import Path

CATALOGO = "https://incompetech.com/music/royalty-free/pieces.json"
MP3 = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/"
LICENCA = "https://creativecommons.org/licenses/by/4.0/"
AGENTE = "Mozilla/5.0"


def baixar(url):
    return subprocess.run(["curl", "-fsSL", "-m", "180", "-A", AGENTE, url], check=True, capture_output=True).stdout


def segundos(duracao):
    h, m, s = (int(x) for x in duracao.split(":"))
    return h * 3600 + m * 60 + s


def buscar(args, catalogo):
    termos = args.buscar.lower().split()
    achados = []
    for f in catalogo:
        texto = " ".join(f.get(k) or "" for k in ("title", "description", "feel", "instruments")).lower()
        pontos = sum(t in texto for t in termos)
        if pontos and segundos(f["length"]) >= args.min and (not args.sentimento or args.sentimento in (f.get("feel") or "")):
            achados.append((pontos, f))
    for _, f in sorted(achados, key=lambda a: -a[0])[:20]:
        print(f"{f['title']} | {f['length']} | {f.get('feel')} | {(f.get('instruments') or '')[:40]} | {(f.get('description') or '')[:90]}")


def preparar(args, catalogo):
    ep = Path(args.episodio).resolve()
    f = next((p for p in catalogo if p["title"].lower() == args.titulo.lower()), None)
    if not f:
        sys.exit(f'✗ "{args.titulo}" não está no catálogo. Use --buscar.')
    tempos = json.loads((ep / "tempos.json").read_text())
    total = tempos["duracao_video"]
    pasta = ep / "assets" / "musica"
    pasta.mkdir(parents=True, exist_ok=True)
    original = pasta / "original.mp3"
    original.write_bytes(baixar(MP3 + urllib.parse.quote(f["filename"])))
    if segundos(f["length"]) < total:
        print(f"⚠ a faixa tem {f['length']} e o vídeo {total:.0f} s: ela vai repetir (a emenda pode aparecer)")
    # a voz comanda o compressor: a música cai enquanto há fala e volta nas pausas
    # o loudnorm solta uma rajada (+17 dB) nos últimos 60 ms ao esvaziar o buffer: normaliza com folga e só depois corta.
    # A saída é quadrática: uma nota forte da faixa nos últimos segundos não desmente o fade.
    filtro = (f"[0:a]atrim=0:{total + 4},asetpts=N/SR/TB,loudnorm=I={args.volume}:TP=-3,aresample=44100,"
              f"atrim=0:{total},asetpts=N/SR/TB,afade=t=in:d=0.8,afade=t=out:st={total - 2.5}:d=2.5:curve=qua[m];"
              f"[1:a]aresample=44100,apad=whole_dur={total}[v];"  # o compressor para na entrada mais curta: a voz tem de durar o vídeo todo
              "[m][v]sidechaincompress=threshold=0.05:ratio=3:attack=40:release=700[s]")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-stream_loop", "-1", "-i", str(original),
                    "-i", str(ep / "assets" / "voz" / "narracao.wav"), "-filter_complex", filtro, "-map", "[s]",
                    "-t", str(total), "-ac", "2", str(pasta / "trilha.wav")], check=True)
    credito = (f"{f['title']} Kevin MacLeod (incompetech.com)\n"
               f"Licensed under Creative Commons: By Attribution 4.0\n{LICENCA}")
    (ep / "musica.json").write_text(json.dumps(
        {"titulo": f["title"], "autor": "Kevin MacLeod", "isrc": f.get("isrc"), "credito": credito},
        ensure_ascii=False, indent=1))
    print(f"✓ trilha: {f['title']} ({total:.1f} s, {args.volume} LUFS antes de abaixar) · rode montar.py e o render")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodio", nargs="?")
    ap.add_argument("titulo", nargs="?")
    ap.add_argument("--buscar")
    ap.add_argument("--sentimento", help="Dark, Mysterious, Suspenseful, Somber, Epic…")
    ap.add_argument("--min", type=int, default=90, help="duração mínima da faixa (s)")
    ap.add_argument("--volume", type=float, default=-20, help="volume da trilha em LUFS (a voz fica em -16)")
    args = ap.parse_args()
    catalogo = json.loads(baixar(CATALOGO))
    if args.buscar:
        buscar(args, catalogo)
    elif args.episodio and args.titulo:
        preparar(args, catalogo)
    else:
        ap.error("informe --buscar ou <episódio> <título>")


if __name__ == "__main__":
    main()
