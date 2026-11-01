#!/usr/bin/env bash
# Gera a narração de um episódio com Qwen3-TTS numa GPU T4 do Google Colab, pelo terminal (Colab CLI oficial).
#
# Uso:  ferramentas/narrar_colab.sh episodios/002-guerra-dos-mundos
#
# Primeira vez no computador:
#   uv tool install google-colab-cli        (ou: pip3 install google-colab-cli)
#   colab new --gpu T4 && colab stop        (abre o login Google uma vez: cole o código que aparecer)
#
# O que faz: liga uma VM com T4 → instala qwen-tts → envia roteiro.json e a voz do canal (canal/voz/) →
# roda ferramentas/colab/narrar_qwen3.py → baixa assets/voz/narracao-<slug>.zip → DESLIGA a VM (sempre).
# Se canal/voz/voz-rebobina.wav ainda não existe, a voz é criada lá e baixada para canal/voz/ (identidade do canal).
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
EP="$(cd "$1" && pwd)"
SLUG="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['slug'])" "$EP/roteiro.json")"
S="rebobina-$SLUG"
command -v colab >/dev/null || { echo "✗ Colab CLI não instalado: uv tool install google-colab-cli"; exit 1; }

trap 'colab stop -s "$S" >/dev/null 2>&1 || true' EXIT   # nunca deixa GPU ligada à toa
echo "▶ ligando GPU T4 no Colab (sessão $S)…"
colab new -s "$S" --gpu T4
colab install -s "$S" qwen-tts soundfile
echo 'import os; os.makedirs("/content/rebobina", exist_ok=True)' | colab exec -s "$S"
mkdir -p "$EP/assets/voz"
python3 "$RAIZ/ferramentas/pronuncia.py" "$EP/roteiro.json" "$EP/assets/voz/_roteiro_tts.json"   # dicionário do canal
colab upload -s "$S" "$EP/assets/voz/_roteiro_tts.json" /content/rebobina/roteiro.json
VOZ_NOVA=1
if [ -f "$RAIZ/canal/voz/voz-rebobina.wav" ] && [ -f "$RAIZ/canal/voz/voz-rebobina.txt" ]; then
  colab upload -s "$S" "$RAIZ/canal/voz/voz-rebobina.wav" /content/rebobina/voz-rebobina.wav
  colab upload -s "$S" "$RAIZ/canal/voz/voz-rebobina.txt" /content/rebobina/voz-rebobina.txt
  VOZ_NOVA=0
fi
echo "▶ narrando ($(python3 -c "import json,sys;print(len(json.load(open(sys.argv[1]))['cenas']))" "$EP/roteiro.json") cenas)…"
colab exec -s "$S" --timeout 2400 -f "$RAIZ/ferramentas/colab/narrar_qwen3.py" | tee /tmp/narrar_colab.log
grep -q NARRACAO_OK /tmp/narrar_colab.log || { echo "✗ a narração falhou no Colab (veja o log acima)"; exit 1; }
mkdir -p "$EP/assets/voz"
colab download -s "$S" /content/rebobina/narracao.zip "$EP/assets/voz/narracao-$SLUG.zip"
if [ "$VOZ_NOVA" = 1 ]; then
  mkdir -p "$RAIZ/canal/voz"
  colab download -s "$S" /content/rebobina/voz-rebobina.wav "$RAIZ/canal/voz/voz-rebobina.wav"
  colab download -s "$S" /content/rebobina/voz-rebobina.txt "$RAIZ/canal/voz/voz-rebobina.txt"
  echo "★ voz do canal criada e salva em canal/voz/ — ouça e, se não gostar, apague e rode de novo"
fi
echo "✓ $EP/assets/voz/narracao-$SLUG.zip"
