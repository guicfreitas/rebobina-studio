# Lições do canal

Erros que já custaram rodadas de revisão. Leia antes de escrever ou animar. Acrescente uma linha só quando um erro novo se repetir.

## Roteiro e fatos
- Não atribua a "especialistas" ou a alguém uma síntese nossa: a frase precisa estar na fonte, com autor certo.
- Não insinue causa: dois fatos lado a lado podem soar como um explicando o outro. Sem fonte da causa, reescreva.
- Número precisa do contexto dele: quem contou, em que situação, e se é pedido, estimativa ou confirmado.
- Duas fontes que se copiam contam como uma. Confira se a segunda é mesmo independente.
- Com fontes divergentes, use a forma que vale para todas ("mais de 160") e registre a divergência.
- Tela é fato: número, mapa, ponto e rótulo também precisam de 2+ fontes. "Mapa" e "lista" não podem afirmar o que a fala evita.
- Abra a fonte original e confira a citação literal, sem depender de resumo.
- Sem superlativo nem ranking sem fonte ("a que mais preocupa").
- Cena com até 14 palavras por frase; cheque a duração a 2,35 palavras por segundo.
- Falso cognato na tela: confira o sentido em português ("felonia").

## Voz
- Consulte `canal/pronuncia.json`. Palavra nova entra em `fala_tts` com letra de apoio para cada som, sem letra muda.
- Palavra curta importante ("major") pode sair errada: confira na transcrição da faixa só de voz.

## Cena e som
- `data-duration` dos clipes internos nunca menor que a cena; quando a voz mudar, atualize a cena à mão.
- Nada abaixo de y 1080; texto entre x 90 e 930; leitura mínima de 36 px. Grade e multidão também respeitam a zona.
- Peça entra sem atravessar legenda nem OSD: use autoAlpha e escala; papel corta acento se a margem for curta.
- Palco parado até 3 s, e a coisa nova entra na palavra que a nomeia.
- Desenho precisa se ler sem legenda: se não parece trigo ou cerca, não serve.
- Esquema é rotulado como esquema; nada desenhado pode parecer dado medido.
- Efeito: 1 a cada cerca de 4 s, som fiel à ação, nunca sobre palavra importante. Sem som fiel, fica sem som. Use `desloca` pelo `ataque` de `canal/sfx/fontes.json`.
- Só edite o que o roteiro manda; se mudar fala, rode de novo narrar, musica, sfx e montar.
