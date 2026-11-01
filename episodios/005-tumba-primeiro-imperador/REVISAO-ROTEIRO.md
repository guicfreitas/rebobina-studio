# Revisão de roteiro — 005-tumba-primeiro-imperador — rodada 3
VEREDITO: APROVADO
Palavras: 195 · duração estimada: 83,0 s (2,35 palavras/s); sem `tempos.json`.

Escopo desta rodada: só a aplicação das correções da rodada 2. As fontes não foram reabertas; os fatos valem como conferidos nas rodadas 1 e 2.

## Problemas
Nenhum P0 ou P1.

### P2 (não bloqueiam)
- P2 · f1 · Sugestão da rodada 2 não aplicada; afeta só a nota do fato, não a fala nem a tela. O texto segue com "e esta pesquisa não verificou relatos antigos de saque".
  → trocar por "e há relatos antigos de saque, sem prova sólida de destruição da tumba".
- P2 · `canal/pronuncia.json` · "Qin Shi Huang" e "Sima Qian" seguem fora. `fala_tts` cobre este vídeo; incluir depois do teste de pronúncia.

## Correções da rodada 2
- P0 c10 · aplicado: `fala`, `fala_tts`, `tela`, `visual`, `f10.afirmacao` e `f10.fontes` (5 fontes, com a Futura Sciences).
- P0 c12 · aplicado: `fala`, `tela`, `visual` e os dois trechos de `f13.afirmacao`.
- P1 c08 · aplicado: última frase do `visual`.
- P1 c03, c04 · contador: encerrado pelo responsável, com a correção de `ferramentas/montar.py` informada. Não reaberto.
- Cortes · aplicados: c02, c04 (`fala` e `fala_tts`), c06, c07 (`fala` e `fala_tts`), c09 (`fala` e `fala_tts`).
- P2 `canal/historico.json` · retirado: o responsável informou que o 001 nunca foi publicado.
- A previsão da rodada 2 era 196 palavras; a contagem real é 195. A redação confere, então a diferença não indica correção faltando.

## Formato conferido
- 13 cenas, 6 batidas em ordem, 9 formas e nenhuma repetida em cenas seguidas.
- Maior frase: 14 palavras (c11). Tela dentro do limite: até 5 palavras por linha e até 4 linhas.
- Todo `fala_tts` tem o mesmo número de palavras da `fala` e só muda as grafias fonéticas.
- Todos os ids de fato citados nas cenas existem, e todos os fatos são usados.
- Forma do gancho e acento diferem dos 3 últimos vídeos do histórico.

## Fatos conferidos
Sem nova checagem nesta rodada. Valem os resultados registrados na rodada 2:
- f1 a f9, f11, f12 e f14 ✓ (rodada 1; citações de f2 reconferidas na rodada 2).
- f10 ✓ na redação aplicada: National Geographic, Sixth Tone, Diário do Povo, Futura Sciences. "Escurece" e "racha" ficaram fora do vídeo.
- f13 ✓ na redação aplicada: The Star, National Geographic, Wikipedia, Scientific Reports. A medição no ar ficou fora do vídeo.
- Limite que continua valendo: não localizei estudo de 2023 ou 2024 que diga qual método o museu usa hoje; por isso a fala não nomeia o conservante.

## Pontos fortes (não mexer)
- O gancho é uma crença real, e o fecho no c13 responde a ele sem ranking de motivos sem fonte.
- A regra oficial no c11 mantém "por enquanto", e a tinta aparece como exemplo, não como causa.
- "~8.000" com "ESTIMATIVA" e "a tinta que restou" mantêm os números honestos.
- "Proteção sem garantia" e "só pista" dizem apenas o que as fontes sustentam.
