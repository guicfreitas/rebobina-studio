# Revisão de roteiro — 004-guerra-dos-emus — rodada 3
VEREDITO: APROVADO
Palavras: 201 · duração estimada: 76,9 s pela fórmula do roteirista (160 pal/min + 1,5 s); 82 a 84 s só de fala pelo ritmo medido na voz atual (143 a 147 pal/min em 002 e 003). Sem `tempos.json`.

Rodada restrita à aplicação das correções da rodada 2. Fontes reabertas só para f13 e f15.

## Problemas
Nenhum P0 ou P1. Os três P2 abaixo não impedem o animador.

- P2 · c12 · tela · "RECOMPENSAS POR EMU: 57.034" não diz que são pedidos, ao contrário da fala e de f13. O áudio cobre, mas a tela sozinha pode ser lida como recompensas pagas. → opcional: "PEDIDOS DE RECOMPENSA: 57.034" (4 palavras).
- P2 · f13 · fontes · a afirmação cita a Australian Geographic, mas a URL dela não está na lista de f13. → acrescentar https://www.australiangeographic.com.au/topics/wildlife/2016/10/australias-emu-wars/ ou tirar a menção.
- P2 · `canal/historico.json` · o episódio 001 segue sem registro (item da rodada 1, fora do roteiro).

## Pontos pedidos nesta rodada
- **f15 · basta.** O alt text "A kangaroo and an emu holding up a shield." está no HTML, na imagem de destaque da página. Baixei a imagem: mostra canguru e emu apoiando o escudo, a estrela de sete pontas e o lema "ADVANCE AUSTRALIA". O texto da página dá a concessão de 7/5/1908 e o crédito SP 929.6 C 734D, da State Library of South Australia. Quem sustenta o emu aqui é a imagem da peça, mais do que a descrição. A Wikipedia dá os apoios de 1908 ("a kangaroo and an emu using its foot to help the kangaroo to support the shield", detalhe visível na imagem) e cita o brasonamento da Commonwealth of Australia Gazette nº 39, 8/8/1908, p. 1181: "a Kangaroo, to the sinster an Emu". Não li a Gazette; ela conta como referência da Wikipedia, não como terceira fonte lida. O P1 da rodada 2 está resolvido, e a tela "BRASÃO · DESDE 1908" fica sustentada por duas fontes.
- **f13/c12 · redação certa.** "Pedidos de recompensa por emu" traduz "bounties were claimed" (Wikipedia) e "farmers managed to claim 57,034 bounties" (History Hit). Seis meses de 1934 confere nas duas. A ressalva da rodada 2 continua: as fontes podem derivar umas das outras.
- **201 palavras · sem problema.** O limite é 170 a 210 em `canal/BIBLIA.md` e no `roteirista`, e o P1 deste revisor só começa acima de 230. O 200 era só referência de duração. A palavra a mais veio da correção opcional da c12, e aceito a troca.
- **Deixa da c12 · correta.** "recompensa" está na fala e no `fala_tts`, então a deixa do `visual` existe. Nenhuma outra deixa da cena depende da palavra antiga.

## Decisões de duração (atualizadas)
Estimativas a 140 pal/min. Valem como exceção, e os tetos se conferem no `tempos.json`:
- c14 (27 palavras, cerca de 11,5 s): aceita. Teto: 12,5 s.
- c12 (agora 22 palavras, cerca de 9,4 s a 140 pal/min; 9,0 a 9,2 s no ritmo medido; limite de 8 s): aceita, com folga menor que na rodada 2. Teto mantido: 9,5 s. Se passar, tirar "só": "Em seis meses de mil novecentos e trinta e quatro."
- c01 (10 palavras, 4,3 s): aceita. Teto: fim da fala em 4,6 s. Acima disso, usar "Três homens com metralhadoras perderam para uma ave?" e mover a deixa de 'guerra' para 'perderam'.

c10, data e "até agora": ficam como estão (ver a decisão da rodada 2; o aparte de James e Green é registro de imprensa, ressalvado em f11).

## Correções da rodada 2
- P0 c05 ✓ `fala`, `fala_tts`, `tela` e `visual` iguais ao texto pedido
- P0 f6 ✓ afirmação substituída; as duas URLs novas estão nas fontes
- P1 f15 ✓ ANBG retirada; Centre of Democracy no lugar (APH e AWM seguem sem leitura, como f15 declara)
- P1 c14 ✓ deixas de 'atirou' e 'história' acrescentadas
- P2 c14 ✓ `marcos_ano`: `montar.py` usa a primeira ocorrência da palavra, então 2026 cai em "está no brasão"
- P2 c12 ✓ redação aplicada, com `fala_tts` coerente
- P2 f11 ✓ Hansard de 8/11/1932 acrescentado
- P2 f16 ✓ "citando o Nungarin Standard"
- P2 001 no histórico ✗ fora do roteiro

## Fatos conferidos
- f13 ✓ reaberto nesta rodada (Wikipedia, History Hit)
- f15 ✓ reaberto nesta rodada (Centre of Democracy, Wikipedia)
- f6 ✓ reescrito conforme a rodada 2, que conferiu os Hansards
- Demais fatos não reabertos: valem as conferências das rodadas 1 e 2 (f1–f5, f7–f12, f14, f16)

Limites: APH, AWM e Museums Victoria seguem sem leitura (403 nas rodadas anteriores e, para Museums Victoria, nesta); as páginas de pmc.gov.au vieram vazias. Não li Johnson (2006) nem Boom and Bust.

## Conferido sem problema
- Estrutura, nesta rodada: 14 cenas, frases ≤ 14 palavras, telas com ≤ 5 palavras/linha e ≤ 4 linhas.
- Variedade, plataformas e voz: sem mudança desde a rodada 2; "tópa" e "emú" presentes nas falas alteradas.

## Pontos fortes (não mexer)
- c02 "Parece lenda de internet. Mas tem data, major e relatório."
- c09 e a citação real sobre os tanques.
- c10: a frase de 1932 com o "até agora" recuperado.
- A virada c11–c12, 986 contra 57.034 pedidos, mantendo "conta do major".
- O fecho do brasão com "entrou para a história como perdedor".
