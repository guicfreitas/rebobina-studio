#!/usr/bin/env python3
"""Aplica o dicionário de pronúncia do canal (canal/pronuncia.json) ao texto que a voz lê.

A legenda continua usando "fala"; só "fala_tts" recebe a grafia fonética. O dicionário vale para todos os
episódios: {"Giles Corey": "Djáils Córi"}. A chave mais longa ganha, sem diferenciar maiúsculas.

Uso:  python3 ferramentas/pronuncia.py <roteiro.json> <saida.json>
"""
import json, re, sys
from pathlib import Path

DICIONARIO = Path(__file__).resolve().parent.parent / "canal" / "pronuncia.json"


def aplicar(texto, dicionario=None):
    dicionario = json.loads(DICIONARIO.read_text()) if dicionario is None else dicionario
    if not dicionario:
        return texto
    termos = sorted(dicionario, key=len, reverse=True)
    padrao = re.compile(r"(?<!\w)(" + "|".join(map(re.escape, termos)) + r")(?!\w)", re.IGNORECASE)
    minusculas = {t.lower(): v for t, v in dicionario.items()}
    return padrao.sub(lambda m: minusculas[m.group(1).lower()], texto)


def aplicar_roteiro(roteiro):
    dicionario = json.loads(DICIONARIO.read_text())
    for c in roteiro["cenas"]:
        c["fala_tts"] = aplicar(c.get("fala_tts") or c["fala"], dicionario)
    return roteiro


if __name__ == "__main__":
    roteiro = aplicar_roteiro(json.loads(Path(sys.argv[1]).read_text()))
    Path(sys.argv[2]).write_text(json.dumps(roteiro, ensure_ascii=False, indent=1))
