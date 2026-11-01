# Revisão frame a frame — 005-tumba-primeiro-imperador — rodada 2
VEREDITO: APROVADO
Duração 79,8 s · 1080x1920 · 30 fps · −15,0 LUFS · pico −1,5 dBTP

Escopo curto, a pedido: só os 3 P1 da rodada 1, a saída de `maquina` (c10), o `papel` (c09) e as placas translúcidas (c09). As outras cenas não foram revistas. `metricas.json` sem problemas nem avisos.

## Problemas
Nenhum P0 ou P1 novo. Os P2 da rodada 1 seguem abertos, exceto `maquina`.
- P2 · t=46,52–47,4 s · c09 · `papel` pode ficar quase inaudível: cerca de 18–20 dB abaixo da voz → só decidir depois de ouvir; subir o volume só se fizer falta · manter o tempo.

## Itens conferidos
- ✓ Legendas do "não": "NÃO ERA COR" (33,09 s) + "DE BARRO" (33,79 s), "NÃO É GARANTIDA" (54,14 s), "NÃO DISPARA / FLECHAS" (74,10 s). O sentido não se inverte mais. A última ocupa 2 linhas, mas não toca a porta: a porta termina em y≈1058 e a legenda começa em y≈1130.
- ✓ c08→c09: o soldado segue com o mesmo tom desbotado dos dois lados do corte, em 00:15. A cor não volta mais. Comparação visual, sem medir pixels.
- ✓ Fio de VERMELHO (t=37,5 s): termina em x≈480, já dentro do peito vermelho.
- ✓ `maquina` saiu: `sfx.json` tem 25 efeitos, nenhum deles `maquina`. Em `efeitos.wav` só resta a cauda do baque de c09, que some antes de 49,8 s. O `efeitos.wav` (13:58) é anterior ao render (14:04).
- ✓ `papel` (c09) não está órfão: toca de 46,52 a 47,4 s, com pico por volta de 47,1–47,2 s, em "solta" (47,16 s). Fica 0,2 s antes da primeira placa (47,36 s) e termina quando as placas começam. Isso corrige a rodada 1, que punha o pico em cima da queda. Está dentro da tolerância de 0,4 s.
- ✓ Placas translúcidas: não incomodam em velocidade normal. Cada queda dura 0,5 s, e a pilha no chão se lê como cacos coloridos. Só em pausa se vê rachadura através da placa e mistura de cor onde as placas se sobrepõem. Sem correção.
- Fora do escopo: entre grupos de legenda há cerca de 2 quadros sem texto (saída em `fim − 0,02` + entrada com fade). É o padrão de `montar.py`, também presente no episódio 003 (44 ocorrências nos dois). Não é regressão.

## Não verificado (rodada 2)
- Áudio: eu não ouço. Só medi. Falta ouvir se o `papel` aparece e a lista de pronúncia da rodada 1, abaixo.
- `hyperframes check`: não rodei de novo nesta rodada.
- Demais cenas e P2 abertos: não revistos.

---

# Rodada 1 (histórico)
VEREDITO: REPROVADO
Duração 79,8 s · 1080x1920 · 30 fps · −15,0 LUFS · pico −1,5 dBTP

Motivo: nenhum P0, mas 3 P1 (a regra reprova com 3). Nenhum dos três exige narrar de novo.
`metricas.json` sem problemas nem avisos. `hyperframes check`: ok (só o aviso de tamanho de `legendas.html`, arquivo gerado).

## Problemas

### P1
- P1 · t=33,31 / 54,35 / 74,32 s · c07, c10, c13 · a legenda separa o "não" do verbo. Sem som, lê-se "ERA COR" + "DE BARRO" (0,47 + 0,62 s), "É GARANTIDA" (0,92 s, enquanto o carimbo diz NÃO GARANTIDA) e "DISPARA FLECHAS" (1,18 s). As três frases ficam com o sentido invertido → em `agrupar_legendas` (`ferramentas/montar.py`), nunca fechar grupo logo depois de "não". Resultado: "SÓ QUE / NÃO ERA COR / DE BARRO", "AINDA / NÃO É GARANTIDA", "EM AÇÃO / NÃO DISPARA FLECHAS" · manter o limite de 3 palavras e os demais grupos. Conferir o efeito nos outros grupos ao rodar `montar.py`.
- P1 · t≈43,0 s · c08→c09 · o soldado termina c08 desbotado (opacidade 0,67 em 00:15) e c09 abre com a cor 100% viva, ainda em 00:15. A cor "volta" no corte, contra o que a voz diz → em c09, começar `#c09-so-cor` e `.c09-lasca` com opacidade 0,67 · manter rachaduras, queda das placas, contador e o desbotamento de c08.
- P1 · t=36,46–38,1 s · c07 · o fio de "VERMELHO" termina em x≈450, em cima da manga azul, e não chega ao peito vermelho (x≥465). Depois de "azul", o rótulo aponta para a cor errada → estender `#c07-fv` até x≈480, por cima da manga · manter rótulo, cor e os outros três fios.

### P2 (não bloqueiam)
- P2 · t=49,28 s · c10 · **único efeito que deve sair: `maquina` de c10.** Entra 0,53 s depois do baque de c09 e cai sobre "Hoje" (cerca de 25 dB abaixo da voz em RMS, medido), num momento em que o recibo mal se move → apagar do `sfx.json`, rodar `sfx.py`, `montar.py` e o render · manter os outros 25.
- P2 · t=13,3–14,7 s · c03 · "PERTO DE" termina em x=934: 4 px além da coluna (930) e 6 px antes do trilho (940) → recuar `#c03-loc` e `#c03-fio` 20 px para a esquerda.
- P2 · t=9,5–14,7 s · c03 · o contorno encosta no topo de "210 A.C." (x≈340, y≈775) e a ilha de Hainan quase toca "HUANG" (x≈575, y≈895) → descer os dois textos 10–15 px ou subir o mapa o mesmo tanto, sem invadir a faixa da legenda.
- P2 · t=7,35–9,3 s · c02 · o carimbo "OUTRO MEDO" encosta no til de "CONFIRMAÇÃO" e fica na linha das armadilhas, o que permite ler "ARMADILHAS: OUTRO MEDO" → subir 10 px e, se couber, passar o carimbo para a faixa de "RELÍQUIAS".
- P2 · t=69–71,8 s · c12 · "ORIGEM AINDA EM DEBATE" fica logo abaixo da flecha com "SEM CONFIRMAÇÃO" e parece falar das flechas, mas é sobre o mercúrio → aproximar a linha do bloco do mercúrio.
- P2 · t=20,2–22 s · c04 · sem som, "BESTAS ARMADAS" pode ser lido como animais. As flechas vermelhas ajudam → se o roteirista aceitar, trocar por "BALESTRAS ARMADAS".
- P2 · t=12,01–13,29 s · c03 · legenda parte o nome: "MORRE QIN SHI" / "HUANG" → tratar "Qin Shi Huang" como bloco único.
- P2 · vários · legendas de 0,30–0,35 s ("A TUMBA" 0,17 s, "É MEDO" 3,56 s, "O MUSEU" 5,41 s, "A TINTA" 39,54 s, "E LEVA" 47,92 s) somem antes da leitura → aceitável só porque o palco sustenta a ideia.
- P2 · t=0–3,1 s · c01 · a capa tem gancho e porta, mas o lacre só entra em 3,11 s e a flecha em 3,86 s. Até lá, só o zoom lento e as legendas mudam, e a porta com pontos pode lembrar um armário → considerar o lacre já no frame 0.
- P2 · t=30–32,4 s · c06 · o bloco de ~8.000 figuras vira hachura no tamanho do celular, e os painéis cobrem boa parte dele → manter, se a ideia de multidão bastar.
- P2 · identidade · 5 trocas de ano; `DESIGN.md` pede de 2 a 4. A de 2024→2026 (49 s) é a mais dispensável, mas "Hoje" pede 2026 → decisão do Guilherme.

## Pontos pedidos

### Efeitos (26, média de 1 a cada 3,1 s)
- Conferi o ataque de cada som, descontado o silêncio inicial do arquivo, contra o evento na animação. **Nenhum efeito está órfão ou fora de tempo.** Os impactos (baque, carimbo, clique) ficam a até 0,07 s do evento visual.
- `papel` (c09) e `pagina` (c04, c11) começam antes, mas o pico cai em cima da queda das placas, da abertura do rolo e da virada da página.
- `vhs` final entra em 78,82 s, junto do STOP (78,88 s) e 0,34 s antes do azul (79,16 s). Fica como está.
- A média engana: os intervalos vão de 0,53 s a 9,7 s. Os 4 cliques de c07 ficam a menos de 1 s entre si, e de 67,5 s a 77,2 s não há efeito nenhum. Não há excesso geral; só `maquina` (c10) sai.
- Para ouvir (risco de cobrir a voz; Whisper ainda entende na mistura): `carimbo` em "garantida" (54,76 s, cerca de 4 dB acima da voz), `baque` em "mil/figuras" (30,69 s, no nível da voz), `swoosh` em "flechas" (20,40 s, no nível da voz). `vhs` termina em cima de "Ano" (c03, Whisper ouviu "Há no" na mistura), "Mil" (c05) e "Exposta" (c08).

### Contador
- "210 A.C." ✓ (fixo em cerca de 9,5 s, com REW), bate com o roteiro.
- "~100 A.C." ✓ (FF passa por "102 A.C." e o rótulo entra em cerca de 15,3 s).
- Salto a 2024 ✓: FF de 1974 passa por 1993, chega a 2024 no começo de c08 e combina com "MUSEU DA TUMBA, 2024". Depois, 2024→2026 em 49,2 s, em "Hoje".

### c11 com 9,74 s
Sem trecho morto: cerca de 10 eventos, e o maior intervalo é de cerca de 1,4 s (62,05–63,45 s). É a cena mais longa e a última de papel antes do fecho, mas não pede corte. Manter.

### Voz (medido, não ouvido)
Comparei Whisper na faixa de voz com formantes das vogais e com a mesma palavra em outras cenas. Isso é indício, não confirmação.

| Palavra | Whisper | Medição | Conclusão |
|---|---|---|---|
| "tumba" c02 | "Tomba" na frase; "tumba" no recorte isolado | F1 ≈ 300–345 Hz, igual a c01, c04 e c11 (≈ 250–355). /o/ em "solo" ≈ 470–505 | Erro provável do Whisper, não da voz |
| "tumba" c06 | "tomba" na frase; "da tumba" no recorte | F1 cai de ≈ 430 a 260 Hz; fim da palavra fraco | Provável /u/, sinal menos limpo. Ouvir |
| "Exposta" c08 | "Exposto" | Vogal tônica com F1 ≈ 530–590 (aberta, como em "expósta"); vogal final com F1 ≈ 600, /u/ estaria perto de 300 | Erro provável do Whisper; a junção "exposta ao" funde as vogais |
| "já vista" c13 | "vista" na frase; "visto" no recorte | Sem sinal de /u/ final; o "-a" se funde com "em" | Erro provável do Whisper |
| "Qin Shi Huang" c03 | "Chin-Shih-Huan" / "Tin Shi Huang" / "Jin Shi-Huan" | Cada rodada grafa diferente | Sem conclusão: nome estrangeiro. Ouvir |
| "Sima Qian" c04 | "Sima Tien" / "Sima Tian" | Compatível com `fala_tts` "Síma Tchién" em leitura brasileira | Sem sinal de erro. Ouvir |

Nenhuma dessas medições justifica narrar de novo.

### Silhuetas e mapa
- Silhuetas genéricas ✓: soldado sem rosto e pictogramas; nenhuma pessoa real, nenhum retrato do imperador.
- Mapa c03 ✓: a mancha verde fica em volta do ponto e não preenche o contorno. O contorno ganha um fundo cinza neutro em "Morre", sem cor de acento. O ponto de Xi'an está na posição esperada. O contorno é o atual, sem rótulo que diga isso.

## Cena a cena
- c01: pergunta gigante, porta com pontos; depois lacre vermelho e flecha amarela ✓ (frame 0 com gancho e símbolo).
- c02: etiqueta de museu pendurada, linhas datilografadas, carimbo, faixa verde "MUITO FRÁGEIS" ✓ (P2 do carimbo).
- c03: mapa da China se traça, nome, ponto em Xi'an, mancha verde ✓ (P2 de encostes e legenda).
- c04: rolo de papel, texto datilografado, linhas prateadas, três flechas vermelhas ✓.
- c05: "1974" gigante, gaveta "ARQUIVO", ficha com poço, pá bate no soldado ✓.
- c06: pictogramas viram multidão, número sobe a ~8.000, morro "GUARDA DA TUMBA" ✓.
- c07: soldado bege ganha 4 cores com rótulos ✗ (P1 do fio) (P1 da legenda).
- c08: contador 00:00→00:15, soldado desbota, "A COR COMEÇA A MUDAR", "MUSEU DA TUMBA, 2024" ✓.
- c09: contador até 04:00, rachaduras, placas caem até o chão ✗ (P1 da cor que volta).
- c10: máquina "LABORATÓRIO" solta recibo, carimbo "NÃO GARANTIDA" ✗ (P1 da legenda).
- c11: ofício, carimbo "NÃO ESCAVADA", vira a folha, "POR ORA" sublinhado ✓.
- c12: flecha com carimbo "SEM CONFIRMAÇÃO", corte do morro com pontos só na terra de cima, câmara vazia ✓ (P2 do rótulo).
- c13: porta do início, flecha se apaga, "ABRIR" em vermelho, lacre treme; STOP e tela azul ✗ (P1 da legenda).
  - Fim: ■ STOP de 78,88 s até o azul, azul pleno de cerca de 79,28 s a 79,78 s. O azul cobre o STOP, como no episódio 004 ✓.

Textos da tela conferidos com `roteiro.json` e a tabela de fatos: sem erro de digitação, acento ou número. Zonas: nada sob o trilho ou atrás da legenda.

## Não verificado
- Áudio: eu não ouço. Só medi: −15,0 LUFS, pico −1,5 dBTP. Alinhamento dos efeitos na mistura medido em 3 pontos (atraso 0,0 s).
- Pronúncia, para o humano conferir: "Qin Shi Huang" (12,5 s), "Sima Qian" (17,0 s), "tumba" (6,0 s e 32,0 s), "Exposta" (38,5 s), "já vista" (73,2 s), "spray" (49,9 s), "câmara" (55,7 s; Whisper na mistura ouviu "câmera"), "um poço" (26,0 s; Whisper na mistura perdeu o "um"), "Ano" (9,4 s). Entonação de pergunta em "E as flechas?" (65,4 s).
- Cena c12 a c13 sem efeito por 9,7 s: se soa vazia, só o ouvido dirá.
- Quadros entre os 2 frames/s das folhas: revisados só nas trocas de cena c08→c09, c09→c10 e no fim, além do frame 0.
- Fatos e fontes: não reabertos; valem os da revisão de roteiro.
