#!/usr/bin/env bash
# Chamado pelo hook StopFailure quando o limite de uso acaba: desliga VMs do Colab e suspende o Mac.
# Uso manual para testar sem suspender:  ferramentas/suspender_no_limite.sh --teste
LOG="$(cd "$(dirname "$0")/.." && pwd)/canal/.suspensao.log"
echo "$(date '+%F %T') limite de uso atingido" >> "$LOG"
for s in $(colab sessions 2>/dev/null | sed -n 's/^\[\([^]]*\)\].*/\1/p' | grep -v '^colab$'); do
  [ "${1:-}" = "--teste" ] && echo "pararia VM: $s" || colab stop -s "$s" >/dev/null 2>&1
done
[ "${1:-}" = "--teste" ] && { echo "suspenderia o Mac"; exit 0; }
sleep 20   # deixa a notificação do limite aparecer
pmset sleepnow
