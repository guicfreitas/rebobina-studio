#!/usr/bin/env bash
# Renderiza um episódio.  Uso: ferramentas/renderizar.sh episodios/001-acre-cavalo [rascunho|final]
#   rascunho -> render/rascunho.mp4 (rápido, para revisão)   final -> render/final.mp4 (qualidade de entrega)
set -euo pipefail
EP="$1"; MODO="${2:-rascunho}"
cd "$EP"
mkdir -p render
if [ "$MODO" = "final" ]; then Q=delivery; OUT=render/final.mp4; else Q=draft; OUT=render/rascunho.mp4; fi
npx --yes hyperframes check --json > render/check.json || { echo "✗ check falhou — veja render/check.json"; exit 1; }
npx --yes hyperframes render --quality "$Q" --output "$OUT"
echo "✓ $EP/$OUT"
