#!/usr/bin/env python3
"""Monta a estrutura HyperFrames de um episódio a partir de roteiro.json + tempos.json.

Uso:
    python3 ferramentas/montar.py episodios/001-acre-cavalo

Gera (sempre sobrescreve — NÃO edite à mão, rode de novo):
    index.html                 raiz: cenas no tempo da narração, OSD, efeitos, legendas, áudio
    compositions/osd.html      ▶ PLAY / ◀◀ REW / ■ STOP + contador de ano (rola entre eras)
    compositions/fx.html       scanlines, grão, vinheta, faixas de "rebobinar", tela azul final
    compositions/legendas.html legendas queimadas palavra a palavra
Cria só se não existir (é aqui que o agente animador trabalha):
    compositions/<id da cena>.html   um rascunho por cena

Dentro de cada cena, use os tempos da narração em vez de segundos fixos:
    RB.t("c03", "Melgarejo")      -> segundo (local da cena) em que a palavra começa
    RB.t("c03", "cavalos", 2)     -> 2ª ocorrência
    RB.tf("c03", "raça")          -> segundo em que a palavra termina
    RB.dur("c03")                 -> duração da cena
Assim, se a narração mudar, basta rodar narrar.py + montar.py e tudo se realinha.
"""
import json, re, shutil, sys, unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TEMPLATE = RAIZ / "templates" / "base-video"
FPS = 30


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def r2(x):
    return round(x + 1e-9, 3)


# Legendas: coluna de texto do DESIGN (x 90–930); os 6 px de cada lado são o contorno de 12 px, que sai da letra.
LG_ESQ, LG_LARGURA = 96, 828
LG_TAM, LG_TAM_MIN = 72, 64     # px. Grupo comprido encurta, não encolhe; só um número inteiro que não cabe vai a 64.
LG_PALAVRAS, LG_CHARS = 3, 29   # limite do grupo (o número inteiro conta como uma palavra)
# largura dos caracteres do Montserrat Black em em, com o letter-spacing de .01em
LG_LARG = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", (
    .816, .783, .747, .836, .683, .654, .779, .814, .36, .584, .775, .627, .964, .814, .858, .753, .858, .755, .667, .664, .794, .796,
    1.216, .772, .72, .697, .702, .428, .618, .624, .722, .629, .671, .655, .688, .671)))
PALAVRAS_NUMERO = set("""dois tres quatro cinco seis sete oito nove dez onze doze treze catorze quatorze quinze dezesseis dezessete
    dezoito dezenove vinte trinta quarenta cinquenta sessenta setenta oitenta noventa cem cento duzentos duzentas trezentos
    trezentas quatrocentos quinhentos seiscentos setecentos oitocentos novecentos mil""".split())
PALAVRAS_FRACAS = set("a o e as os de da do das dos em na no nas nos ao aos à um uma que se por sob".split())


def largura_legenda(txt, tam):
    sem_acento = "".join(c for c in unicodedata.normalize("NFD", txt) if unicodedata.category(c) != "Mn")
    return sum(LG_LARG.get(c, 0.32) for c in sem_acento) * tam


def medir_legenda(palavras, obrigatorio=True):
    """(tamanho em px, índice da palavra que abre a 2ª linha ou None). Nunca passa de 2 linhas nem da coluna.
    Se não couber: encerra, ou devolve None com obrigatorio=False."""
    junta = lambda ps: " ".join(ps)
    for tam in (LG_TAM, LG_TAM_MIN):
        if largura_legenda(junta(palavras), tam) <= LG_LARGURA:
            return tam, None
        cortes = [(max(largura_legenda(junta(palavras[:k]), tam), largura_legenda(junta(palavras[k:]), tam)), k)
                  for k in range(1, len(palavras))]
        if cortes and min(cortes)[0] <= LG_LARGURA:
            return tam, min(cortes)[1]
    if obrigatorio:
        sys.exit(f"✗ legenda não cabe em 2 linhas: {junta(palavras)!r}")
    return None


def agrupar_legendas(palavras):
    """Grupos de até LG_PALAVRAS. Um número por extenso nunca é dividido entre grupos.
    Um "não" sem pontuação nunca fecha grupo: separado do verbo, inverte o sentido da frase sem som."""
    blocos, i = [], 0
    limpa = lambda w: re.sub(r"[.,;:…]+$", "", w["text"]).upper()
    fecha = lambda w: bool(re.search(r"[.,;:!?…]$", w["text"]))
    e_num = lambda w: norm(w["text"]) in PALAVRAS_NUMERO
    while i < len(palavras):
        j = i + 1
        if e_num(palavras[i]):
            while j < len(palavras) and not fecha(palavras[j - 1]) and palavras[j]["cena"] == palavras[i]["cena"]:
                if e_num(palavras[j]):
                    j += 1
                elif norm(palavras[j]["text"]) == "e" and j + 1 < len(palavras) and e_num(palavras[j + 1]):
                    j += 2
                else:
                    break
        blocos.append(palavras[i:j])
        i = j
    fracas = {norm(x) for x in PALAVRAS_FRACAS}
    e_fraca = lambda w: norm(w["text"]) in fracas and not fecha(w)
    e_nao = lambda w: norm(w["text"]) == "nao" and not fecha(w)
    itens_de = lambda bl: [{**w, "txt": limpa(w)} for w in bl if limpa(w)]

    def fecharia(grupo, qtd, bl):
        """Pelos limites e pela palavra fraca, o bloco bl abriria um grupo novo?"""
        chars = sum(len(x["txt"]) + 1 for x in grupo + itens_de(bl)) - 1
        return bool(grupo) and (qtd >= LG_PALAVRAS or chars > LG_CHARS
                                or (len(bl) == 1 and e_fraca(bl[0]) and qtd == LG_PALAVRAS - 1))

    grupos, atual, n = [], [], 0
    for k, bl in enumerate(blocos):
        itens = itens_de(bl)
        if len(bl) == 1 and e_nao(bl[0]) and k + 1 < len(blocos) and fecharia(atual + itens, n + 1, blocos[k + 1]):
            # o "não" ficaria no fim do grupo: ele abre o próximo e leva junto a palavra fraca que o antecede.
            # "que" fica: "SÓ QUE / NÃO ERA", "POR QUE / NÃO O FOGO?" leem melhor que um "SÓ" ou "POR" sozinho.
            antes = [atual.pop()] if atual and e_fraca(atual[-1]) and norm(atual[-1]["text"]) != "que" else []
            if atual:
                grupos.append(atual)
            atual, n = antes, len(antes)
        # palavra fraca não fica pendurada no fim do grupo: ela abre o próximo
        if fecharia(atual, n, bl):
            # exceção: o bloco fica com o "não" que o antecede, se os dois couberem; o número inteiro continua inteiro
            cabe = medir_legenda([x["txt"] for x in atual + itens], obrigatorio=False)
            if not (e_nao(atual[-1]) and n < LG_PALAVRAS and cabe):
                grupos.append(atual); atual, n = [], 0
        atual += itens; n += 1
        if fecha(bl[-1]):
            grupos.append(atual); atual, n = [], 0
    if atual:
        grupos.append(atual)
    return grupos


def main():
    ep = Path(sys.argv[1]).resolve()
    rot = json.loads((ep / "roteiro.json").read_text())
    tem = json.loads((ep / "tempos.json").read_text())
    (ep / "compositions").mkdir(exist_ok=True)
    # assets fixos do template (fontes, gsap, css, símbolos) — nunca apaga o que o episódio já tem
    for src in (TEMPLATE / "assets").rglob("*"):
        if src.is_file():
            dst = ep / "assets" / src.relative_to(TEMPLATE / "assets")
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists() or src.name in ("rebobina.css", "gsap.min.js"):
                shutil.copy2(src, dst)

    total = tem["duracao_video"]
    trilha = ('      <audio id="musica" class="clip" src="assets/musica/trilha.wav" data-start="0"\n'
              '        data-track-index="6" data-volume="1"></audio>\n') if (ep / "assets" / "musica" / "trilha.wav").exists() else ""
    if (ep / "assets" / "sfx" / "efeitos.wav").exists():
        trilha += ('      <audio id="efeitos" class="clip" src="assets/sfx/efeitos.wav" data-start="0"\n'
                   '        data-track-index="7" data-volume="1"></audio>\n')
    cenas = rot["cenas"]
    tc = {c["id"]: c for c in tem["cenas"]}
    # janela de cada cena: começa quando sua fala começa (a 1ª em 0) e vai até a próxima começar
    janelas = []
    for i, c in enumerate(cenas):
        ini = 0.0 if i == 0 else tc[c["id"]]["inicio"] - 0.04
        fim = total if i == len(cenas) - 1 else tc[cenas[i + 1]["id"]]["inicio"] - 0.04
        janelas.append((c["id"], r2(ini), r2(fim - ini)))
    jdict = {cid: (ini, dur) for cid, ini, dur in janelas}

    # palavras por cena, com tempos locais
    pal = {}
    for w in tem["palavras"]:
        ini = jdict[w["cena"]][0]
        pal.setdefault(w["cena"], []).append([norm(w["text"]), r2(w["start"] - ini), r2(w["end"] - ini)])
    rb = {"cenas": {cid: {"inicio": ini, "dur": dur, "fala": [r2(tc[cid]["inicio"] - ini), r2(tc[cid]["fim"] - ini)]}
                    for cid, ini, dur in janelas},
          "palavras": pal, "total": total}

    # eras (contador de ano)
    # "marcos_ano" (opcional na cena): [["palavra", ano], ...] faz o contador acompanhar uma linha do tempo
    # dentro da cena, na palavra indicada, sem as faixas de ruído do "rebobinar".
    eras, marcos, rotulos = [], set(), {}
    for c, (cid, ini, dur) in zip(cenas, janelas):
        ano = c.get("ano")
        if c.get("marcos_ano"):
            for palavra, a in c["marcos_ano"]:
                w = next((p for p in pal[cid] if p[0].startswith(norm(palavra))), None)
                if w is None:
                    sys.exit(f"✗ marcos_ano: {palavra!r} não está na fala de {cid}")
                eras.append((r2(ini + w[1]), a))
                marcos.add(r2(ini + w[1]))
        elif ano is not None and (not eras or eras[-1][1] != ano):
            eras.append((ini, ano))
        if c.get("ano_rotulo"):  # texto do contador no fim da rolagem, ex.: "~100 A.C."
            rotulos[f"{ini:g}"] = c["ano_rotulo"]  # mesma forma que String(t) no JS
    cortes = [ini for _, ini, _ in janelas[1:]]
    # faixas de ruído só em saltos grandes (≥ 10 anos ou para trás); saltos curtos só rolam o contador
    trocas = [t for (t, a), (_, b) in zip(eras[1:], eras[:-1]) if (a < b or a - b >= 10) and t not in marcos]

    acento = rot.get("acento", "#2FBF71")
    hosts = []
    for k, (cid, ini, dur) in enumerate(janelas):
        hosts.append(f'''      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"
        data-start="{ini}" data-duration="{dur}" data-track-index="1" data-track-kind="graphics"
        data-width="1080" data-height="1920" style="z-index:1"></div>''')

    index = f'''<!doctype html>
<!-- GERADO por ferramentas/montar.py — não edite à mão. Episódio {rot["id"]}: {rot["tema"]} -->
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="assets/rebobina.css" />
    <style>:root {{ --acento: {acento}; }}</style>
    <script>
      window.RB = {json.dumps(rb, ensure_ascii=False, separators=(",", ":"))};
      RB._n = (w) => w.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").replace(/[^a-z0-9]/g, "");
      RB._w = (cena, palavra, n) => {{
        const alvo = RB._n(palavra), lista = RB.palavras[cena] || [];
        let k = 0;
        for (const w of lista) if (w[0].startsWith(alvo) && ++k === (n || 1)) return w;
        throw new Error(`RB: palavra "${{palavra}}" (#${{n || 1}}) não está na fala de ${{cena}}`);
      }};
      RB.t = (cena, palavra, n) => RB._w(cena, palavra, n)[1];
      RB.tf = (cena, palavra, n) => RB._w(cena, palavra, n)[2];
      RB.dur = (cena) => RB.cenas[cena].dur;
      RB.fala = (cena) => RB.cenas[cena].fala;
    </script>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}"
      data-width="1080" data-height="1920">
{chr(10).join(hosts)}
      <div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html"
        data-start="0" data-duration="{total}" data-track-index="2" data-track-kind="captions"
        data-width="1080" data-height="1920" style="z-index:5"></div>
      <div id="osd" data-composition-id="osd" data-composition-src="compositions/osd.html"
        data-start="0" data-duration="{total}" data-track-index="3" data-track-kind="graphics"
        data-width="1080" data-height="1920" style="z-index:6"></div>
      <div id="fx" data-composition-id="fx" data-composition-src="compositions/fx.html"
        data-start="0" data-duration="{total}" data-track-index="4" data-track-kind="graphics"
        data-width="1080" data-height="1920" style="z-index:7"></div>
      <audio id="narracao" class="clip" src="assets/voz/narracao.wav" data-start="0"
        data-track-index="5" data-volume="1"></audio>
{trilha}    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
    (ep / "index.html").write_text(index)

    # ——— OSD ———
    eras_js = json.dumps(eras)
    osd = f'''<template>
  <!-- GERADO por ferramentas/montar.py -->
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    #osd-play, #osd-ano, #osd-fita {{ position: absolute; font-family: var(--f-mono); font-weight: 700;
      color: var(--papel); text-shadow: 3px 0 rgba(255,59,48,.55), -3px 0 rgba(63,167,255,.55); }}
    #osd-play {{ left: 90px; top: 196px; font-size: 46px; letter-spacing: .06em; }}
    #osd-ano {{ right: 90px; top: 188px; font-size: 64px; letter-spacing: .04em; }}
    #osd-fita {{ right: 92px; top: 262px; font-size: 28px; opacity: .7; letter-spacing: .12em; }}
    #osd-ponto {{ display: inline-block; width: 24px; height: 24px; border-radius: 50%; background: var(--rec);
      margin-right: 16px; vertical-align: 4px; }}
  </style>
  <div id="root" data-composition-id="osd" data-width="1080" data-height="1920">
    <div id="osd-play" class="clip" data-start="0" data-duration="{total}"><span id="osd-ponto"></span><span id="osd-modo">PLAY ▶</span></div>
    <div id="osd-ano" class="clip" data-start="0" data-duration="{total}"><span id="osd-ano-txt">{eras[0][1] if eras else ""}</span></div>
    <div id="osd-fita" class="clip" data-start="0" data-duration="{total}">FITA {rot["id"]}</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const TOTAL = {total}, ERAS = {eras_js};
    const ponto = "#osd-ponto", modo = "#osd-modo", ano = "#osd-ano-txt";
    const ROTULOS = {json.dumps(rotulos, ensure_ascii=False)}, rotuloAno = (v) => v <= 0 ? "\\u200B" + (Math.abs(v) || 1) + " A.C." : String(v);
    for (let t = 0; t < TOTAL; t += 0.5) tl.set(ponto, {{ opacity: (Math.round(t * 2) % 2) ? 0.15 : 1 }}, t);
    // rebobinar: o contador rola em passos (como contador de fita) até o novo ano
    for (let i = 1; i < ERAS.length; i++) {{
      const [t, alvo] = ERAS[i], de = ERAS[i - 1][1], passos = 14, t0 = Math.max(t - 0.28, 0);
      tl.set(modo, {{ textContent: alvo < de ? "◀◀ REW" : "▶▶ FF" }}, t0);
      tl.set(ponto, {{ backgroundColor: "#ffd23f" }}, t0);
      for (let k = 1; k <= passos; k++) {{
        const v = Math.round(de + (alvo - de) * (1 - Math.pow(1 - k / passos, 2)));
        tl.set(ano, {{ textContent: rotuloAno(v) }}, t0 + k * (0.62 / passos));
      }}
      if (ROTULOS[t]) tl.set(ano, {{ textContent: "\\u200B" + ROTULOS[t] }}, t0 + 0.64);
      tl.set(modo, {{ textContent: "PLAY ▶" }}, t0 + 0.7);
      tl.set(ponto, {{ backgroundColor: "#ff3b30" }}, t0 + 0.7);
      tl.fromTo("#osd-ano", {{ x: -10 }}, {{ x: 0, duration: 0.3, ease: "steps(4)" }}, t0 + 0.62);
    }}
    tl.set(modo, {{ textContent: "■ STOP" }}, TOTAL - 0.9);
    tl.set(ponto, {{ opacity: 0 }}, TOTAL - 0.9);
    window.__timelines["osd"] = tl;
  </script>
</template>
'''
    (ep / "compositions" / "osd.html").write_text(osd)

    # ——— FX ———
    fx = f'''<template>
  <!-- GERADO por ferramentas/montar.py -->
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    #fx-scan {{ position: absolute; inset: 0; opacity: .09;
      background: repeating-linear-gradient(to bottom, #000 0 2px, transparent 2px 5px); }}
    #fx-vinheta {{ position: absolute; inset: 0;
      background: radial-gradient(ellipse 75% 60% at 50% 45%, transparent 55%, rgba(0,0,0,.55) 100%); }}
    #fx-grao {{ position: absolute; left: -200px; top: -200px; width: 1480px; height: 2320px; opacity: .11; mix-blend-mode: screen; }}
    .fx-banda {{ position: absolute; left: -40px; width: 1160px; opacity: 0; mix-blend-mode: screen; }}
    .fx-banda svg {{ width: 100%; height: 100%; display: block; }}
    #fx-linha {{ position: absolute; left: 0; width: 1080px; height: 6px; top: 900px; background: rgba(241,232,211,.75); opacity: 0; }}
    #fx-azul {{ position: absolute; inset: 0; background: var(--tela-azul); opacity: 0; }}
  </style>
  <div id="root" data-composition-id="fx" data-width="1080" data-height="1920">
    <svg width="0" height="0" style="position:absolute">
      <filter id="fx-ruido" x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.9 0.06" numOctaves="2" seed="7" />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <filter id="fx-ruido-fino"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="3" /><feColorMatrix type="saturate" values="0" /></filter>
    </svg>
    <div id="fx-grao" class="clip" data-start="0" data-duration="{total}"><svg width="1480" height="2320"><rect width="1480" height="2320" filter="url(#fx-ruido-fino)" /></svg></div>
    <div id="fx-scan" class="clip" data-start="0" data-duration="{total}"></div>
    <div id="fx-vinheta" class="clip" data-start="0" data-duration="{total}"></div>
    <div id="fx-b1" class="fx-banda clip" data-start="0" data-duration="{total}" style="height:140px;top:0"><svg><rect width="100%" height="100%" filter="url(#fx-ruido)" /></svg></div>
    <div id="fx-b2" class="fx-banda clip" data-start="0" data-duration="{total}" style="height:60px;top:0"><svg><rect width="100%" height="100%" filter="url(#fx-ruido)" /></svg></div>
    <div id="fx-b3" class="fx-banda clip" data-start="0" data-duration="{total}" style="height:220px;top:0"><svg><rect width="100%" height="100%" filter="url(#fx-ruido)" /></svg></div>
    <div id="fx-linha" class="clip" data-start="0" data-duration="{total}"></div>
    <div id="fx-azul" class="clip" data-start="0" data-duration="{total}"></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const TOTAL = {total}, CORTES = {json.dumps(cortes)}, TROCAS = {json.dumps(trocas)};
    // grão: salta a cada 2 frames com deslocamento pseudo-aleatório determinístico
    let s = 1234567;
    const rnd = () => ((s = (s * 16807) % 2147483647) / 2147483647);
    for (let t = 0; t < TOTAL; t += 2 / {FPS}) tl.set("#fx-grao", {{ x: Math.round(rnd() * 200 - 100), y: Math.round(rnd() * 200 - 100) }}, t);
    // corte comum: linha de tracking de 2 frames
    for (const c of CORTES) {{
      if (TROCAS.some((t) => Math.abs(t - c) < 0.01)) continue;
      const y = 500 + Math.round(rnd() * 700);
      tl.set("#fx-linha", {{ opacity: 0.8, y: y - 900 }}, c);
      tl.set("#fx-linha", {{ opacity: 0 }}, c + 2 / {FPS});
    }}
    // troca de era: faixas de ruído varrem a tela (rebobinar)
    tl.set(".fx-banda", {{ opacity: 0 }}, 0);
    for (const t of TROCAS) {{
      const t0 = Math.max(t - 0.28, 0);
      [["#fx-b1", 1920, -200, 0.55], ["#fx-b2", 1600, -100, 0.42], ["#fx-b3", 2000, -300, 0.65]].forEach(([el, de, ate, d], i) => {{
        tl.fromTo(el, {{ y: de, opacity: 0.85 }}, {{ y: ate, duration: d, ease: "none", immediateRender: false }}, t0 + i * 0.05);
        tl.set(el, {{ opacity: 0 }}, t0 + i * 0.05 + d);
      }});
    }}
    // fecho: tela azul de VHS
    tl.fromTo("#fx-azul", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12, ease: "steps(3)" }}, TOTAL - 0.62);
    window.__timelines["fx"] = tl;
  </script>
</template>
'''
    (ep / "compositions" / "fx.html").write_text(fx)

    # ——— LEGENDAS ———
    grupos = agrupar_legendas(tem["palavras"])
    els, js = [], []
    for gi, g in enumerate(grupos):
        ini = max(g[0]["start"] - 0.06, 0.1)
        fim = g[-1]["end"] + 0.12
        if gi + 1 < len(grupos):
            fim = min(fim if fim > g[-1]["end"] + 0.05 else g[-1]["end"] + 0.05, grupos[gi + 1][0]["start"] - 0.07)
            fim = max(fim, ini + 0.3)
        tam, quebra = medir_legenda([x["txt"] for x in g])
        spans = "".join(f'<span id="lg-{gi}-{k}">{x["txt"]}</span>' + ("" if k + 1 == len(g) else "<br>" if k + 1 == quebra else " ")
                        for k, x in enumerate(g))
        els.append(f'    <div id="lg-{gi}" class="lg clip" data-start="{r2(ini)}" data-duration="{r2(fim - ini)}"><p style="font-size:{tam}px">{spans}</p></div>')
        js.append(f'    tl.fromTo("#lg-{gi} p", {{ scale: 0.86, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.12, ease: "power3.out" }}, {r2(ini)});')
        for k, x in enumerate(g):
            js.append(f'    tl.set("#lg-{gi}-{k}", {{ color: "#ffd23f" }}, {r2(max(x["start"], ini))});')
            if k + 1 < len(g):
                js.append(f'    tl.set("#lg-{gi}-{k}", {{ color: "#f1e8d3" }}, {r2(g[k + 1]["start"])});')
        js.append(f'    tl.set("#lg-{gi} p", {{ opacity: 0 }}, {r2(fim - 0.02)});')
    legendas = f'''<template>
  <!-- GERADO por ferramentas/montar.py -->
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .lg {{ position: absolute; left: {LG_ESQ}px; top: 1110px; width: {LG_LARGURA}px; height: 190px; display: flex; align-items: center; justify-content: center; }}
    .lg p {{ width: {LG_LARGURA}px; text-align: center; font-family: var(--f-legenda); font-weight: 900; line-height: 1.05;
      color: var(--papel); -webkit-text-stroke: 12px #000; paint-order: stroke fill; letter-spacing: .01em; overflow: visible; }}
  </style>
  <div id="root" data-composition-id="legendas" data-width="1080" data-height="1920">
{chr(10).join(els)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["legendas"] = tl;
  </script>
</template>
'''
    (ep / "compositions" / "legendas.html").write_text(legendas)

    # ——— rascunhos de cena (só se não existirem) ———
    novos = []
    for c, (cid, ini, dur) in zip(cenas, janelas):
        f = ep / "compositions" / f"{cid}.html"
        if f.exists():
            continue
        linhas = "".join(f'<div class="rb-titulo" style="font-size:120px">{t}</div>' for t in c.get("tela", []))
        f.write_text(f'''<template>
  <!-- RASCUNHO gerado por montar.py. O agente animador substitui este arquivo pela cena real.
       Cena {cid} · {c.get("batida")} · forma: {c.get("forma")}
       Fala: {c["fala"]}
       Visual pedido: {c.get("visual", "")} -->
  <style>#root {{ position: absolute; inset: 0; background: var(--fita); }} #{cid}-txt {{ top: 420px; }}</style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
    <div id="{cid}-txt" class="rb-coluna clip" data-start="0" data-duration="{dur}">{linhas}</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#{cid}-txt div", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25, stagger: 0.3, ease: "power3.out" }}, 0.1);
    window.__timelines["{cid}"] = tl;
  </script>
</template>
''')
        novos.append(cid)

    print(f"✓ montado: {len(janelas)} cenas · {total:.1f}s · {len(grupos)} grupos de legenda · {len(trocas)} trocas de era")
    for cid, ini, dur in janelas:
        print(f"   {cid}: {ini:6.2f}s → {ini + dur:6.2f}s  ({dur:.2f}s)")
    if novos:
        print(f"   rascunhos criados: {', '.join(novos)}")


if __name__ == "__main__":
    main()
