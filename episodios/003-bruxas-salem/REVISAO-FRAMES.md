# Revisão frame a frame — 003-bruxas-salem — rodada 3
VEREDITO: APROVADO (0 P0, 0 P1, 6 P2)
Duração 90,3 s · 1080x1920 · 30 fps · −14,4 LUFS · pico −1,5 dBTP · `metricas.json` sem problemas nem avisos · `hyperframes check` ok (1 aviso: `legendas.html` grande)

## Aviso (não reprova; decisão do Guilherme)
- 90,3 s fica 0,3 s acima do ideal de 70–90 s e dentro do limite de 120 s.

## Problemas
Nenhum P0 ou P1.

- P2 · t≈55,80–55,87 s · c08 · o destaque de "À" e "MORTE" acende depois da voz: "à" ≈55,47 na voz e 55,80 na tela (+0,33 s); "morte" ≈55,57 na voz e 55,87 na tela (+0,29 s). Fica abaixo do limite de 0,4 s, e a frase inteira já está na tela desde 54,88 → pode ficar; se houver novo render, marcar "à" em ≈55,47 e "morte" em ≈55,57.
- P2 · t≈57,50 s · c08 · "POUPADA" bate na segunda sílaba de "poupou" (voz ≈57,3; +0,2 s), dentro do limite → pode ficar.
- P2 · t=58,24–58,57 s · c09 · palco quase vazio por 0,33 s de voz ("Só que"), até "CONDENADA" bater em "condenação". Curto e usado como respiro → pode ficar.
- P2 · t≈28,7 e 28,9 s · c05 · as pedras não chegam mais ao OSD, mas ainda cruzam o título "GILES COREY" ao cair. Vi em uma amostra de 1 a cada 3 frames, então a duração exata não foi medida → conferir no celular.
- P2 · t≈57–58 s · c08 · o fio vermelho oscila e sai cerca de 20 px da borda direita da ficha (x≈1030). Não é texto → pode ficar.
- P2 · t=86–89 s · c12 · a fumaça segue como disco cinza liso sobre o pôster e o carimbo; o "N" do Space Mono segue denso nos carimbos (c06, c08, c10, c12) → conferir no celular.

## Os 3 P1 da rodada 2
- Trilha até o fim: corrigido. No mp4, o pico cai sem salto: −16,0 dB (88,0–88,5), −18,5 (88,5–89,0), −21,8 (89,0–89,5), −26,9 (89,5–90,0), −36,7 (90,0–90,3). A média nos últimos 50 ms é −72,8 dB. O áudio tem 90,30 s, igual ao vídeo, e não há corte nem silêncio digital antes do fim.
- "MAS" adiantado: corrigido. A voz começa em 49,96 e a palavra está marcada em 49,96.
- Ficha da c08 vazando: corrigido. Em todos os frames de 49,80 a 50,27 há zero pixel claro abaixo da gaveta (y 1062–1110, x < 940) e na zona vermelha (y > 1335). A ficha sai de trás da gaveta.

## Outras mudanças desde a rodada 2
- c07: 11 focos contados no frame de 47,5 s, os mesmos 11 lugares de f13. Lausanne e Nancy não aparecem em `compositions/` nem em `roteiro.json`.
- c05: nenhuma pedra na faixa do OSD (y 100–300) de 26,5 a 31,5 s.
- c10: o topo do papel fica fixo em y=300 de 73,5 a 74,2 s, sem subir em "FITA 003" no tremor de "legisladores".
- Alinhamento da mistura: a correlação entre `narracao.wav` e o áudio do mp4 dá atraso de 0,00 s nos 6 trechos medidos (de c01 a c12; 0,97–0,99).
- As palavras da c09 à c12 recuaram 0,51 s em `tempos.json`, como a voz.

## Sincronia da c08 à c12 (tela medida frame a frame)
Voz: envelope acima de −35 dB, whisper por palavra (`-ng`, modelo small) e, para "morte", cortes sucessivos do áudio. Precisão aproximada de ±0,1 s.
| Cena | Palavra | Voz | Na tela | Desvio |
|---|---|---|---|---|
| c08 | Mas (legenda) | 49,96 | 49,96 | 0 |
| c08 | condenada (carimbo) | 54,94 | 54,97 | +0,03 |
| c08 | à (destaque) | ≈55,47 | 55,80 | +0,33 |
| c08 | morte (destaque) | ≈55,57 | 55,87 | +0,29 |
| c08 | poupou (carimbo) | ≈57,3 | 57,50 | +0,2 |
| c09 | condenação (carimbo) | ≈58,5 | 58,57 | +0,07 |
| c09 | Várias (1711) | 60,76 | 60,73 | −0,03 |
| c09 | nomes (1957) | ≈62,1 | 62,13 | 0 |
| c09 | limpos (2001) | ≈62,9 | 63,00 | +0,1 |
| c09 | não (X) | 64,55 | 64,53 | 0 |
| c09 | ninguém ("?") | 66,03 | 66,00 | 0 |
| c09 | Ela (cartão) | 67,60 | 67,53 | −0,07 |
| c09 | filhos (cartão treme) | ≈70,0 | 70,13 | +0,1 |
| c10 | oitavo | ≈71,95 | 72,00 | +0,05 |
| c10 | legisladores | ≈73,7 | 73,73 | 0 |
| c10 | inocentada (carimbo) | 77,16 | 77,20 | +0,04 |
| c11 | inocência (329) | ≈81,54 | ≈81,6 | +0,06 |
| c12 | nunca (risco) | ≈83,0 | 82,97 | −0,03 |
| c12 | fogueira (carimbo) | ≈84,1 | 84,17 | +0,07 |
| c12 | apagar ("329 ANOS") | ≈85,1 | 85,00 | −0,1 |
Nenhum desvio chega a 0,4 s. "Mas", "Várias", "Ela" e "inocentada" foram medidos no início de um trecho de voz; os demais têm a precisão indicada acima.

## Ritmo
Na resolução cheia, a c06 e a c08 não têm trecho acima de 1 s sem mudança no palco. Nas demais cenas, o maior trecho é de 2,6 s (c03, 9,5–12,1), medido em imagem reduzida, com limiar de 0,35% dos pixels. Essa medida é conservadora: ela apontou 4,5 s na c08 só porque a datilografia some na redução, e a resolução cheia desmentiu.

## Cena a cena
- c01: pôster "QUEIMADAS NA FOGUEIRA", fósforo lilás aceso e "SALEM, 1692"; frame 0 é a capa ✓.
- c02: três dígitos embaralham e travam em "0" amarelo gigante em "nenhuma"; REW para 1692 ✓.
- c03: mapa de Massachusetts enche de lilás, zoom com 5 pontos vermelhos e ponto amarelo "SALEM" ✓.
- c04: pontos enchem o palco com contador até 160+, 19 ficam vermelhos, 5 passam a lilás, sem forca ✓.
- c05: "GILES COREY · 19 SET 1692", pedras empilham, grades em "cadeia", carimbo "FOGUEIRAS: 0" ✓.
- c06: página em rolo, "LEI INGLESA DE 1604 / BRUXARIA: / CRIME, NÃO HERESIA", carimbo "PENA: FORCA" ✓.
- c07: mapa da Europa, carimbo "HERESIA", 11 focos laranja, Escócia laranja, Inglaterra lilás, câmera cruza até "SALEM" branco ✓.
- c08: ficha sobe da gaveta 1693, sem foto, fio vermelho, carimbos "CONDENADA" e "POUPADA" ✓.
- c09: carimbo "CONDENADA", linha do tempo 1711/1957/2001 com X, "?" e cartão; o OSD acompanha os anos ✓.
- c10: "1693 CULPADA" empurrado por caderno "8º ANO · NORTH ANDOVER", "2022", "INOCENTADA" ✓.
- c11: fita com rolos e contador de 1693 a 2022, "329 ANOS" amarelo em "inocência" ✓.
- c12: pôster volta riscado, "NENHUMA FOGUEIRA", fósforo apaga, "329 ANOS PARA APAGAR"; "■ STOP" a partir de 89,39 e tela azul de 89,7 a 90,3 ✓.
- Texto na tela × `tela` do roteiro: sem erro de digitação, acento ou número. OSD: 2026 → 1692 → 1693 → 1711/1957/2001 → 2022 ✓. Zonas: nenhum texto no trilho nem atrás da legenda nos frames vistos. Nada de cara de template.

## Não verificado
- Áudio: só medido, não ouvido. Equilíbrio voz × trilha e o fim da música: confirmar de ouvido.
- Pronúncia a conferir (como o whisper transcreveu, só a voz): "Salem" → "Sallen" em todas as vezes; "Massachusetts" → "Massachusset"; "inglesa" → "Inglésia"; "Giles Corey" → "Jaius Corei"; "contava como" → "contava com"; "a poupou" → "apoupou"; "Por quê" → "Porque". Conferir também "Johnson" e "Júnior" (transcrito "Jr."). Transcrição não prova erro de voz, só aponta onde ouvir.
- Fontes de f13: não abertas. `REVISAO-ROTEIRO.md` (13:42) condicionou a aprovação à retirada dos 2 focos e a correções em f13, e `roteiro.json` é de 13:43. Conferi que os focos saíram; as demais correções de f13 não foram conferidas uma a uma.
- Posição geográfica exata dos pontos da c03 e dos focos da c07.
- Comparação de layout com a 002: não feita por imagem.
- Celular real com a interface do app: zonas conferidas pelas medidas do DESIGN.
- Passagem das pedras sobre o título da c05, frame a frame.

---

# Histórico: rodada 2

# Revisão frame a frame — 003-bruxas-salem — rodada 2
VEREDITO: REPROVADO (0 P0, 3 P1)
Duração 90,8 s · 1080x1920 · 30 fps · −14,3 LUFS · pico −1,6 dBTP · `metricas.json` sem problemas nem avisos · `hyperframes check` ok (1 aviso: `legendas.html` grande)

## Aviso (não reprova; decisão do Guilherme)
- 90,8 s fica 0,8 s acima do ideal de 70–90 s e dentro do limite de 120 s. Corrigir o P1 da c08 cortando o silêncio inicial leva a cerca de 90,3 s.

## Problemas
- P1 · t=88,8–90,8 s · todas as faixas, fim do vídeo · a trilha para de repente em 88,80 s, com o volume subindo (−23,6 dB em 88,75), e os 2 s finais têm silêncio digital (−180 dB) sob o STOP e a tela azul. O fade de 2,5 s previsto em `ferramentas/musica.py` começa em 88,3 e é cortado aos 0,5 s: `trilha.wav` tem 88,80 s, a duração da narração, e o vídeo tem 90,8 s. Causa provável: `sidechaincompress` termina junto com a voz, a entrada mais curta → em `musica.py`, usar `[1:a]aresample=44100,apad=whole_dur={total}[v]`, rodar `musica.py`, `montar.py` e o render, e medir `trilha.wav` = duração do vídeo com fade até o fim · manter a faixa "Static Motion", o volume e a queda da música na fala.
- P1 · t=49,96–50,47 s · c08 · "MAS" acende 0,51 s antes da voz. `assets/voz/c08.wav` guarda 0,59 s de ruído de −41 a −47 dB antes de "Mas" (nas outras cenas a folga é de até 0,08 s), e o corte de pontas tratou esse ruído como voz. A voz começa em 50,47; o grupo "MAS SOBROU" sai em 50,62, quando ela só começa "sobrou" → em `narrar.py`, cortar o início da c08 até cerca de 0,08 s antes da voz e refazer `tempos.json`, `musica.py`, `montar.py` e o render. No tempo atual, os inícios medidos são: Mas 50,47 · sobrou ≈50,60 · uma ≈51,0 · ponta ≈51,2 · solta ≈51,45 · manter o texto e os tempos do resto da c08.
- P1 · t=49,84–49,97 s · c08 · nos 5 primeiros frames a ficha vaza por baixo da gaveta: o papel desce até y≈1370, atravessa a faixa da legenda e entra na zona vermelha (y > 1330), quebrando a ideia de que ela sai da gaveta. Vem de `y: 520` na entrada de `#c08-card` (altura 690 px) → pôr a ficha num contêiner com `overflow: hidden` e limite inferior em y=1060, a base da gaveta · manter a duração de 0,3 s, a gaveta e a posição final.

- P2 · t=27,27 / 28,30 / 28,70 / 29,47 s · c05 · ao cair, cada pedra aparece por 1 frame na altura do OSD, encostada no contador → começar a queda em y ≥ 320 ou esconder a pedra até entrar no palco.
- P2 · t=74,23–74,27 s · c10 · o tremor do caderno em "legisladores" (y −5) encosta o papel em "FITA 003" → tremer em x ou descer o caderno 5 px.
- P2 · t=86–89 s · c12 · a fumaça é um disco cinza liso, que parece bolinha ao passar sobre o pôster e o carimbo. O ritmo está resolvido; é só acabamento → conferir no celular.
- P2 · t=16,25–16,96 s · c03 · o rótulo "SALEM" fica só 0,7 s antes do corte. É a palavra-chave, mas volta na c07 → pode ficar.
- P2 · c06, c08, c10, c12 · o "N" do Space Mono continua denso nos carimbos ("PENA", "CONDENADA", "INOCENTADA", "NENHUMA") → conferir no celular.
- P2 · `ferramentas/revisar_video.py` · `freezedetect` não acusou nada nem com n=0,004 e d=1,5 s: o grão do VHS deixa a métrica cega, e a falta de aviso não prova ritmo → trocar por comparação de frames com limiar por pixel.

## Itens da rodada 1
- P0 legendas no trilho: corrigido. O x máximo medido em todos os frames é 916 (limite 930). A única exceção é a ficha do P1 acima, que não é legenda.
- P1 legenda e gatilhos adiantados: corrigido em 11 das 12 cenas; a voz começa até 0,08 s depois da primeira palavra. Falta a c08 (P1 acima).
- P1 números interpolados e quebrados: corrigido. "MIL SEISCENTOS E / NOVENTA E DOIS", "MAIS DE CENTO / E SESSENTA" e "TREZENTOS E VINTE / E NOVE ANOS" ficam inteiros, cada um em um só grupo. Desvios na tabela abaixo.
- P1 tamanho das legendas: corrigido. Os 85 grupos têm 72 px.
- P1 c07 parada, "FOGO" adiantado: corrigido. "BOA PARTE DA EUROPA:" entra em "Europa" (41,53), o carimbo "HERESIA" em "heresia" (43,77), "FOGO" em "fogo" (46,07), com zoom de 1 a 1,06.
- P1 c03 parada: corrigido (escala de 1 a 1,12; medida abaixo).
- P1 c12 parada: corrigido (fumaça em passos até 89,2 s; medida abaixo).
- P1 cartão da c09: corrigido. Entra em 68,03 ("Ela") e fica 3,2 s; "CONDENADA · 1693" com 36 px; em "filhos" só treme.
- P1 textos pequenos da c09: corrigido. Todos ≥ 36 px; "E OUTRAS / PESSOAS" em 2 linhas; os X não encostam em "BISHOP · MARTIN".
- P1 focos da c07 sem fontes: registro corrigido. f13 lista os 13 lugares, e o mapa tem 13 focos. Não reconferi as fontes (ver "Não verificado").
- P1 peças voando: corrigido nas cenas citadas. Nenhuma peça cruza as faixas protegidas fora dos casos listados acima (c05, c08, c10) e dos efeitos de rebobinar/avançar.
- P2 mapas anacrônicos, cidades da c03 e nomes em f11: registrados em `roteiro.json`. A c03 agora tem 5 pontos vermelhos, as 5 cidades de f2; a posição geográfica de cada um não foi conferida.
- P2 fita atrás do "329" e rótulo "SALEM" longe do ponto: corrigidos.
- P2 "N" dos carimbos: continua (acima).

## Efeitos da correção
- Pausas: as 28 emendas foram localizadas comparando cada faixa com `assets/voz/cenas/`. Nenhuma corta palavra: o trecho removido nunca passa de −42 dB (janelas de 10 ms), e as duas pontas de cada emenda ficam entre −43 e −55 dB.
- Fim das cenas: nenhuma palavra perdida na transcrição; o nível final de cada faixa é só ruído de fundo.
- Clipes: os 12 têm a mesma duração em `index.html` e na própria composição, são contíguos e terminam em 90,8 s. Nenhum elemento some antes da hora nos frames vistos.
- Trilha: a queda na fala acompanha a voz nova (mediana −30 dB na fala, −23 dB nas pausas); o comprimento está errado (P1 acima).
- Texto lido: as 210 palavras da fala aparecem na transcrição (`whisper-cli`, modelo small, só a voz). As diferenças são números em algarismos e as palavras de risco listadas abaixo. Legendas = `tempos.json` = `fala` do roteiro, palavra a palavra.

## Palco parado (maior trecho sem mudança, frame a frame)
| Cena | Trecho | Duração | O que há |
|---|---|---|---|
| c03 | 9,47–12,07 | 2,6 s | zoom lento e início do traçado |
| c03 | 13,90–16,23 | 2,3 s | zoom já feito, pontos entrando |
| c07 | 43,77–46,07 | 2,3 s | carimbo "HERESIA" e zoom lento |
| c07 | 41,53–43,77 | 2,2 s | mapa e zoom lento |
| c12 | 89,20–89,87 | 0,7 s | fumaça terminou, antes do STOP |

Nenhum chega a 3 s. Limiar: mais de 0,35% dos pixels mudando mais de 10 níveis de um frame para o outro, em y 190–1110 e x < 940.

## Legenda × voz nas palavras estimadas
Método: início da palavra pelo envelope (ilhas acima de −35 dB) e por sondas com `whisper-cli`, cortando o áudio em passos de 0,1–0,2 s. Precisão aproximada de ±0,15 s. As marcas por palavra do whisper erram até 0,67 s e não servem para isso sozinhas.
| Trecho | tempos.json | Voz | Desvio |
|---|---|---|---|
| c03 "dois" | 10,72 | ≈10,5 | +0,2 |
| c04 "sessenta" | 18,09 | ≈17,9 | +0,2 |
| c04 "pessoas" | 18,58 | ≈18,3–18,5 | até +0,25 |
| c08 "vinte" | 53,61 | ≈53,7 | −0,1 |
| c08 "anos" | 54,48 | ≈54,7 | −0,2 |
| c09 "continuou" | 60,05 | ≈60,05 | 0 |
| c10 "dois" (final) | 77,09 | ≈76,9 | +0,2 |
| c10 "ela" | 77,33 | ≈77,1–77,4 | até +0,2 |
| c11 "anos" | 80,65 | ≈80,55 | +0,1 |
| c11 "entre" | 80,94 | ≈80,8 | +0,15 |
| c11 "inocência" e "329" | 82,10 | ≈82,05 | 0 |
Só "Mas" (c08) passa de 0,4 s. As demais estimadas caem no início de um trecho de voz ou ficam a ≤ 0,36 s na comparação com o whisper.

## Cena a cena
- c01: pôster "QUEIMADAS NA FOGUEIRA", fósforo lilás aceso e "SALEM, 1692"; frame 0 é a capa ✓.
- c02: três dígitos embaralham e travam em "0" amarelo gigante em "nenhuma"; REW para 1692 ✓.
- c03: mapa escuro de Massachusetts, contorno se traça, enche de lilás, zoom com 5 pontos vermelhos e ponto amarelo "SALEM" ✓.
- c04: pontos enchem o palco com contador até 160+, 19 ficam vermelhos, 5 passam a lilás, sem forca ✓.
- c05: "GILES COREY · 19 SET 1692", pedras empilham, grades em "cadeia", carimbo "FOGUEIRAS: 0" ✓. Pedras: P2.
- c06: página em rolo, datilografia "LEI INGLESA DE 1604 / BRUXARIA: / CRIME, NÃO HERESIA", carimbo "PENA: FORCA" ✓. A linha "NÃO HERESIA" vai até x≈970, em y≈660, acima da zona do trilho.
- c07: mapa da Europa, carimbo "HERESIA", focos laranja, Escócia laranja, Inglaterra lilás, câmera cruza até "SALEM" branco ✓.
- c08: gaveta 1693, ficha sem foto, fio vermelho, "CONDENADA" e "POUPADA" nas palavras certas. Início: 2 P1.
- c09: carimbo "CONDENADA", linha do tempo 1711/1957/2001 com X, "?" e cartão; o OSD acompanha os anos ✓.
- c10: "1693 CULPADA" empurrado por caderno "8º ANO · NORTH ANDOVER", "2022", "INOCENTADA" em "inocentada" ✓.
- c11: fita com rolos e contador de 1693 a 2022, "329 ANOS" amarelo em "inocência" ✓.
- c12: pôster volta riscado, "NENHUMA FOGUEIRA", fósforo apaga em "apagar", "329 ANOS PARA APAGAR", STOP e tela azul ✓. Falta áudio no fim (P1).
- Texto na tela × `tela` do roteiro: sem erro de digitação, acento ou número. OSD: 2026 → 1692 → 1693 → 1711/1957/2001 → 2022 ✓. Nada de cara de template.

## Não verificado
- Áudio: só medido, não ouvido. Narração −16,2 LUFS; trilha −26,4 LUFS. Equilíbrio voz × trilha: confirmar de ouvido.
- Pronúncia a conferir (como o whisper transcreveu): "Salem" → "Sallen" em todas as vezes; "Massachusetts" → "Massachusset"; "inglesa" → "Inglésia"; "Giles Corey" → "Jaius Corei" / "Jai e os core"; "contava como" → "contava com"; "a poupou" → "apopou"; "Por quê" → "Porque". Transcrição não prova erro de voz, só aponta onde ouvir. Conferir também "Johnson" e "Júnior" (transcrito "Jr.").
- Na transcrição da mistura completa, o whisper pulou a c03 e marcou "[MÚSICA DE FUNDO]" no fim. Cortando o trecho, a c03 aparece inteira na mistura (com "Inglês" em vez de "inglesa"), então tratei como falha do transcritor; confirmar de ouvido que a música não cobre a voz nessa cena.
- Fontes de f2 e f13: vi que estão registradas, mas não abri nenhuma. `REVISAO-ROTEIRO.md` é de 03:15, antes da última edição de `roteiro.json` (12:56), então o revisor de roteiro pode não ter visto f13.
- Posição real dos pontos da c03 e dos focos da c07 no mapa.
- Comparação de layout com a 002: não feita por imagem.
- Celular real com a interface do app: zonas conferidas pelas medidas do DESIGN.
- Se 001 e 002 têm o mesmo corte de trilha: não confirmado; medir antes de reaproveitar `musica.py` corrigido em republicações.
