# Rebobina — Identidade visual (frame.md)

Conceito: **uma fita VHS de arquivo sendo rebobinada até o momento em que a história aconteceu.**
O que é fixo é a "moldura da fita" (OSD, contador de ano, textura, legendas). O que varia é **tudo dentro dela**.

## Formato

- 1080 × 1920, 30 fps, vertical. Duração: 70–90 s (nunca < 65 s).
- Projeto HyperFrames: `index.html` (raiz) + `compositions/*.html` (uma cena por arquivo).

## Zonas seguras (TikTok + Shorts)

```
y 0–168      ███ proibido: barra de status/busca do app
y 168–300    OSD: ▶ PLAY / contador de ano            (texto pequeno permitido)
y 300–1060   PALCO: o visual principal da cena
y 1080–1320  LEGENDAS (centro em y≈1200)
y 1330–1920  ███ só textura/decoração: legenda do post, @, botões
x > 940 entre y 700–1600  ███ trilho de botões (curtir, comentar) — sem texto
```

Coluna de texto: **x 90 → 930** (840 px). Títulos podem usar até x 990 acima de y 700.

## Paleta (tokens em `assets/rebobina.css`)

| Token | Hex | Uso |
|---|---|---|
| `--fita` | `#0E0D10` | fundo padrão |
| `--fita-2` | `#1C1A22` | painéis, cartões escuros |
| `--papel` | `#F1E8D3` | documentos, texto claro principal |
| `--tinta` | `#1B1A17` | texto sobre papel |
| `--rec` | `#FF3B30` | carimbos, ponto REC, "MITO", riscos |
| `--vhs` | `#FFD23F` | palavra ativa da legenda, números-chave |
| `--tela-azul` | `#2335D9` | tela azul de VHS (transição de era) |
| `--acento` | por vídeo | 1 cor de acento escolhida por episódio (mapas, destaques). Registrar no histórico; não repetir nos 3 últimos. |

Sugestões de acento: `#2FBF71` verde-mata · `#3FA7FF` azul-rio · `#E07A3B` terracota · `#B48CFF` lilás · `#4FD1C5` ciano · `#E8B04B` ouro-velho.

## Tipografia (arquivos em `assets/fonts/`, sempre via `@font-face`)

| Papel | Fonte | Tamanho | Regras |
|---|---|---|---|
| Título/impacto | League Gothic | 150–280 px | MAIÚSCULAS, line-height .9, no máx. 4 palavras por linha |
| OSD e números técnicos | Space Mono 700 | 40–56 px | contador, datas, "◀◀ REW" |
| Documentos, fichas, recibos | Special Elite | 40–60 px | texto "datilografado" sobre `--papel` |
| Jornal antigo (mastro, manchete) | Playfair Display 900 | 60–160 px | só em cenas de jornal/imprensa; nunca imitar o logotipo real de um jornal |
| Legendas | Montserrat 900 | 64–80 px | maiúsculas, contorno preto 10 px (paint-order), palavra ativa em `--vhs` |

Nada que precise ser lido abaixo de 36 px.

## Elementos fixos (a "fita")

1. **OSD superior** (sempre visível): à esquerda `▶ PLAY` com ponto vermelho piscando em passos (não suave); à direita o **contador de ano** em Space Mono (`1867`). Quando a história muda de era, o contador **rola** até o novo ano (efeito rebobinar).
2. **Textura**: scanlines horizontais fixas (opacidade 0.08), grão animado em passos de 2 frames (opacidade 0.10), vinheta nas bordas.
3. **Transição de era — "rebobinar"** (0.5–0.7 s): faixas de ruído de tracking varrem a tela, a imagem treme na horizontal, o OSD mostra `◀◀ REW`, o contador rola. Usar **só** quando o ano muda (2 a 4 vezes por vídeo).
4. **Legendas** queimadas, 3–5 palavras por grupo, um grupo por vez.
5. **Fecho**: tela azul VHS por 0.4 s + `■ STOP` no OSD no último segundo (assinatura de saída). Sem cartão de logo.

## Movimento

- Cortes secos na palavra que nomeia a coisa nova. Tremidinha de 2 frames (x ±6 px) no corte.
- Entradas rápidas: 0.18–0.30 s, `power3.out`. Nada de fade lento genérico.
- Documentos: texto aparece datilografado (passos), carimbos batem (escala 1.5 → 1, rotação −8°, `back.out(2)`, 0.16 s).
- Contadores e números: rolam em passos (como contador de fita), não interpolação suave.
- Mapas: traçado do contorno + preenchimento que "escorre" da cor antiga para a nova.
- Em toda cena, algo se move pelo menos a cada 2–3 s (sem trechos mortos).

## Proibido (cara de template / IA genérica)

- Ícones dentro de círculos, três cartões lado a lado, slides de bullet points.
- Fade-in de opacidade como única animação.
- Gradientes roxo-azul "de startup", glassmorphism.
- Fotos de banco de imagem, rostos gerados por IA, imagens de pessoas reais baixadas da web.
- Logo ou nome do canal no frame 0.
- O mesmo layout de cena em dois vídeos seguidos.

## Frame 0

O frame 0 é o que aparece no feed e a reserva da capa: **a frase do gancho em League Gothic gigante + o objeto-símbolo** do episódio (ex.: cavalo de xadrez ♞), já na tela. Nunca preto, nunca logo.

## Capa

Imagem própria gerada por `ferramentas/capa.py` a partir do campo `capa` do roteiro, com a moldura da fita e sem legenda. Precisa dizer do que é o vídeo para quem a vê na grade do perfil, sem som. Sem legenda, o palco da capa vai até y 1320.
