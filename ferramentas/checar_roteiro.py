#!/usr/bin/env python3
"""Checagem automática do roteiro: pega o que é contável antes de gastar uma rodada do revisor-roteiro.

Uso:  python3 ferramentas/checar_roteiro.py episodios/006-slug

Confere: palavras e duração estimada, cenas, frases, tela, formas, capa, referências e fontes dos fatos, e variedade
contra os episódios anteriores (pastas de episodios/, publicados ou não). ✗ = P0, sai com código 1. ⚠ = P1.
Não substitui o revisor: ele continua checando se as fontes dizem mesmo o que o roteiro afirma.
"""
import json, re, sys, unicodedata
from pathlib import Path
from urllib.parse import urlparse

RAIZ = Path(__file__).resolve().parent.parent
PALAVRAS_POR_S = 2.35             # medido nos episódios 002 a 005 (2,24 a 2,44)
INICIO_E_FIM_S = 1.5
PALAVRAS_MIN, PALAVRAS_MAX = 170, 230
CENAS_MIN, CENAS_MAX = 10, 14
FRASE_MAX = 14
TELA_PALAVRAS, TELA_LINHAS = 5, 4
FORMAS_MIN = 5
FORMAS = {"mapa", "linha-do-tempo", "ficha-de-arquivo", "documento", "recibo", "numero-que-cai", "mito-x-fato", "antes-e-depois",
          "multidao-de-pontos", "citacao-poster", "comparacao-de-escala", "objeto-simbolo", "manchete-de-jornal"}
AMERICA_LATINA = {"América do Sul", "América Central", "América Latina", "Brasil", "Caribe"}
PROIBIDOS = ("olá", "se inscreva", "deixa o like", "deixe o like", "você não vai acreditar")
SUFIXOS_DUPLOS = ("com.br", "gov.br", "org.br", "edu.br", "co.uk", "ac.uk", "org.uk", "gov.uk", "edu.au", "gov.au", "org.au", "com.au")


def sem_acento(txt):
    return "".join(c for c in unicodedata.normalize("NFD", txt) if unicodedata.category(c) != "Mn")


def dominio(url):
    """en.wikipedia.org e pt.wikipedia.org contam como a mesma fonte."""
    partes = (urlparse(url).hostname or "").lower().split(".")
    return ".".join(partes[-3:] if ".".join(partes[-2:]) in SUFIXOS_DUPLOS else partes[-2:])


def frases(fala):
    return [f for f in re.split(r"[.!?…]+", re.sub(r"\b([ad])\.C\.", r"\1C", fala)) if f.strip()]


def checar_fala(rot, p0, p1):
    cenas = rot["cenas"]
    n = sum(len(c["fala"].split()) for c in cenas)
    estimada = n / PALAVRAS_POR_S + INICIO_E_FIM_S
    if n < PALAVRAS_MIN:
        p0.append(f"{n} palavras (mínimo {PALAVRAS_MIN}): risco de ficar abaixo de 65 s")
    elif n > PALAVRAS_MAX:
        p1.append(f"{n} palavras (máximo {PALAVRAS_MAX}): passa de 90 s")
    if not CENAS_MIN <= len(cenas) <= CENAS_MAX:
        p1.append(f"{len(cenas)} cenas (esperado {CENAS_MIN} a {CENAS_MAX})")
    for c in cenas:
        for f in frases(c["fala"]):
            if len(f.split()) > FRASE_MAX:
                p1.append(f'{c["id"]}: frase com {len(f.split())} palavras: "{f.strip()}"')
        if re.search(r"\d", c["fala"]):
            p1.append(f'{c["id"]}: número em algarismos na fala (use por extenso): "{c["fala"]}"')
        baixa = c["fala"].lower()
        p0 += [f'{c["id"]}: expressão proibida na fala: "{x}"' for x in PROIBIDOS if re.search(rf"\b{x}\b", baixa)]
        tela = c.get("tela", [])
        if len(tela) > TELA_LINHAS:
            p1.append(f'{c["id"]}: tela com {len(tela)} linhas (máximo {TELA_LINHAS})')
        p1 += [f'{c["id"]}: tela com mais de {TELA_PALAVRAS} palavras: "{t}"' for t in tela if len(t.split()) > TELA_PALAVRAS]
    return n, estimada


def checar_formas(rot, p1):
    formas = [sem_acento(c["forma"]) for c in rot["cenas"]]
    p1 += [f"{c['id']}: forma fora do catálogo: {c['forma']}" for c in rot["cenas"] if sem_acento(c["forma"]) not in FORMAS]
    if len(set(formas)) < FORMAS_MIN:
        p1.append(f"{len(set(formas))} formas diferentes (mínimo {FORMAS_MIN})")
    p1 += [f"{a['id']} e {b['id']}: mesma forma em cenas seguidas ({a['forma']})"
           for a, b in zip(rot["cenas"], rot["cenas"][1:]) if sem_acento(a["forma"]) == sem_acento(b["forma"])]


def checar_capa(rot, p1):
    capa = rot.get("capa")
    if not capa:
        p1.append("sem o campo capa (linhas e símbolo: ver agente roteirista)")
        return
    linhas = capa.get("linhas", [])
    if not 1 <= len(linhas) <= TELA_LINHAS:
        p1.append(f"capa com {len(linhas)} linhas (de 1 a {TELA_LINHAS})")
    p1 += [f'capa com mais de {TELA_PALAVRAS} palavras na linha: "{t}"' for t in linhas if len(t.replace("*", "").split()) > TELA_PALAVRAS]
    if "*" not in "".join(linhas):
        p1.append("capa sem *palavra em destaque*")
    if not capa.get("simbolo"):
        p1.append("capa sem símbolo")


def checar_fatos(rot, p0, p1):
    fatos = {f["id"]: f for f in rot.get("fatos", [])}
    usados = {x for c in rot["cenas"] for x in c.get("fatos", [])}
    p0 += [f"cena cita o fato {x}, que não existe em fatos" for x in sorted(usados - fatos.keys())]
    p1 += [f"fato {x} não é usado por nenhuma cena" for x in sorted(fatos.keys() - usados)]
    p1 += [f"{c['id']}: cena sem fato ligado" for c in rot["cenas"] if not c.get("fatos")]
    for f in fatos.values():
        doms = {dominio(u) for u in f.get("fontes", [])}
        if len(doms) < 2:
            p0.append(f"fato {f['id']}: {len(doms)} fonte(s) de domínios diferentes (mínimo 2)")


def anteriores(rot):
    """Roteiros com id menor, do mais antigo ao mais recente."""
    saida = []
    for arq in sorted((RAIZ / "episodios").glob("*/roteiro.json")):
        r = json.loads(arq.read_text())
        if r["id"] < rot["id"]:
            saida.append(r)
    return saida


def checar_variedade(rot, p1):
    velhos = anteriores(rot)
    seq = [sem_acento(c["forma"]) for c in rot["cenas"]]
    p1 += [f"mesma sequência de formas do episódio {v['id']}" for v in velhos[-10:]
           if [sem_acento(c["forma"]) for c in v["cenas"]] == seq]
    p1 += [f"mesma forma de gancho do episódio {v['id']} ({rot['cenas'][0]['forma']})" for v in velhos[-3:]
           if sem_acento(v["cenas"][0]["forma"]) == seq[0]]
    p1 += [f"mesmo acento do episódio {v['id']} ({rot.get('acento')})" for v in velhos[-3:]
           if (v.get("acento") or "").lower() == (rot.get("acento") or "").lower()]
    regioes = [v.get("regiao") for v in velhos[-2:]] + [rot.get("regiao")]
    if len(regioes) == 3:
        if len(set(regioes)) == 1:
            p1.append(f"terceiro vídeo seguido em {rot.get('regiao')} (máximo 2)")
        if set(regioes) <= AMERICA_LATINA:
            p1.append("3 vídeos seguidos na América Latina (a cada 3, pelo menos 1 de fora)")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ep = Path(sys.argv[1]).resolve()
    rot = json.loads((ep / "roteiro.json").read_text())
    p0, p1 = [], []
    n, estimada = checar_fala(rot, p0, p1)
    checar_formas(rot, p1)
    checar_capa(rot, p1)
    checar_fatos(rot, p0, p1)
    checar_variedade(rot, p1)
    for p in p0:
        print("✗", p)
    for p in p1:
        print("⚠", p)
    print(f"{'✗' if p0 else '✓'} {rot['id']}: {n} palavras, cerca de {estimada:.0f} s, {len(p0)} P0, {len(p1)} P1")
    sys.exit(1 if p0 else 0)


if __name__ == "__main__":
    main()
