#!/usr/bin/env python3
"""Monta a página de escolha de áudio: por padrão, do teste de pronúncia (canal/voz/pronuncia-teste/escolher.html).

Rode depois de testar_pronuncia.sh e publique o HTML como artifact (os áudios vão embutidos).
Com "sfx", monta a página dos efeitos sonoros candidatos (canal/sfx/candidatos/escolher.html).
"""
import base64, html, json, sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent.parent / "canal" / "voz" / "pronuncia-teste"
RODADA = 6  # mude a cada rodada nova: é a chave das marcações salvas no aparelho
INTRO_VOZ = "Ouça as opções e marque a melhor. Tudo usa a sua voz clonada. Nas comparações, a primeira opção é a grafia normal; só muda a escrita. Pode responder só parte e voltar depois: suas marcações ficam salvas neste aparelho. No fim, copie a resposta e cole na conversa."
CSS = """
/* Fita VHS: lista única, um cartão por palavra, resposta fixa no fim */
:root{--bg:#121016;--sup:#1d1a24;--fg:#efe9dc;--mut:#a9a3b3;--vhs:#f2c94c;--azul:#2a2fd0;--lin:#3a3744;color-scheme:dark;--d:"League Gothic",Impact,sans-serif;--m:"Space Mono",ui-monospace,Menlo,monospace}
body{background:var(--bg);color:var(--fg);font:15px/1.5 var(--m)}
main{max-width:640px;margin:auto;padding-block:24px 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:20px}
h1{font:400 56px/1 var(--d);margin:0;letter-spacing:.01em;text-wrap:balance}
.tag{color:var(--vhs);font-weight:700;margin:0 0 6px}
.intro{margin:10px 0 0;color:var(--mut)}
section{background:var(--sup);padding:16px;border-radius:4px;display:grid;gap:10px}
h2.grupo{font:400 40px/1.05 var(--d);margin:16px 0 0;color:var(--vhs);letter-spacing:.01em;text-wrap:balance}
h3,#res h2{font:400 34px/1 var(--d);margin:0;letter-spacing:.01em}
.frase{color:var(--fg);font-size:15px}
.qual{width:100%;height:auto;box-sizing:border-box;padding:10px;font:14px var(--m);background:var(--bg);color:var(--fg);border:1px solid var(--lin);border-radius:4px}
.fr{margin:0;color:var(--mut);font-size:13px}.fr b{color:var(--fg)}
.op{display:grid;gap:6px;padding-top:10px;border-top:1px solid var(--lin);min-width:0}
label{display:flex;gap:10px;align-items:center;cursor:pointer;min-width:0}
input[type=radio]{accent-color:var(--vhs);width:20px;height:20px;flex:none}
.let{font-weight:700;color:var(--vhs)}.txt{min-width:0;overflow-wrap:anywhere}
audio{width:100%;height:40px}
#res{background:var(--azul);padding:16px;border-radius:4px;display:grid;gap:10px}
#res h2{color:#fff}
pre{margin:0;white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.5 var(--m);color:#fff}
button{font:700 15px var(--m);padding:12px;border:0;border-radius:4px;background:var(--vhs);color:#121016;cursor:pointer}
:focus-visible{outline:2px solid var(--vhs);outline-offset:2px}
"""
JS = """
let s={},q={};try{const d=JSON.parse(localStorage.getItem(K))||{};s=d.s||{};q=d.q||{}}catch(e){}
const secs=[...document.querySelectorAll("section")],saida=document.getElementById("saida"),cont=document.getElementById("cont");
function pinta(){const l=[];secs.forEach(x=>{const v=s[x.dataset.id];if(v)l.push(x.dataset.termo+" = "+v+(v==="ruim"&&q[x.dataset.id]?": "+q[x.dataset.id]:""))});saida.textContent=l.length?l.join("\\n"):"Nenhuma escolha ainda.";cont.textContent=l.length+" de "+secs.length+" escolhidas";try{localStorage.setItem(K,JSON.stringify({s,q}))}catch(e){}}
secs.forEach(x=>{const v=s[x.dataset.id];const t=x.querySelector(".qual");if(t){t.value=q[x.dataset.id]||"";t.addEventListener("input",()=>{q[x.dataset.id]=t.value;s[x.dataset.id]="ruim";x.querySelector("input[value=ruim]").checked=true;pinta()})}x.querySelectorAll("input[type=radio]").forEach(i=>{if(i.value===v)i.checked=true;i.addEventListener("change",()=>{s[x.dataset.id]=i.value;pinta()})})});
document.addEventListener("play",e=>document.querySelectorAll("audio").forEach(a=>{if(a!==e.target)a.pause()}),true);
document.getElementById("copiar").addEventListener("click",async e=>{try{await navigator.clipboard.writeText(saida.textContent);e.target.textContent="Copiado"}catch(x){const r=document.createRange();r.selectNodeContents(saida);const g=getSelection();g.removeAllRanges();g.addRange(r);e.target.textContent="Texto selecionado: copie manualmente"}});
pinta();
"""


def main():
    global PASTA
    nome, titulo, intro = "Pronúncia do Rebobina", "Como cada palavra deve soar", INTRO_VOZ
    if sys.argv[1:] == ["sfx"]:
        PASTA = PASTA.parent.parent / "sfx" / "candidatos"
        nome, titulo, intro = "Efeitos do Rebobina", "Como cada ação deve soar", "Ouça as opções e marque o melhor som para cada ação. Se nada servir, marque Nenhuma ficou boa. No fim, copie a resposta e cole na conversa."
    candidatos = json.loads((PASTA / "candidatos.json").read_text())
    secoes, grupo = [], None
    for it in candidatos:
        if it.get("grupo") != grupo:
            grupo = it.get("grupo")
            secoes.append(f'<h2 class="grupo">{html.escape(grupo or "")}</h2>')
        if it.get("tipo") == "frase":  # uma faixa só: a pessoa diz se alguma palavra soou mal
            audio = base64.b64encode((PASTA / "audio" / f"{it['id']}-0.mp3").read_bytes()).decode()
            secoes.append(f'<section data-termo="{html.escape(it["termo"])}" data-id="{it["id"]}"><h3>{html.escape(it["termo"])}</h3>'
                          f'<p class="fr frase">{html.escape(it["opcoes"][0])}</p><audio controls preload="none" src="data:audio/mpeg;base64,{audio}"></audio>'
                          f'<div class="op"><label><input type="radio" name="{it["id"]}" value="soou bem" id="{it["id"]}-b"><span class="txt">Soou bem</span></label>'
                          f'<label><input type="radio" name="{it["id"]}" value="ruim" id="{it["id"]}-r"><span class="txt">Alguma palavra soou mal</span></label>'
                          f'<input class="qual" type="text" id="{it["id"]}-q" placeholder="Quais palavras?" aria-label="Quais palavras soaram mal"></div></section>')
            continue
        ops = []
        for n, o in enumerate(it["opcoes"]):
            audio = base64.b64encode((PASTA / "audio" / f"{it['id']}-{n}.mp3").read_bytes()).decode()
            ops.append(f'<div class="op"><label><input type="radio" name="{it["id"]}" value="{html.escape(o)}" id="{it["id"]}-{n}">'
                       f'<span class="let">{"ABCDEF"[n]}</span><span class="txt">{html.escape(o)}</span></label>'
                       f'<audio controls preload="none" src="data:audio/mpeg;base64,{audio}"></audio></div>')
        ops.append(f'<div class="op"><label><input type="radio" name="{it["id"]}" value="NENHUMA" id="{it["id"]}-x">'
                   '<span class="let">–</span><span class="txt">Nenhuma ficou boa</span></label></div>')
        frase = html.escape(it["frase"]).replace("{}", f"<b>{html.escape(it['termo'])}</b>")
        secoes.append(f'<section data-termo="{html.escape(it["termo"])}" data-id="{it["id"]}"><h3>{html.escape(it["termo"])}</h3>'
                      f'{"<p class=fr>" + frase + "</p>" if frase else ""}{"".join(ops)}</section>')
    pagina = f"""<title>{nome}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=League+Gothic&family=Space+Mono:wght@400;700&display=swap">
<style>{CSS}</style>
<main>
<header><p class="tag">◀◀ REW · TESTE DE VOZ</p><h1>{titulo}</h1>
<p class="intro">{intro}</p></header>
{"".join(secoes)}
<div id="res"><h2 id="cont">0 de {len(candidatos)} escolhidas</h2><pre id="saida">Nenhuma escolha ainda.</pre><button id="copiar" type="button">Copiar resposta</button></div>
</main>
<script>const K="rebobina-{PASTA.parent.name}-{RODADA}";{JS}</script>"""
    (PASTA / "escolher.html").write_text(pagina)
    print(f"✓ {PASTA / 'escolher.html'} ({len(pagina) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
