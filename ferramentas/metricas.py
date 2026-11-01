#!/usr/bin/env python3
"""Desempenho dos vídeos publicados, guardado em canal/metricas.json (uma foto por dia, por episódio).

Uso:
    python3 ferramentas/metricas.py            coleta YouTube e TikTok com yt-dlp, salva e mostra
    python3 ferramentas/metricas.py --ler      só mostra o que já foi salvo (sem rede)
    python3 ferramentas/metricas.py --manual 004 tiktok views=1200 likes=30 comentarios=4 compart=2
    python3 ferramentas/metricas.py --manual 004 youtube retencao=62

A coleta também compara o título publicado com publicacao.json e avisa de Short no canal que falta em
canal/historico.json. Sai com código 1 se houver divergência. Retenção só existe no Studio: anote com --manual.
"""
import json, subprocess, sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
HISTORICO = RAIZ / "canal" / "historico.json"
METRICAS = RAIZ / "canal" / "metricas.json"
CANAL_SHORTS = "https://www.youtube.com/@RebobinaNaHistoria/shorts"
CAMPOS = "%(.{id,title,view_count,like_count,comment_count,repost_count})j"
TIMEOUT_S = 60
VIDEOS_PARA_CONCLUIR = 20


def yt_dlp(*args):
    """Linhas JSON do yt-dlp. Falha vira lista vazia: número ausente nunca é preenchido com palpite."""
    try:
        r = subprocess.run(["yt-dlp", "--no-warnings", "--skip-download", "-O", CAMPOS, *args],
                           capture_output=True, text=True, timeout=TIMEOUT_S)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []
    return [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]


def numeros(v):
    pares = {"views": v.get("view_count"), "likes": v.get("like_count"), "comentarios": v.get("comment_count"), "compart": v.get("repost_count")}
    return {k: n for k, n in pares.items() if n is not None}


def carregar():
    return json.loads(METRICAS.read_text()) if METRICAS.exists() else {}


def anotar(dados, ep_id, plataforma, valores):
    """Mescla na foto de hoje: a coleta automática e a anotação manual convivem."""
    fotos = dados.setdefault(ep_id, [])
    if not fotos or fotos[-1]["data"] != date.today().isoformat():
        fotos.append({"data": date.today().isoformat()})
    fotos[-1].setdefault(plataforma, {}).update(valores)


def titulo_esperado(item):
    arq = RAIZ / "episodios" / f"{item['id']}-{item['slug']}" / "publicacao.json"
    return json.loads(arq.read_text())["youtube"]["titulo"].strip() if arq.exists() else None


def coletar(dados, historico):
    problemas = []
    for item in historico:
        links = item.get("links", {})
        if links.get("youtube"):
            achado = yt_dlp(links["youtube"])
            if achado:
                anotar(dados, item["id"], "youtube", numeros(achado[0]))
                esperado = titulo_esperado(item)
                if esperado and achado[0]["title"].strip() != esperado:
                    problemas.append(f'{item["id"]}: título no YouTube é "{achado[0]["title"]}", deveria ser "{esperado}"')
            else:
                print(f"⚠ {item['id']}: YouTube não respondeu")
        if links.get("tiktok"):
            achado = yt_dlp(links["tiktok"])
            if achado:
                anotar(dados, item["id"], "tiktok", numeros(achado[0]))
            else:
                print(f"⚠ {item['id']}: TikTok não respondeu; anote com --manual")
    conhecidos = " ".join(i.get("links", {}).get("youtube", "") for i in historico)
    for v in yt_dlp("--flat-playlist", CANAL_SHORTS):
        if v["id"] not in conhecidos:
            problemas.append(f'Short "{v["title"]}" ({v["id"]}) está no canal e falta em canal/historico.json')
    return problemas


def mostrar(dados, historico):
    fmt = lambda d, k: f"{d[k]:,}".replace(",", ".") if k in d else "-"
    print("ep   idade  YT views  YT likes  retenção  TT views  TT likes  última foto")
    for item in historico:
        fotos = dados.get(item["id"])
        if not fotos:
            continue
        ult = fotos[-1]
        yt, tk = ult.get("youtube", {}), ult.get("tiktok", {})
        idade = (date.fromisoformat(ult["data"]) - date.fromisoformat(item["data"])).days
        ret = f"{yt['retencao']}%" if "retencao" in yt else "-"
        print(f"{item['id']:<4} {idade:>3} d  {fmt(yt, 'views'):>8}  {fmt(yt, 'likes'):>8}  {ret:>8}  {fmt(tk, 'views'):>8}  {fmt(tk, 'likes'):>8}  {ult['data']}")
    if len(dados) < VIDEOS_PARA_CONCLUIR:
        print(f"Só {len(dados)} vídeos medidos: sinal fraco. Não mude regra do canal por causa disto antes de {VIDEOS_PARA_CONCLUIR}.")


def main():
    historico = json.loads(HISTORICO.read_text())
    dados = carregar()
    if "--manual" in sys.argv:
        i = sys.argv.index("--manual")
        ep_id, plataforma = sys.argv[i + 1], sys.argv[i + 2]
        anotar(dados, ep_id, plataforma, {k: float(v) if "." in v else int(v) for k, v in (a.split("=", 1) for a in sys.argv[i + 3:])})
        METRICAS.write_text(json.dumps(dados, ensure_ascii=False, indent=1))
        problemas = []
    elif "--ler" in sys.argv:
        problemas = []
    else:
        problemas = coletar(dados, historico)
        METRICAS.write_text(json.dumps(dados, ensure_ascii=False, indent=1))
    mostrar(dados, historico)
    for p in problemas:
        print("✗", p)
    sys.exit(1 if problemas else 0)


if __name__ == "__main__":
    main()
