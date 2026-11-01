#!/usr/bin/env python3
"""Sinais de procura para escolher pauta e título, sem chave de API.

Uso:
    python3 ferramentas/sinais.py "guerra dos emus" "exército de terracota"
    python3 ferramentas/sinais.py --descobrir

Por termo: autocomplete do YouTube no Brasil, views mensais do artigo na Wikipédia em português e vídeos
concorrentes na busca do YouTube. --descobrir: o autocomplete de perguntas abertas, para achar mitos e dúvidas.
Autocomplete mostra o que as pessoas digitam, não quantas: não é volume de busca. Fonte que falha é avisada,
nunca preenchida.
"""
import json, subprocess, sys
from datetime import date
from urllib.parse import quote, urlencode

AGENTE = "rebobina-sinais/1.0 (canal de historia; uso pessoal)"
TIMEOUT_S = 20
MESES = 3
BUSCA_N = 30
SHORT_MAX_S = 180
MOSTRAR = 5
SEMENTES = ("por que o brasil", "por que os", "por que a", "é verdade que", "quem inventou", "como surgiu", "qual a origem",
            "de onde veio", "o que aconteceu com")


def pegar_json(url, **params):
    # curl, não urllib: o Python do Mac costuma vir sem certificados SSL
    r = subprocess.run(["curl", "-sSf", "-m", str(TIMEOUT_S), "-A", AGENTE, f"{url}?{urlencode(params)}" if params else url],
                       capture_output=True, check=True)
    return json.loads(r.stdout.decode("utf-8", errors="replace"))


def autocomplete(consulta):
    return pegar_json("https://suggestqueries.google.com/complete/search", client="firefox", ds="yt", hl="pt", gl="BR", q=consulta)[1]


def mostrar_autocomplete(consultas):
    vistos = {}
    falhas = 0
    for q in consultas:
        try:
            for s in autocomplete(q):
                vistos.setdefault(s.lower().strip(), s)
        except Exception:
            falhas += 1
    print(f"  autocomplete do YouTube (BR): {len(vistos)} sugestões" + (f", {falhas} consulta(s) falharam" if falhas else ""))
    for s in vistos.values():
        print(f"    - {s}")


def meses_fechados():
    ano, mes = date.today().year, date.today().month
    fim = date(ano, mes, 1)
    for _ in range(MESES):
        mes = mes - 1 or 12
        ano = ano - 1 if mes == 12 else ano
    return date(ano, mes, 1), fim


def mostrar_wikipedia(termo):
    try:
        achados = pegar_json("https://pt.wikipedia.org/w/api.php", action="opensearch", search=termo, limit=1, format="json")[1]
        if not achados:
            print("  Wikipédia pt: nenhum artigo encontrado")
            return
        ini, fim = meses_fechados()
        artigo = quote(achados[0].replace(" ", "_"), safe="")
        url = (f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/pt.wikipedia/all-access/user/{artigo}"
               f"/monthly/{ini:%Y%m}0100/{fim:%Y%m}0100")
        itens = pegar_json(url)["items"]
        por_mes = ", ".join(f"{i['timestamp'][:4]}-{i['timestamp'][4:6]}: {i['views']}" for i in itens)
        print(f'  Wikipédia pt, artigo mais próximo "{achados[0]}": {por_mes} (views por mês)')
    except Exception as e:
        print(f"  ⚠ Wikipédia indisponível: {e}")


def mostrar_concorrentes(termo):
    try:
        r = subprocess.run(["yt-dlp", "--no-warnings", "--flat-playlist", "--extractor-args", "youtube:lang=pt",
                            "-O", "%(.{title,view_count,duration,channel})j", f"ytsearch{BUSCA_N}:{termo}"],
                           capture_output=True, text=True, timeout=TIMEOUT_S * 3)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"  ⚠ busca do YouTube indisponível: {e}")
        return
    videos = [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]
    if not videos:
        print("  ⚠ busca do YouTube sem resultados legíveis")
        return
    curtos = [v for v in videos if (v.get("duration") or SHORT_MAX_S + 1) <= SHORT_MAX_S]
    longos = [v for v in videos if v not in curtos]
    print(f"  busca do YouTube: {len(videos)} resultados, {len(curtos)} de até {SHORT_MAX_S} s")
    for rotulo, grupo in (("curtos", curtos), ("longos", longos)):
        for v in sorted(grupo, key=lambda v: v.get("view_count") or 0, reverse=True)[:MOSTRAR]:
            print(f"    [{rotulo}] {v.get('view_count') or '?'} views · {v.get('duration') or '?'} s · {v.get('channel')} · {v.get('title')}")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    print(f"Sinais coletados em {date.today().isoformat()}")
    if args == ["--descobrir"]:
        mostrar_autocomplete(SEMENTES)
        return
    for termo in args:
        print(f'\n"{termo}"')
        mostrar_autocomplete((termo, f"por que {termo}", f"{termo} é verdade", f"verdade sobre {termo}"))
        mostrar_wikipedia(termo)
        mostrar_concorrentes(termo)


if __name__ == "__main__":
    main()
