#!/usr/bin/env python3
"""Gera a capa de um episódio em HyperFrames, a partir do campo "capa" de roteiro.json.

Uso:  python3 ferramentas/capa.py episodios/005-tumba-primeiro-imperador

    "capa": {"linhas": ["A TUMBA DO 1º IMPERADOR", "FECHADA POR MEDO", "*DAS ARMADILHAS?*"], "simbolo": "simbolos/porta"}

Cada linha ocupa a largura da coluna; *asteriscos* marcam o destaque. O símbolo é assets/<simbolo>.svg do episódio.
Gera capa/ dentro do episódio (não edite à mão, rode de novo) e entrega capa/capa.jpg, que o pacote_publicacao.py usa.
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

ESQ, TOPO, LARGURA, ALTURA = 90, 320, 840, 1000   # coluna do DESIGN; sem legenda, o palco desce até y 1320
TAM_MAX, TAM_MIN = 300, 100
LARGURA_EM = 0.37                                 # largura média do caractere do League Gothic em maiúsculas
TEXTO_ALTURA_MAX = 640


def tamanho(linha):
    return max(TAM_MIN, min(TAM_MAX, int(LARGURA / (len(linha.replace("*", "")) * LARGURA_EM))))


def linha_html(linha, tam):
    corpo = re.sub(r"\*([^*]+)\*", r'<em>\1</em>', linha)
    return f'<div class="linha" style="font-size:{tam}px">{corpo}</div>'


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ep = Path(sys.argv[1]).resolve()
    rot = json.loads((ep / "roteiro.json").read_text())
    capa = rot.get("capa") or sys.exit('✗ roteiro.json sem o campo "capa"')
    simbolo = ep / "assets" / f"{capa['simbolo']}.svg"
    if not simbolo.exists():
        sys.exit(f"✗ símbolo não existe: {simbolo.relative_to(ep)}")

    tamanhos = [tamanho(l) for l in capa["linhas"]]
    excesso = sum(tamanhos) * 0.92 / TEXTO_ALTURA_MAX
    if excesso > 1:
        tamanhos = [int(t / excesso) for t in tamanhos]

    dst = ep / "capa"
    shutil.rmtree(dst, ignore_errors=True)
    (dst / "assets").mkdir(parents=True)
    for pasta in ("fonts", "vendor"):
        shutil.copytree(ep / "assets" / pasta, dst / "assets" / pasta)
    shutil.copy2(ep / "assets" / "rebobina.css", dst / "assets")
    shutil.copy2(ep / "hyperframes.json", dst)

    ano = rot["cenas"][0].get("ano", "")
    linhas = "\n".join(linha_html(l, t) for l, t in zip(capa["linhas"], tamanhos))
    (dst / "index.html").write_text(f'''<!doctype html>
<!-- GERADO por ferramentas/capa.py — não edite à mão. Episódio {rot["id"]} -->
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/rebobina.css" />
    <style>
      :root {{ --acento: {rot.get("acento", "#2FBF71")}; }}
      #root {{ background: var(--fita); overflow: hidden; }}
      #palco {{ position: absolute; left: {ESQ}px; top: {TOPO}px; width: {LARGURA}px; height: {ALTURA}px; display: flex; flex-direction: column; gap: 36px; }}
      .linha {{ font-family: var(--f-titulo); text-transform: uppercase; line-height: .92; color: var(--papel); letter-spacing: .01em; white-space: nowrap; }}
      .linha em {{ font-style: normal; color: var(--vhs); }}
      #simbolo {{ flex: 1; min-height: 0; display: flex; justify-content: center; align-items: center; }}
      #simbolo svg {{ width: 100%; height: 100%; }}
      #osd-play, #osd-ano, #osd-fita {{ position: absolute; font-family: var(--f-mono); font-weight: 700; color: var(--papel);
        text-shadow: 3px 0 rgba(255,59,48,.55), -3px 0 rgba(63,167,255,.55); }}
      #osd-play {{ left: 90px; top: 196px; font-size: 46px; letter-spacing: .06em; }}
      #osd-ano {{ right: 90px; top: 188px; font-size: 64px; letter-spacing: .04em; }}
      #osd-fita {{ right: 92px; top: 262px; font-size: 28px; opacity: .7; letter-spacing: .12em; }}
      #osd-ponto {{ display: inline-block; width: 24px; height: 24px; border-radius: 50%; background: var(--rec); margin-right: 16px; vertical-align: 4px; }}
      #scan {{ position: absolute; inset: 0; opacity: .09; background: repeating-linear-gradient(to bottom, #000 0 2px, transparent 2px 5px); }}
      #vinheta {{ position: absolute; inset: 0; background: radial-gradient(ellipse 75% 60% at 50% 45%, transparent 55%, rgba(0,0,0,.55) 100%); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="1080" data-height="1920">
      <div id="quadro" class="clip" data-start="0" data-duration="1" data-track-index="1">
        <div id="palco">
{linhas}
          <div id="simbolo">{simbolo.read_text()}</div>
        </div>
        <div id="osd-play"><span id="osd-ponto"></span>PLAY ▶</div>
        <div id="osd-ano">{ano}</div>
        <div id="osd-fita">FITA {rot["id"]}</div>
        <div id="scan"></div>
        <div id="vinheta"></div>
      </div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
''')
    subprocess.run(["npx", "--yes", "hyperframes", "snapshot", ".", "--at", "0", "--no-end", "--keep", "--output", "quadro"], cwd=dst, check=True)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", "quadro/at-0s.png", "-q:v", "2", "capa.jpg"], cwd=dst, check=True)
    print(f"✓ capa pronta: {(dst / 'capa.jpg').relative_to(ep.parent.parent)}. Abra e confira se o texto coube e diz do que é o vídeo.")


if __name__ == "__main__":
    main()
