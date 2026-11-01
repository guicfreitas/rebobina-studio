# Rebobina — Bíblia do canal

> Toda fita tem um começo. A gente rebobina até ele.

Canal dark (sem rosto) de **acontecimentos históricos** em vídeo vertical para **TikTok** e **YouTube Shorts**.
Idioma atual: **PT-BR**. Inglês virá depois (ver "Versão em inglês" no fim).

**Perfis:** TikTok `@rebobina.media` (https://www.tiktok.com/@rebobina.media) · YouTube "Rebobina na História" `@RebobinaNaHistoria` (https://www.youtube.com/@RebobinaNaHistoria) · Instagram "Rebobina na História" `@rebobina.media` (https://www.instagram.com/rebobina.media/)

---

## 1. Promessa ao espectador

Em cerca de 80 segundos você descobre **a história real por trás de algo que você acha que sabe**:
um mito popular, uma curiosidade do livro de história, um "por que isso é assim?".
Cada vídeo termina com uma virada e uma frase que fica na cabeça.

O que o Rebobina **não** é: compilado de fatos soltos, lista "top 10", voz robótica lendo Wikipédia.

## 2. Público

Brasileiros de 16 a 40 anos que gostam de "curiosidades que ninguém te contou na escola".
Assistem no celular, muitas vezes **sem som**. A legenda e a imagem precisam contar a história sozinhas.

## 3. Pautas: o que entra

Um bom tema do Rebobina tem **as quatro coisas**:

1. **Gancho com crença popular** — um mito, uma frase feita, uma pergunta que todo mundo já fez ("o Acre foi trocado por um cavalo?", "por que o Brasil fala português?", "Santos Dumont inventou o avião?").
2. **Virada verificável** — a resposta real surpreende e tem fonte confiável.
3. **Visualizável sem filmagem** — dá pra contar com mapas, linhas do tempo, documentos, números, recibos, fichas. (Somos um canal de motion graphics em HTML, não de imagens de arquivo.)
4. **Cabe em 70–90 s** — uma história, um fio condutor. Se precisa de 3 minutos, vira série em partes.

Escopo: **história mundial e do Brasil, em pé de igualdade**. Alternar: a cada 3 vídeos, pelo menos 1 de fora da América Latina e no máximo 2 do mesmo continente seguidos. Temas mundiais funcionam melhor quando o gancho é algo que o brasileiro conhece (um mito famoso, uma frase do dia a dia, um objeto comum).

### O que NÃO entra (regra dura)

- Tragédias recentes com vítimas identificáveis, violência gráfica, sofrimento como espetáculo (o YouTube desmonetiza "conteúdo perturbador").
- Política partidária atual, eleições, figuras políticas vivas como tema central.
- Teorias da conspiração, pseudo-história, "segredos que esconderam de você" sem fonte.
- Conselho médico, jurídico ou financeiro (o YouTube não monetiza persona de IA aconselhando sobre isso).
- Qualquer fato sem pelo menos **2 fontes independentes**, sendo 1 delas acadêmica, oficial ou enciclopédica.

## 4. Regras de plataforma (o que define a duração)

| | TikTok (Programa de Recompensas do Criador) | YouTube Shorts (YPP) |
|---|---|---|
| Duração mínima para monetizar | **mais de 60 s** | qualquer |
| Duração máxima | 10 min | **3 min** |
| Entrada no programa | 18+, 10 mil seguidores, 100 mil views em 30 dias | 1.000 inscritos + 10 mi views de Shorts em 90 dias (20 mi para novos a partir de 01/02/2027) |
| Originalidade | Conteúdo original, sem música com direitos autorais por mais de 1 min | Política de "conteúdo inautêntico": nada de vídeos com cara de template, repetitivos ou em massa |
| Rótulo de IA | Ativar "conteúdo gerado por IA" quando houver voz/imagem sintética | Divulgar apenas conteúdo sintético **realista** (não é o nosso caso, animação gráfica) |

**Nossa regra:** vídeo final entre **70 e 90 segundos**. Nunca abaixo de **65 s** (margem de segurança sobre os 60 s do TikTok). Nunca acima de 120 s.

> Revisar esta tabela a cada 3 meses: as plataformas mudam as regras com frequência.

## 5. Estrutura de roteiro (esqueleto de 6 batidas)

| Batida | Tempo | Função | Exemplo (Acre) |
|---|---|---|---|
| 1. Gancho | 0–4 s | A crença popular, dita como pergunta ou afirmação provocadora. Já está na tela no frame 0. | "Dizem que o Brasil comprou o Acre… em troca de um cavalo." |
| 2. Quebra | 4–8 s | Contradição curta que obriga a ficar. | "É mentira. Mas o cavalo existiu." |
| 3. Rebobinar | 8–30 s | Volta no tempo: ano, lugar, personagem. O contador de anos rebobina. | 1867, Melgarejo, o presente. |
| 4. Escalada | 30–60 s | 2 a 4 acontecimentos em cadeia, cada um causando o próximo. | Borracha → arrendamento → guerra. |
| 5. Virada | 60–75 s | O fato que responde o gancho, com o número ou documento real. | O recibo: £ 2 milhões + terra + ferrovia. |
| 6. Fecho | últimos 5–10 s | Uma frase que amarra o gancho + gancho para a próxima fita (série). | "…e uma guerra. Essa ferrovia ganhou um apelido: Ferrovia do Diabo. Mas essa é outra fita." |

Regras de escrita:

- **170–210 palavras faladas** (a voz narra a ~140 palavras/min ⇒ 73–90 s).
- Frases curtas, de 6 a 14 palavras. Uma ideia por frase. Português falado, não acadêmico.
- Números na **fala** por extenso ("mil novecentos e três"); na **tela** em algarismos ("1903").
- Nada de "Olá pessoal", "se inscreva" ou "deixa o like" no começo. Chamada para ação só no fecho, e só em forma de série ("essa é outra fita").
- Cada cena tem **uma** forma de informação (ver §7) diferente da anterior.
- Toda afirmação factual aponta para uma fonte na tabela de fatos do roteiro.
- Datas e números arredondados com honestidade ("cerca de 3 mil km²" quando as fontes divergem).
- Quando historiadores divergem, a fala diz isso ("segundo historiadores", "a versão mais aceita").

### Narração

Fase atual: **Qwen3-TTS** (Apache 2.0, uso comercial liberado) rodando grátis numa GPU do Google Colab
comandada pelo terminal (Colab CLI), sempre clonando a voz do canal em `canal/voz/voz-rebobina.wav`
(`motor_voz: "colab"`). Reserva local:
Kokoro (`pm_alex`). Fase seguinte: **voz do Guilherme**
gravada (`motor_voz: "gravacao"` no roteiro, arquivo em `assets/voz/gravacao.wav`). O roteiro é
escrito para ser **falado**: leia em voz alta antes de aprovar.

## 6. Tom de voz

Curioso, direto, levemente irônico, nunca debochado com povos, vítimas ou países.
Pense em um amigo que adora história contando algo no bar, mas que checou as fontes antes.

## 7. Formas de informação (para variar as cenas)

Cada cena escolhe **uma**, e o vídeo usa pelo menos **5 formas diferentes**:

`mapa` · `linha-do-tempo` · `ficha-de-arquivo` (personagem) · `documento` (tratado, carta, contrato com carimbo) · `recibo` (custos, trocas) · `número-que-cai` (contador) · `mito-x-fato` (carimbo MITO / FATO) · `antes-e-depois` · `multidão-de-pontos` (pessoas, quantidades) · `citação-pôster` · `comparação-de-escala` · `objeto-símbolo` (um ícone grande: cavalo de xadrez, medalha, trilho) · `manchete-de-jornal`

## 8. Variedade (defesa contra "conteúdo inautêntico")

O YouTube corta a monetização de canais cujos vídeos parecem saídos do mesmo template. Por isso:

- `canal/historico.json` registra cada vídeo: tema, era, região, gancho, formas usadas, paleta de acento e transições.
- Um vídeo novo **não pode** repetir a mesma sequência de formas de nenhum dos últimos 10 vídeos, nem abrir com a mesma forma de gancho de nenhum dos últimos 3.
- Alternar eras (antiguidade · colonial · império · república · século XX) e regiões.
- A identidade visual (VHS, contador, legendas) é fixa; o **conteúdo das cenas** nunca é.
- A voz humana do canal está na **escolha da pauta, na pesquisa e na virada**: é isso que o roteirista e o revisor protegem.

## 9. Ritmo de publicação

- Começo: **1 vídeo por dia**, no mesmo horário (sugestão: 19h, horário de Brasília).
- Mesmo arquivo nas duas plataformas, com título, descrição e hashtags adaptados a cada uma.
- Séries: quando um fecho promete "outra fita", o próximo vídeo da série sai em até 3 dias.

## 10. Versão em inglês (fase 2)

Mesmo roteiro, traduzido e **adaptado** (não literal) pelo roteirista, com `idioma: en` no cabeçalho.
O narrador muda para uma voz em inglês, as legendas e textos de tela são refeitos e o canal é outro
(sugestão: **Rewind Files** ou **Rewound**). Fontes em inglês na tabela de fatos.
