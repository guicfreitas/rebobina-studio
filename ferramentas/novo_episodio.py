#!/usr/bin/env python3
"""Cria a pasta de um episódio novo: episodios/<NNN>-<slug>/

Uso:  python3 ferramentas/novo_episodio.py ferrovia-do-diabo
Imprime o caminho criado. O roteirista escreve ali o roteiro.json.
"""
import json, re, shutil, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
slug = re.sub(r"[^a-z0-9-]+", "-", sys.argv[1].lower()).strip("-")
eps = RAIZ / "episodios"
nums = [int(p.name[:3]) for p in eps.glob("[0-9][0-9][0-9]-*")]
ep = eps / f"{(max(nums) + 1 if nums else 1):03d}-{slug}"
ep.mkdir(parents=True)
shutil.copy2(RAIZ / "templates" / "base-video" / "hyperframes.json", ep / "hyperframes.json")
print(ep.relative_to(RAIZ))
