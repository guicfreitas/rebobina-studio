---
description: Produz um vídeo do Rebobina de ponta a ponta (roteiro → revisão → animação → revisão frame a frame → pacote de publicação)
argument-hint: "[tema opcional] [sem paradas]"
---

Produza um novo vídeo do canal **Rebobina** coordenando os agentes do projeto.
Pedido: **$ARGUMENTS** ("sem paradas" é uma opção, não um tema).

Você é o orquestrador: não escreva roteiro nem cena você mesmo; delegue a cada agente pelo
Task tool (`subagent_type`) e passe entre eles apenas caminhos de arquivo e vereditos.
Mantenha uma lista de tarefas visível com as etapas abaixo.

0. **Escolha do tema** (só se o pedido não trouxer tema) → agente `pesquisador-pautas`. Ele pesquisa o nicho,
   compara candidatos e devolve o vencedor e o caminho do relatório em `canal/pesquisas/`.
1. **Roteiro** → agente `roteirista` com o tema pedido ou, sem tema, com o vencedor e o relatório da pesquisa.
2. **Revisão do roteiro** → agente `revisor-roteiro` com a pasta do episódio.
   - REPROVADO: devolva ao `roteirista` com o caminho de `REVISAO-ROTEIRO.md`; revise de novo.
     Máximo **3 rodadas**; se ainda reprovar, pare e mostre os problemas ao Guilherme.
3. **Parada 1 — aprovação do roteiro** (pule se o pedido contém "sem paradas"): mostre ao
   Guilherme, se o tema veio da pesquisa, por que ele venceu e o que não pôde ser medido; depois o gancho, as falas em ordem, a virada, a duração estimada e as fontes principais.
   Espere "ok" ou ajustes (ajustes voltam ao passo 1 com as instruções dele).
4. **Narração** (automática com `motor_voz: "colab"`): o animador roda `narrar.py`, que liga uma GPU T4
   no Colab pelo Colab CLI, narra com a voz do canal e desliga. Se for a primeira vez no computador e o
   `colab` pedir login, peça ao Guilherme para colar o código do Google no terminal. Se for criada uma voz
   nova (★), mostre `canal/voz/voz-rebobina.wav` para ele aprovar antes de animar.
5. **Animação** → agente `animador` com a pasta. Se ele avisar que a narração ficou < 65 s, volte
   ao `roteirista` pedindo +20–30 palavras e repita os passos 2, 4 e 5.
6. **Revisão frame a frame** → agente `revisor-frames`.
   - REPROVADO: devolva ao `animador` com `REVISAO-FRAMES.md`; revise de novo. Máximo **3 rodadas**.
7. **Parada 2 — aprovação do vídeo** (pule se "sem paradas"): envie `render/rascunho.mp4` ao
   Guilherme com 2 linhas sobre o que foi feito e o que o revisor não pôde checar (áudio/pronúncia).
8. **Publicação** → agente `publicador`. Ele faz o render final e a pasta `publicar/`, e nunca
   clica em Publicar.
9. Termine com: caminho de `publicar/`, duração final e **o conteúdo inteiro de `publicar/TEXTOS.md`**
   (legenda do TikTok com hashtags, título e descrição do YouTube com hashtags, comentário fixado),
   cada um em bloco de código para copiar; e o lembrete de rodar `--publicado` com os links depois de postar.
