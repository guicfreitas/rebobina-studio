# Revisão frame a frame — 001-acre-cavalo — rodada 2
VEREDITO: APROVADO
Duração 75,8 s · 1080x1920 · 30 fps · −13,5 LUFS · pico −1,3 dBTP (medidos em render/rascunho.mp4)

> Rodadas feitas durante a montagem do pipeline, seguindo `.claude/agents/revisor-frames.md`.

## Problemas da rodada 1 (corrigidos)
- P0 · t=14,2s · c04 · documento do tratado já visível no rodapé antes de entrar → começa em y 1700
- P0 · t=44,6s · c08 · "DE CASTRO" aparecendo cortado na borda direita → começa fora da tela (x 1200)
- P0 · t=30,5s · c06 · contador mostrava "20" em vez de "20.000" (GSAP leu o texto como número) → prefixo invisível
- P1 · t=5,6s · c02 · carimbo MITO subia sobre o contador do OSD → para à direita do cavalo
- P1 · c05/c06/c09 · zoom do mapa invadia a faixa do OSD → contêiner com overflow hidden
- P1 · t=14,0–15,3s · c04 · palco vazio enquanto a voz diz "um diplomata brasileiro" → título grande desde o início
- P1 · t=41,6–44,3s · c08 · palco vazio → "4ª TENTATIVA" + linha do tempo com os levantes de 1899/1900
- P1 · t=41,0s · c07 · carimbo ARRENDADO só 0,5 s na tela e invadindo o trilho direito → entra em "arrendou", dentro da coluna
- P1 · t=56,0s · c09 · a virada (Acre fica verde) durava 0,7 s → começa em "o Acre passou"
- P1 · t=53,5s · c09 · acento de "PETRÓPOLIS" cortado pela máscara da animação → máscara com folga vertical
- P2 · t=47,5s · c08 · "6 AGO 1902 · XAPURI" quebrava em 2 linhas → nowrap

## Cena a cena
- c01 pergunta gigante + cavalo de xadrez verde (capa) ✓ · c02 carimbo MITO, "…mas o cavalo existiu." ✓
- c03 ficha de arquivo datilografada de Melgarejo ✓ · c04 2 medalhas + 1 cavalo → Tratado de Ayacucho assinado ✓
- c05 mapa: área do Acre fica cor da Bolívia ✓ · c06 rios + pontos de seringueiros + 60.000+ ✓
- c07 contrato de arrendamento + carimbo ✓ · c08 linha do tempo, 4ª tentativa, Plácido de Castro ✓
- c09 Tratado de Petrópolis, Acre escorre para o verde ✓ · c10 recibo impresso item a item ✓
- c11 conta real: cavalo ✗, dinheiro/terra/trilhos/guerra ✓ · c12 trilhos na escuridão, "Ferrovia do Diabo", tela azul + STOP ✓

## Não verificado
- Áudio: só medido. Conferir de ouvido a pronúncia de "Melgarejo", "Síndiqueit" (Syndicate), "Plácido de Castro", "Petrópolis", "Xapuri".
- Kokoro em português tem sotaque sintético perceptível; o volume integrado ficou em −13,5 LUFS (ok para social).
