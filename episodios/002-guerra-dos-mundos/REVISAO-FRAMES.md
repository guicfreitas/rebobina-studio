# Revisão frame a frame — 002-guerra-dos-mundos — rodada 3 (voz Qwen3 no Colab)
VEREDITO: APROVADO NA IMAGEM E NAS MÉTRICAS · falta ouvir a voz (86,3 s, -14,5 LUFS, pico -1,4 dBTP)

## Corrigido nesta rodada
- Voz: Kokoro → Qwen3-TTS (T4 no Colab); legendas com tempos medidos por transcrição
- P0 · c03 e outras cenas · clipes internos mais curtos que a nova narração → durações ajustadas
- P0 · c06 · grade de casas invadia as legendas (até y 1160) → termina em y 1028
- P1 · c07 · rótulo do 98% ia até x 1035 → 32 px
- P1 · c05 · recorte da direita passava de x 930 → recortes reposicionados

## Não verificado
- Áudio medido e transcrito, mas não ouvido. Conferir de ouvido: "Halloween" (o whisper entendeu "Ralloy/Halói"), "Orson Welles", "ventríloquo" e o timbre de canal/voz/voz-rebobina.wav.

# Rodada 2 (voz Kokoro)
VEREDITO: APROVADO (métricas do render final em revisao/metricas.json)

## Problemas da rodada 1 (corrigidos)
- P0 · t=0–7s e t=72–79s · c01/c11 · "MARCIANOS" vazava da página do jornal → manchete 126 px
- P0 · t=27,6s · c05 · recortes "relato da imprensa" visíveis no rodapé antes de entrar → começam em y 1100
- P0 · t=33,5s · c05 · textos dos recortes quebravam linha e eram cortados → 40 px, sem quebra
- P1 · t=31s · c05 · citação "…tomando drama de guerra como fato" saía da folha → folha maior
- P1 · t=28s · c05 · palco vazio 0,5 s → o jornal cai logo no início da cena
- P1 · t=50,9s · c08 · ficha vazia ~1 s → relato aparece em 0,2 s
- P1 · t=77–79s · c11 · frase final "a notícia falsa era o pânico" ficava ~0,8 s antes da tela azul → aparece em "falsa" e o vídeo ganhou +0,6 s de respiro (CAUDA = 2,0 s para todos os episódios)
- P1 · c10 · prato da balança saía da tela à direita → balança redimensionada

## Não verificado
- Áudio só medido. Conferir de ouvido: "Orson Welles" (fala_tts "Órsson Uélss"), "Halloween" ("Rálouin"), "ventríloquo".
