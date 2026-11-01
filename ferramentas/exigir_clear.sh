#!/usr/bin/env bash
# Hook UserPromptSubmit: barra /novo-video em conversa longa, porque cada mensagem relê o histórico e encarece o vídeo.
# O Claude Code não deixa um comando rodar /clear sozinho. Para seguir sem limpar: /novo-video sem clear [tema]
python3 -c '
import json, os, sys
d = json.load(sys.stdin)
p = d.get("prompt", "").strip()
if not p.startswith("/novo-video") or "sem clear" in p:
    sys.exit(0)
t = d.get("transcript_path") or ""
if os.path.exists(t) and os.path.getsize(t) > 200_000:
    print("Conversa longa: rode /clear e mande /novo-video de novo. Para seguir assim mesmo: /novo-video sem clear", file=sys.stderr)
    sys.exit(2)
'
