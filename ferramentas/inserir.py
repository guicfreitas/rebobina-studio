#!/usr/bin/env python3
"""Insere SVGs (mapas, símbolos) dentro das cenas, sem copiar e colar à mão.

Uso:  python3 ferramentas/inserir.py episodios/001-acre-cavalo

Numa cena, escreva um marcador onde o SVG deve entrar:
    <!--@cavalo-->              -> assets/simbolos/cavalo.svg
    <!--@mapa:regiao-->         -> assets/mapas/regiao.svg   (gerado por mapa.mjs)
    <!--@svg:simbolos/medalha--> -> assets/simbolos/medalha.svg
O script troca o marcador por  <!--@nome--> ...svg... <!--/@nome-->  e pode ser rodado de novo
(atualiza o conteúdo). Os ids do SVG ganham o prefixo da cena (c05-pais-bolivia), para não
repetir ids quando o mesmo mapa aparece em duas cenas.
"""
import re, sys
from pathlib import Path

ep = Path(sys.argv[1]).resolve()
padrao = re.compile(r"<!--@([\w:/.-]+)-->(.*?<!--/@\1-->)?", re.S)


def arquivo(nome):
    if nome == "cavalo":
        return ep / "assets/simbolos/cavalo.svg"
    tipo, _, resto = nome.partition(":")
    return ep / "assets" / ("mapas" if tipo == "mapa" else "") / f"{resto}.svg"


total = 0
for f in sorted((ep / "compositions").glob("*.html")):
    txt = f.read_text()
    m_id = re.search(r'data-composition-id="([^"]+)"', txt)
    pref = m_id.group(1) if m_id else f.stem

    def troca(m):
        global total
        nome = m.group(1)
        src = arquivo(nome)
        if not src.exists():
            sys.exit(f"✗ {f.name}: {src} não existe")
        svg = re.sub(r"<!--.*?-->\s*", "", src.read_text()).strip()
        svg = re.sub(r'\bid="([^"]+)"', lambda k: f'id="{pref}-{k.group(1)}"', svg)
        svg = re.sub(r'url\(#([^)]+)\)', lambda k: f'url(#{pref}-{k.group(1)})', svg)
        total += 1
        return f"<!--@{nome}-->{svg}<!--/@{nome}-->"

    novo = padrao.sub(troca, txt)
    if novo != txt:
        f.write_text(novo)
print(f"✓ {total} inserções")
