#!/usr/bin/env bash
# Gera amostras de cada grafia candidata com a voz do canal, numa GPU T4 do Colab, para escolher de ouvido.
# Uso:  ferramentas/testar_pronuncia.sh [candidatos.json]    (padrão: canal/voz/pronuncia-teste/candidatos.json, começa do zero)
# Saída: canal/voz/pronuncia-teste/audio/<id>-<n>.mp3. A grafia escolhida vai para canal/pronuncia.json.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
PASTA="$RAIZ/canal/voz/pronuncia-teste"
CAND="${1:-$PASTA/candidatos.json}"
S="rebobina-pronuncia"
trap 'colab stop -s "$S" >/dev/null 2>&1 || true' EXIT
colab new -s "$S" --gpu T4
colab install -s "$S" qwen-tts soundfile
echo 'import os; os.makedirs("/content/rebobina", exist_ok=True)' | colab exec -s "$S" --timeout 60
colab upload -s "$S" "$CAND" /content/rebobina/candidatos.json
colab upload -s "$S" "$RAIZ/canal/voz/voz-rebobina.wav" /content/rebobina/voz-rebobina.wav
colab upload -s "$S" "$RAIZ/canal/voz/voz-rebobina.txt" /content/rebobina/voz-rebobina.txt
LOG="$PASTA/teste.log"
colab exec -s "$S" --timeout 2400 -f "$RAIZ/ferramentas/colab/testar_pronuncia.py" | tee "$LOG"
grep -q TESTE_OK "$LOG" || { echo "✗ o teste falhou no Colab (veja $LOG)"; exit 1; }
colab download -s "$S" /content/rebobina/teste.zip "$PASTA/teste.zip"
[ $# -ge 1 ] || rm -rf "$PASTA/audio"   # com arquivo próprio, acrescenta às amostras da rodada
mkdir -p "$PASTA/audio"
unzip -q -o "$PASTA/teste.zip" -d "$PASTA/audio"; rm "$PASTA/teste.zip"
for f in "$PASTA"/audio/*.wav; do
  ffmpeg -y -v error -i "$f" -af "loudnorm=I=-16:TP=-1.5" -ac 1 -ar 44100 -b:a 64k "${f%.wav}.mp3" && rm "$f"
done
echo "✓ $(ls "$PASTA/audio" | wc -l | tr -d ' ') amostras em $PASTA/audio"
