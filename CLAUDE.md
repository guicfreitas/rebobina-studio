# Rebobina — canal dark de história (TikTok + YouTube Shorts)

Projeto de produção automatizada de vídeos verticais de 70–90 s sobre acontecimentos históricos,
em PT-BR, feitos em **HyperFrames** (HTML/GSAP → MP4). O dono é o Guilherme; a publicação é
semiautomática (ele aperta "Publicar").

## Fontes de verdade
- `canal/BIBLIA.md` — o que é o canal, pautas permitidas, regras de plataforma (duração!), estrutura de roteiro.
- `canal/DESIGN.md` — identidade visual VHS, zonas seguras, tipografia, movimento, proibições.
- `canal/historico.json` — vídeos publicados. `canal/metricas.json` — desempenho deles. `canal/pautas.md` — fitas prometidas e ideias pedidas com `/pautas`; o pesquisador não escolhe dele.

## Pipeline e agentes (`.claude/agents/`)
| Etapa | Agente | Entrega |
|---|---|---|
| 0 | `pesquisador-pautas` (só sem tema) | `canal/pesquisas/AAAA-MM-DD-slug.md` (tema vencedor com evidências) |
| 1 | `roteirista` | `episodios/NNN-slug/roteiro.json` (falas, telas, formas, fatos com fontes) |
| 2 | `revisor-roteiro` | `REVISAO-ROTEIRO.md` (APROVADO/REPROVADO) |
| 3 | `animador` | narração, `compositions/*.html`, `render/rascunho.mp4` |
| 4 | `revisor-frames` | `revisao/` (métricas + folhas de frames), `REVISAO-FRAMES.md` |
| 5 | `publicador` | `render/final.mp4`, `publicacao.json`, pasta `publicar/` |

Comandos: `/novo-video [tema]` (tudo, com 2 paradas para aprovação; "sem paradas" pula),
`/pautas [n]`, `/publicar episodios/NNN-slug`.

## Ferramentas (`ferramentas/`, rode da raiz)
- `novo_episodio.py <slug>` — cria a pasta do episódio.
- `narrar.py <ep> [--motor arquivos|kokoro|elevenlabs|gravacao]` — voz + `tempos.json` (tempo de cada palavra).
  `colab` (padrão) = Qwen3-TTS numa GPU T4 do Google Colab via Colab CLI (`narrar_colab.sh`: liga, narra, baixa, desliga);
  `arquivos` = faixas por cena prontas (ex.: do notebook `ferramentas/colab/narracao_qwen3.ipynb`). Voz fixa em `canal/voz/`: clone da gravação do Guilherme (`voz-rebobina.wav` + `.txt`); o texto lido está em `GRAVACAO.md`.
- `canal/pronuncia.json` — dicionário de pronúncia do canal, aplicado sozinho pelo `narrar.py`. `testar_pronuncia.sh` gera amostras de grafias com a voz do canal e `pagina_pronuncia.py` monta a página para escolher de ouvido.
- `musica.py --buscar "<clima>"` / `musica.py <ep> "<título>"` — trilha do catálogo incompetech (CC BY 4.0) com volume que abaixa na fala; rode depois do `narrar.py`. Não repita a faixa do vídeo anterior (`historico.json`). O crédito entra sozinho nas descrições.
- `sfx.py <ep>` — mistura os efeitos sonoros de `sfx.json`, cada um preso a uma palavra ou cena; sons em `canal/sfx/`.
- `montar.py <ep>` — gera `index.html`, OSD, efeitos, legendas e rascunhos de cena. **Arquivos gerados não se editam à mão.**
- `mapa.mjs` — mapas SVG com dados reais (Natural Earth/IBGE). `inserir.py <ep>` — injeta SVGs nas cenas.
- `checar_roteiro.py <ep>` — checagem automática antes do revisor de roteiro (palavras, frases, tela, formas, capa, fontes, variedade contra os episódios anteriores).
- `sinais.py "<termo>" …` / `sinais.py --descobrir` — procura real, sem chave: autocomplete do YouTube no Brasil, views da Wikipédia pt, vídeos concorrentes.
- `metricas.py [--ler]` / `metricas.py --manual <id> <plataforma> views=… retencao=…` — desempenho em `canal/metricas.json`; confere o título publicado. TikTok e retenção podem precisar do `--manual`.
- `capa.py <ep>` — capa própria a partir do campo `capa` do roteiro (`capa/capa.jpg`, usada pelo pacote).
- `checar_video.py <ep> [mp4]` — checagem automática antes da revisão de frames (clipes, efeitos, zonas, palco parado).
- `renderizar.sh <ep> [rascunho|final]` · `revisar_video.py <ep> [mp4]` · `pacote_publicacao.py <ep> [--publicado …]`.

## Economia de tokens
Cada vídeo em sessão nova: `/clear` antes de `/novo-video` (um hook lembra). Relatórios de agente curtos, detalhe nos arquivos. Erros repetidos entram em `canal/LICOES.md`.

## Regras que não se quebram
- Vídeo final **> 65 s** (o TikTok só paga acima de 60 s) e ≤ 120 s; ideal 70–90 s.
- Todo fato na fala ou na tela tem 2+ fontes em `roteiro.json`.
- Variedade entre vídeos (política de "conteúdo inautêntico" do YouTube): identidade fixa, cenas sempre novas.
- Sem rede no render (GSAP e fontes estão em `assets/`), sem `Math.random`/`Date.now`, sem fotos de pessoas reais.
- O agente publicador nunca clica em Publicar.
- Linux sem Chrome do HyperFrames: `export HYPERFRAMES_BROWSER_PATH=<chrome-headless-shell>`; no Mac basta `npx hyperframes browser ensure`.
