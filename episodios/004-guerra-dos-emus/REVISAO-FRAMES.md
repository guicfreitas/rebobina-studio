# Revisão frame a frame — 004-guerra-dos-emus — rodada 2
VEREDITO: APROVADO (0 P0, 1 P1; a voz ainda precisa ser ouvida por uma pessoa)
Duração 89,8 s · 1080x1920 · 30 fps · −15,2 LUFS · pico −1,5 dBTP · check sem erros (1 aviso: legendas.html longo, gerado; 51 `line_unread`, todos dos dígitos rolando na c11, efeito intencional)

## Problemas

### P0
Nenhum.

### P1
- P1 · t=48,70–63,17 s · c10 · 14,47 s sem nenhum efeito, 3,2 vezes a média (4,46 s), e o trecho inclui a piada da medalha. Na imagem não incomoda: o palco nunca fica mais de 1,5 s sem mudar, e a trilha segue constante (−30,8 dB RMS, contra −31,6 antes e −30,7 depois). No som, a queda da medalha no peito fica muda, e a rodada 1 mandava manter um efeito ali → acrescentar em `sfx.json` `{"som":"clique","cena":"c10","palavra":"emus","desloca":0.06,"volume":0.3}`; a medalha cai entre 54,73 e 54,87 s. O vão se divide em 6,1 s e 8,3 s · manter os outros 20 efeitos, que estão em sincronia

### P2
- P2 · t=0 · c01 · a cabeça do emu ainda encosta no "S" de "METRALHADORAS" (item da rodada 1, sem mudança) → descer o emu 15 px
- P2 · t=36–38 s · c07 · alguns pontos dourados entram no "S" de "EMUS", da mesma cor → recuar o arco superior 20 px ou escurecer os pontos atrás do texto · manter a divisória em x=600
- P2 · t=48,7–49,4 s · c09 · a ponta do canhão e a lateral do tanque (x≈940–985, y≈890–935) ficam sob o trilho de botões. É desenho, não texto → reduzir o tanque em 8% ou recuá-lo 45 px
- P2 · t=79,0–81,2 s · c14 · um traço de ~2×14 px em (120, 459), início do desenho do escudo, aparece cerca de 2 s antes da hora. Quase invisível → esconder o escudo até o traçado começar
- P2 · t=69,94 s · c12 · `tempos.json` põe "emu" 0,2 s depois da voz, que começa em ≈69,74 s (item da rodada 1, sem mudança; dentro da tolerância) → corrigir o tempo, se a palavra for medida de novo
- P2 · c06, c10, c12 · a voz fica cerca de 2 dB abaixo das cenas vizinhas (−16,3 a −16,5 dB RMS ativo; c05 −14,3, c07 −14,7). Toda cena tem pico igual (0,84), então o nível parece igualado por pico → ouvir a passagem c05→c06→c07; se notar o degrau, igualar por loudness
- P2 · t=88,3 s · trilha · depois do fim da voz (87,68 s) a trilha fica em −46 dB e sobe para −30 dB numa nota isolada, antes de o fade terminar. Sem corte nem rajada: os últimos 60 ms têm pico de 0,0001 → ouvir; se a nota soar solta, encurtar o fade ou trocar o trecho
- P2 · doc · `roteiro.json` · o campo `visual` ainda pede sons que saíram (papel, moeda, tilintar, sineta, arame, página) → alinhar o texto ou deixar anotado que `sfx.json` manda

## Pontos pedidos
- **c04 lê-se como trigo e cerca: sim.** Sem legenda, um estranho vê espigas atrás de uma cerca de mourões e três fios. A maré vem da direita ("~20.000 EMUS" diz o que é), a cerca rompe em três trechos, as espigas atrás escurecem e os pontos atravessam. Rupturas em ≈20,92, 21,29 e 21,66 s, na fala "furam as cercas". P0 da rodada 1 resolvido. Ressalvas sem peso: a maré é uma faixa de bordas retas e tem o mesmo dourado do trigo.
- **Sincronia dos 20 efeitos: todos dentro de ±0,1 s** (tabela abaixo).
- **"major":** resolvido na transcrição. c02: 5 de 6 versões saem "major" (na rodada 1, "maior" em 4 de 4); a exceção é a narração inteira, "maior". c06: 6 de 6 (na rodada 1, "uma joa" em 3 de 4). Falta ouvir.
- **"Meredith":** o transcritor grafa "Meridith" em 5 de 6 e "Merid" em 1. A legenda está boa. Pela análise espectral, o /m/ começa em ≈29,54 s e a voz acaba em ≈30,19 s; o quadro "MEREDITH" fica de 29,63 a 30,33 s, com destaque em 29,69 s. Ou seja, entra 0,09 s depois do início da palavra e sai 0,14 s depois do fim. A estimativa de `tempos.json` atrasa cerca de 0,15 s (margem de ±0,05 s, sem ouvido): "O" fica destacado durante o começo de "major". Não dá para perceber.
- **"cinegrafista":** certo em 4 de 6; nas outras 2, "cine grafista", só separação do transcritor. Sumiu o "sunegrafista" da rodada 1.
- **"Partem,":** a pausa mede 0,31 s (28,81→29,12 s; na rodada 1, 0,08 s). É parecida com as outras vírgulas (0,24–0,41 s; 0,34 s depois de "Meredith"). Se soa natural, só de ouvido.
- **Volume +1 LU: vem da proteção de pico do HyperFrames, não da trilha.** Antes da proteção o nível é o mesmo: −13,45 LUFS na rodada 1 (−16,3 + 2,85) e −13,49 agora (−15,2 + 1,71). O que mudou foi a atenuação, de 2,85 dB para 1,71 dB, uma diferença de 1,14 dB. O novo loudnorm subiu a trilha 0,8 LU no arquivo e os efeitos 0,9 LU, mas sob a voz isso quase não muda a soma. A queda do pico da soma para +0,2 dBFS deve vir dos efeitos que saíram ou baixaram; não dá para provar, porque as faixas da rodada 1 não existem mais.
- **Ganho ×0,72: vem do HyperFrames e afeta as três faixas por igual.** Em hyperframes 0.8.226, `enforceAacTruePeak` (`dist/chunk-BJ3Q3XK7.js`) mede o AAC; acima de −1 dBTP, recodifica o arquivo inteiro com ganho constante até −1,5 dBTP. A conta bate: reproduzi a mix do HyperFrames sem essa etapa e deu pico de +0,2 dBFS (−0,3 depois do AAC), o que exige −1,7 dB = ×0,822. Medi ×0,821 no render. Não vi o log do render; a atribuição vem do código e dessa conta. É ganho, não limitador: não distorce nem muda o equilíbrio entre as faixas.
- **Correção da rodada 1:** a tabela com "voz ×1,02, trilha e efeitos ×0,72" estava errada. O 1,02 veio do meu downmix para mono, que multiplicou a voz por √2. Canal a canal, a voz também era ×0,72, valor que deduzi agora, sem refazer a medição. Hoje as três estão em ×0,82.
- **Consequência:** a voz sai de `narrar.py` com pico em −1,5 dBFS, então qualquer efeito somado passa de −1 dBTP e a proteção dispara. O volume final depende do pior pico da soma: +0,18 dB em 81,26 s (tique sobre "brasão") e +0,07 dB em 6,34 s (carimbo sobre "Mas"). Ele pode mudar a cada ajuste de efeito; está dentro do alvo (−16 a −14). Conferir de novo no `final.mp4`, que eu não medi nesta rodada.

## Efeitos
Início = começo audível do som (−40 dB) menos a deixa. Imagem = primeira mudança, ou pico, medido no palco ou no OSD, menos a deixa. S/V = efeito menos voz no pico do efeito, nos ±25 ms em volta.

| t (s) | Cena | Som → ação | Início | Imagem | S/V (dB) |
|---|---|---|---|---|---|
| 2,52 | c01 | tique → pontos | +0,01 | +0,01 | −6,2 |
| 6,27 | c02 | carimbo → FATO | +0,03 | +0,03 | −5,6 |
| 9,16 | c03 | vhs → REW no OSD | +0,01 | +0,01 | −22,3 |
| 16,47 | c03 | tique → linha de preço | +0,01 | 0,00 | −7,5 |
| 23,39 | c05 | máquina → recibo sobe | +0,01 | −0,06 | −19,8 |
| 26,96 | c05 | carimbo → DEFESA NÃO PAGA | +0,03 | pico +0,04 | +18,4 (fechamento do "p") |
| 31,82 | c06 | clique → clipe | +0,01 | +0,01 | −3,9 |
| 37,25 | c07 | tiro → pontos apagam | +0,01 | +0,02 | −1,3 |
| 37,81 | c07 | clique → TRAVADA | +0,01 | +0,02 | −1,3 |
| 41,19 | c08 | tique → casa "2" | +0,01 | +0,01 | +2,2 |
| 43,16 | c08 | carimbo → RECUO | +0,03 | pico +0,07 | −9,2 |
| 48,70 | c09 | baque → emu = tanque | +0,01 | 0,00 | −4,3 |
| 63,17 | c11 | tique → trava 986 | +0,01 | +0,03 | −2,8 |
| 65,27 | c11 | tique → trava 9.860 | 0,00 | +0,03 | +2,2 |
| 69,36 | c12 | carimbo → fichas | +0,04 | queda contínua | −10,3 |
| 70,36 | c12 | carimbo → fim da coluna | +0,04 | +0,01 | +20,3 (pausa) |
| 78,13 | c13 | carimbo → NEGADO | +0,03 | pico +0,04 | −4,7 |
| 81,25 | c14 | tique → contador a 2026 | +0,01 | rola de −0,25 a +0,45 | −10,0 |
| 83,28 | c14 | clique → mira | +0,01 | +0,02 | −5,1 |
| 87,22 | c14 | clique → mira treme | +0,01 | +0,01 (leve; mira some em +0,41) | −5,3 |

Vãos acima de 6 s: 48,70→63,17 (14,47 s, ver P1); 70,36→78,13 (7,77 s); 9,16→16,47 (7,31 s); 16,47→23,39 (6,92 s). O último cobre a c04, cuja ruptura ficou muda. Não recomendo preencher com `clique`, que a rodada 1 já apontou como som errado para arame; o certo é um estalo de arame em `canal/sfx/`, se houver.

## Mix
| Faixa | LUFS no arquivo | Ganho na mix | LUFS na mix | Observação |
|---|---|---|---|---|
| Voz (mono; L=R na mix) | −16,4 (−13,4 como estéreo) | ×0,82 | −15,1 | sem mudança no arquivo |
| Trilha | −26,0 | ×0,82 | −27,7 | na rodada 1: −26,8 no arquivo, −29,7 na mix |
| Efeitos | −26,9 | ×0,82 | −28,6 | na rodada 1: −27,8 no arquivo, −30,7 na mix |
| Mix final | | | −15,2 | pico −1,5 dBTP |

A soma das 3 faixas reproduz o MP4 (correlação 0,9999, sem atraso, resíduo −39 dB). Em ambos os canais, voz e trilha dão ×0,821 e efeitos ×0,818–0,819. A voz ganhou 1,14 dB; a trilha, 1,94 dB, ou seja, 0,8 dB mais perto da voz.

## Itens da rodada 1
| Item | Estado |
|---|---|
| P0 c04: trigo e cerca | resolvido |
| 35 efeitos → 1 a cada 3–6 s | 20 efeitos, média de 4,46 s; restam 4 vãos acima de 6 s |
| `papel` com ataque lento (6 casos) e `pagina` c11 | saíram |
| `clique` da c04 | saiu; a ruptura ficou sem som |
| c10: tique, baque e clique no peito | os 3 saíram; o clique devia ficar → ver P1 |
| baque c09, volume 0,20 | feito; S/V de 0,0 para −4,3 dB |
| clique c06, volume 0,25 | feito; "sunegrafista" sumiu |
| carimbo c08: +0,12 s e volume 0,30 | feito |
| "major" c02 e c06 | melhorou na transcrição; falta ouvir |
| c02: cedilha e til | resolvido |
| c03: linha sobre "PREÇO" e contorno | resolvido; bloco e mapa sem colisão |
| c03: gráfico em painel "PREÇO DO TRIGO (ESQUEMA)" | resolvido |
| c03: polígono à mão | resolvido; virou mancha sem borda |
| f3 em `roteiro.json` | corrigido |
| c05: palco vazio e últimas linhas | resolvido; recibo cresce em "metralhadoras", "MUNIÇÃO" entra em "topa" |
| c07: divisória sobre o "S" | resolvido, x=600 |
| c08: bola dourada | resolvido; emu em silhueta |
| c08: carimbo cortado | resolvido |
| P2 c01: emu no "S" | sem mudança |
| P2 c02: "FATO" sobre "DA" | resolvido; "LENDA" apaga |
| P2 c09: aspas-fantasma | resolvido |
| P2 c10: plenário em semicírculo | resolvido; pontos em fileiras neutras |
| P2 c13: barras pretas | resolvido; barras cinzas |
| P2 c14: emu de costas para o escudo | resolvido |
| P2 fim da trilha | resolvido; termina em −66 dB (ver a nota em 88,3 s) |
| P2 tempo de "emu" c12 | sem mudança |

## Cena a cena
- c01: "3 HOMENS", "2 METRALHADORAS", "~20.000 EMUS", 3 pontos vermelhos e emu branco; em "guerra", milhares de pontos dourados. Capa ok ✓
- c02: papel "LENDA de internet?" recebe o carimbo vermelho "FATO"; depois data, "OPERAÇÃO MILITAR" e folha "AUSTRÁLIA" ✓
- c03: rebobina até 1932, contorno da Austrália, oeste colorido, ponto com rótulo CAMPION, mancha dourada, painel de preço em degraus, "SUBSÍDIO PROMETIDO: NÃO VEIO" ✓ Muito texto no fim, mas legível.
- c04: espigas atrás da cerca, faixa de pontos dourados, cerca rompida em três trechos, "CERCAS ABERTAS" ✓
- c05: máquina de escrever com recibo que cresce, 4 linhas e carimbo "DEFESA NÃO PAGA" ✓
- c06: ficha com silhueta vazia, "MAJ. G.P.W. MEREDITH", "+ 2 MILITARES", "+ 1 CINEGRAFISTA", rolo de filme e clipe ✓
- c07: mira, represa azul, pontos em volta, "4 NOV 1932", "~1.000 EMUS", "METRALHADORA: TRAVADA", tela dividida com os pontos se espalhando; sem sangue nem queda ✓
- c08: caminhão em traço, linha de mira tremendo, emu dourado, casas de 2 a 8, "CHEGADA", "TRAVOU", carimbo RECUO ✓
- c09: pôster dourado, "MAJ. MEREDITH", rajada tracejada, citação, emu = tanque ✓
- c10: fileiras de pontos, "?", medalha girando que cai no peito do emu, citação, cordas de ringue ✓
- c11: página com 2 contadores que travam em 986 e 9.860; sem aves ✓
- c12: 986 encolhe; 57.034, "PEDIDOS DE RECOMPENSA:", coluna de fichas até y=300, "6 MESES DE 1934", sem invadir o OSD ✓
- c13: ofício "FAZENDEIROS PEDEM: O EXÉRCITO, DE NOVO", barras cinzas, "1934:", carimbo NEGADO ✓
- c14: emu com medalha virado para o escudo genérico, "BRASÃO · DESDE 1908", contador 1908 → 2026, mira sem tiro, "EMU: AINDA LÁ"; ■ STOP de ≈88,9 a ≈89,35 s e azul pleno até 89,8 s ✓

Conferidos sem problema: texto de todas as cenas contra `tela` e fatos; texto fora do trilho direito; legendas; contador de ano (2026, 1932, 1934, 1908, 2026); REW na c03 e c14, FF na c12 e c14.

## Não verificado
- **Áudio:** não ouço, só medi. Conferir de ouvido: "major" (c02, c06), "Meredith" (c06, sai "Meridith"), a pausa de "Partem,", "recuar" ("recordar" nas 2 transcrições do vídeo inteiro, certo nas 3 isoladas), "por emu" ("emum" em 2 de 2), "o emu está" ("emus" em 2 de 2), "Num caminhão" ("Nunca minhão" nas 3 isoladas), "rounds", "represa", "topa", "plantam trigo" ("um trigo" na mix), o degrau de voz na c06 e a nota em 88,3 s.
- **Transcrição não prova pronúncia.** 6 versões com whisper small por frase: bruta, cortada, trecho da narração, trecho da mix, narração inteira e mix inteira.
- **Timbre dos efeitos:** julguei só pelo envelope medido.
- **Causa da queda do pico da soma:** as faixas da rodada 1 não existem mais; os −2,85 dB dessa rodada foram deduzidos do ×0,72 registrado.
- **Frames:** vi folhas a 2 frames/s, frames-chave e 4 montagens de trechos; os demais quadros entraram só na medição de diferença entre quadros.
- **Layout contra episódios anteriores:** não comparei imagens.
- **Limites do trigo em 1932:** a mancha não afirma borda, mas segue sem fonte.
- **`final.mp4`:** não existe nesta rodada; volume e pico precisam ser medidos de novo nele.
