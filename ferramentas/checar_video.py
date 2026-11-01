#!/usr/bin/env python3
"""Checagem automática antes da revisão de frames: pega o que é mensurável sem gastar uma rodada de revisão.

Uso:  python3 ferramentas/checar_video.py episodios/005-tumba-primeiro-imperador [mp4]

Confere: duração, clipes mais curtos que a cena, efeitos (quantidade, intervalo, ataque), texto ou desenho nas zonas
proibidas e palco parado. Sai com código 1 se houver problema. Não substitui olhar os frames.
"""
import json, re, subprocess, sys
from pathlib import Path

LARG, ALT, FPS = 270, 480, 2      # frames reduzidos a 1/4: o grão some na média
ESCALA = 1920 / ALT
PARADO_MAX = 3.0
LIMIAR_LUZ = 150                  # pixel mais claro que isto é texto ou desenho, não fundo
LIMIAR_MUDANCA = 1.0              # diferença média entre frames que conta como movimento no palco


def checar_cenas(ep, problemas):
    index = (ep / "index.html").read_text()
    for cid, dur in re.findall(r'id="(c\d+)"[^>]*?data-duration="([\d.]+)"', index, re.S):
        html = ep / "compositions" / f"{cid}.html"
        if not html.exists():
            problemas.append(f"{cid}: arquivo da cena não existe")
            continue
        for d in re.findall(r'class="clip"[^>]*?data-duration="([\d.]+)"', html.read_text()):
            if float(d) < float(dur) - 0.01:
                problemas.append(f"{cid}: clipe de {d} s em cena de {dur} s")


def checar_efeitos(ep, duracao, problemas):
    arq = ep / "sfx.json"
    if not arq.exists():
        return
    cues = json.loads(arq.read_text())
    ataques = json.loads((ep.parent.parent / "canal" / "sfx" / "fontes.json").read_text())
    if cues and duracao / len(cues) < 3:
        problemas.append(f"efeitos: {len(cues)} em {duracao:.0f} s, 1 a cada {duracao / len(cues):.1f} s (meta: cerca de 4 s)")
    for c in cues:
        ataque = ataques.get(c["som"], {}).get("ataque")
        if ataque and c.get("desloca", 0) > -ataque + 0.1:
            problemas.append(f'efeito {c["som"]} em {c["cena"]}: ataque de {ataque} s pede desloca perto de {-ataque}')


def checar_frames(video, problemas):
    bruto = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vf", f"fps={FPS},scale={LARG}:{ALT},format=gray",
                            "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    frames = [bruto[i:i + LARG * ALT] for i in range(0, len(bruto), LARG * ALT)]
    zonas = {"rodapé (y>1330)": (0, LARG, int(1330 / ESCALA), ALT), "trilho de botões (x>940, y 700-1080)": (int(940 / ESCALA), LARG, int(700 / ESCALA), int(1080 / ESCALA))}
    for nome, (x0, x1, y0, y1) in zonas.items():
        invadidos = [i / FPS for i, f in enumerate(frames[:-int(3 * FPS)])  # o fim tem a tela azul do STOP
                     if sum(1 for y in range(y0, y1) for p in f[y * LARG + x0:y * LARG + x1] if p > LIMIAR_LUZ) > 6]
        if invadidos:
            # papel e desenho podem passar pelo trilho; só texto é proibido, e isso só se vê olhando o frame
            if nome.startswith("rodapé"):
                problemas.append(f"zona {nome}: invadida em {len(invadidos)} frames, a partir de t={invadidos[0]:.1f} s")
            else:
                print(f"⚠ zona {nome}: há algo claro em {len(invadidos)} frames, a partir de t={invadidos[0]:.1f} s; confira se é texto")
    y0, y1 = int(300 / ESCALA), int(1060 / ESCALA)
    parado, inicio = 0.0, 0.0
    for i in range(1, len(frames) - int(3 * FPS)):
        a, b = frames[i - 1][y0 * LARG:y1 * LARG], frames[i][y0 * LARG:y1 * LARG]
        if sum(abs(p - q) for p, q in zip(a, b)) / len(a) < LIMIAR_MUDANCA:
            parado += 1 / FPS
            if parado == 1 / FPS:
                inicio = i / FPS
        else:
            if parado > PARADO_MAX:
                problemas.append(f"palco parado: {parado:.1f} s a partir de t={inicio:.1f} s")
            parado = 0.0


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ep = Path(sys.argv[1]).resolve()
    video = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else ep / "render" / "rascunho.mp4"
    tempos = json.loads((ep / "tempos.json").read_text())
    duracao = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                                   capture_output=True, text=True, check=True).stdout)
    problemas = []
    if not 65 < duracao <= 120:
        problemas.append(f"duração de {duracao:.1f} s fora de 65-120 s")
    if abs(duracao - tempos["duracao_video"]) > 0.2:
        problemas.append(f"vídeo com {duracao:.1f} s, mas tempos.json diz {tempos['duracao_video']} s: renderize de novo")
    checar_cenas(ep, problemas)
    checar_efeitos(ep, duracao, problemas)
    checar_frames(video, problemas)
    for p in problemas:
        print("✗", p)
    print(f"{'✗' if problemas else '✓'} {len(problemas)} problema(s) em {duracao:.1f} s")
    sys.exit(1 if problemas else 0)


if __name__ == "__main__":
    main()
