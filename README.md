# ◀◀ Rebobina

Canal dark de acontecimentos históricos para TikTok e YouTube Shorts, produzido por uma equipe de
agentes do Claude Code e renderizado com [HyperFrames](https://github.com/heygen-com/hyperframes).

## Instalação (macOS, uma vez)

```bash
brew install node@22 ffmpeg espeak-ng          # espeak-ng: pronúncia em português da voz Kokoro
brew install whisper-cpp                         # opcional: mede o tempo real de cada palavra (legendas mais precisas; obrigatório para usar sua voz)
pip3 install kokoro-onnx soundfile               # voz local grátis
cd ferramentas && npm install && cd ..           # mapas (d3-geo), fontes e GSAP
npx hyperframes browser ensure                   # Chrome usado no render
npx hyperframes skills update                    # skills do HyperFrames para o Claude Code
uv tool install google-colab-cli                 # Colab CLI oficial (ou: pip3 install google-colab-cli)
colab new --gpu T4 && colab stop                 # login Google uma única vez (cole o código que aparecer)
```

Na primeira narração, o modelo Kokoro (~330 MB) é baixado automaticamente.

## Fazer um vídeo

```bash
cd rebobina
claude
> /novo-video                         # o roteirista escolhe a pauta
> /novo-video a Guerra dos Emus       # ou você escolhe o tema
> /novo-video Napoleão era baixinho? sem paradas
```

O fluxo para duas vezes para você aprovar: o **roteiro** (barato de mudar) e o **vídeo** (antes
do render final). No fim você recebe `episodios/NNN-slug/publicar/` com o vídeo, a capa, os
textos de TikTok e YouTube e um checklist. Você posta pelo app; depois, cole os links:

```bash
python3 ferramentas/pacote_publicacao.py episodios/NNN-slug --publicado tiktok=<link> youtube=<link>
```

## Narração

A voz do canal fica em `canal/voz/voz-rebobina.wav` + `voz-rebobina.txt`. Ela é criada sozinha na primeira narração (o script avisa com ★): ouça; se não gostar, apague os dois arquivos e narre de novo para sortear outra. Depois disso, todo episódio usa a mesma voz.


| Motor | Como ativar | Observação |
|---|---|---|
| **Qwen3-TTS no Google Colab (padrão)** | `"motor_voz": "colab"` | grátis, voz natural e fixa do canal. **Automático**: o `narrar.py` usa o Colab CLI para ligar uma GPU T4, narrar, baixar e desligar (`ferramentas/narrar_colab.sh`). Sem terminal? Use o notebook `ferramentas/colab/narracao_qwen3.ipynb` e `"motor_voz": "arquivos"` |
| Kokoro (reserva) | `"motor_voz": "kokoro"` no roteiro | grátis, local, roda no Mac Intel, voz `pm_alex` mais robótica |
| Sua voz | grave o roteiro inteiro em `episodios/NNN/assets/voz/gravacao.m4a` e use `"motor_voz": "gravacao"` | precisa do whisper-cpp; o resto é automático |
| ElevenLabs | `.env` com `ELEVENLABS_API_KEY` e `ELEVENLABS_VOICE_ID`, `"motor_voz": "elevenlabs"` | pago, mais natural |

Música: escolha na biblioteca de sons do TikTok/YouTube na hora de postar (volume baixo). Assim não há risco de direitos autorais.

## Estrutura

```
canal/            BIBLIA.md · DESIGN.md · pautas.md · historico.json · marca/ (fotos de perfil + fonte HTML)
.claude/agents/   roteirista · revisor-roteiro · animador · revisor-frames · publicador
.claude/commands/ novo-video · pautas · publicar
ferramentas/      narrar · montar · mapa · inserir · renderizar · revisar_video · pacote_publicacao · checar_roteiro · sinais · metricas · capa
templates/        base-video (fontes, GSAP, CSS, símbolos)
episodios/        001-acre-cavalo (piloto) …
```

## Créditos de dados e fontes
Mapas: Natural Earth (domínio público) via `world-atlas`; estados do Brasil (IBGE) via click_that_hood.
Fontes tipográficas: League Gothic, Space Mono, Special Elite, Montserrat (SIL OFL). Símbolo do cavalo:
glifo da DejaVu Sans (licença livre). Voz: Kokoro-82M (Apache 2.0).

## Licenças de mídia

Sem arquivo de licença, o código e os vídeos deste repositório não têm permissão de reuso. As exceções são os materiais de terceiros:
as trilhas são de Kevin MacLeod (incompetech.com), sob CC BY 4.0, com o crédito em `musica.json` de cada episódio; os efeitos têm autor e licença em `canal/sfx/fontes.json`.
Os efeitos sob licença Pixabay não estão no repositório: baixe pelas páginas listadas nesse arquivo antes de rodar `ferramentas/sfx.py`.
A voz em `canal/voz/` é do dono do canal e não está liberada para clonagem.
