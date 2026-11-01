#!/usr/bin/env python3
"""Monta a pasta publicar/ de um episódio a partir de publicacao.json (escrito pelo agente publicador).

Uso:
    python3 ferramentas/pacote_publicacao.py episodios/001-acre-cavalo
    python3 ferramentas/pacote_publicacao.py episodios/001-acre-cavalo --publicado tiktok=URL youtube=URL

Gera em <ep>/publicar/:
    rebobina-<id>-<slug>.mp4   o vídeo final (render/final.mp4)
    capa.jpg                   capa/capa.jpg de ferramentas/capa.py; sem ela, o frame 0 do vídeo
    TEXTOS.md                  todos os textos juntos, prontos para copiar
    DESCRICAO-TIKTOK.txt       legenda do TikTok + hashtags
    TITULO-YOUTUBE.txt / DESCRICAO-YOUTUBE.txt   título e descrição + hashtags do Shorts
    DESCRICAO-INSTAGRAM.txt    legenda do Reels + hashtags + crédito (só se publicacao.json tiver o bloco "instagram")
    COMENTARIO-FIXADO.txt      comentário para fixar (fontes + pergunta)
    CHECKLIST.md               passo a passo da postagem manual
Com --publicado, registra o episódio em canal/historico.json (usado para garantir variedade).
"""
import difflib, json, re, shutil, subprocess, sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def main():
    ep = Path(sys.argv[1]).resolve()
    rot = json.loads((ep / "roteiro.json").read_text())
    pub = json.loads((ep / "publicacao.json").read_text())
    final = ep / "render" / "final.mp4"
    if not final.exists():
        sys.exit("✗ render/final.mp4 não existe. Rode o render de entrega antes.")
    dst = ep / "publicar"
    dst.mkdir(exist_ok=True)
    nome = f"rebobina-{rot['id']}-{rot['slug']}.mp4"

    if "--publicado" in sys.argv:
        links = dict(a.split("=", 1) for a in sys.argv[sys.argv.index("--publicado") + 1:] if "=" in a)
        hist_f = RAIZ / "canal" / "historico.json"
        hist = json.loads(hist_f.read_text()) if hist_f.exists() else []
        hist = [h for h in hist if h["id"] != rot["id"]]
        hist.append({"id": rot["id"], "slug": rot["slug"], "data": date.today().isoformat(), "tema": rot["tema"],
                     "era": rot.get("era"), "regiao": rot.get("regiao"), "acento": rot.get("acento"),
                     "gancho_forma": rot["cenas"][0]["forma"], "formas": [c["forma"] for c in rot["cenas"]],
                     "duracao": json.loads((ep / "tempos.json").read_text())["duracao_video"],
                     "musica": json.loads((ep / "musica.json").read_text())["titulo"] if (ep / "musica.json").exists() else None,
                     "links": links})
        hist_f.write_text(json.dumps(hist, ensure_ascii=False, indent=1))
        print(f"✓ registrado em canal/historico.json ({len(hist)} vídeos)")
        # confere na hora se o que foi ao ar bate com publicacao.json (título errado, Short fora do histórico)
        subprocess.run([sys.executable, str(RAIZ / "ferramentas" / "metricas.py")])
        return

    # recomprime para upload (o render "delivery" sai com ~28 Mbps; os apps recomprimem de qualquer jeito)
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(final), "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "21", "-maxrate", "8M", "-bufsize", "16M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(dst / nome)], check=True)
    capa = ep / "capa" / "capa.jpg"
    if capa.exists():
        shutil.copy2(capa, dst / "capa.jpg")
    else:  # sem capa.py, o frame 0: as legendas só entram em 0,1 s
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(final), "-frames:v", "1", "-q:v", "2",
                        str(dst / "capa.jpg")], check=True)
    tk, yt = pub["tiktok"], pub["youtube"]
    ig = pub.get("instagram")  # opcional: episódios antigos não têm este bloco
    fontes_urls = list(dict.fromkeys(u for f in rot["fatos"] for u in f["fontes"]))
    tags = lambda lst: " ".join(t if t.startswith("#") else f"#{t}" for t in lst)

    # textos prontos para colar (descrição + hashtags no mesmo bloco)
    desc_tk = f"{tk['legenda'].strip()}\n\n{tags(tk['hashtags'])}"
    titulo_yt = yt["titulo"].strip()
    desc_yt = f"{yt['descricao'].strip()}\n\n{tags(yt['hashtags'])}"
    desc_ig = None
    if ig:
        tags_ig = ig.get("hashtags", [])
        desc_ig = ig["legenda"].strip() + (f"\n\n{tags(tags_ig)}" if tags_ig else "")
    comentario = pub.get("comentario_fixado") or (
        "📼 Fontes desta fita:\n" + "\n".join(fontes_urls[:4]) + "\n\nQual história a gente rebobina na próxima?")

    musica_f = ep / "musica.json"
    musica = json.loads(musica_f.read_text()) if musica_f.exists() else None
    if musica:  # a licença CC BY exige o crédito num lugar fácil de achar
        desc_tk += f"\n\n🎵 {musica['credito']}"
        desc_yt += f"\n\n🎵 {musica['credito']}"
        if ig:
            desc_ig += f"\n\n🎵 {musica['credito']}"
    som_tk = ("3. Som: a trilha já está no vídeo. **Não** adicione som do app." if musica else
              f"3. Som: adicionar pela biblioteca do TikTok um som **{pub.get('musica', 'instrumental de suspense/documentário, baixo')}** com volume **≈ 10–15 %** (a narração precisa ficar clara).")
    som_yt = ("3. Som: a trilha já está no vídeo. **Não** adicione som do app." if musica else
              '3. Som (opcional): no app, "Adicionar som" → mesmo clima, volume baixo.')

    avisos = []
    if len(desc_tk) > 2200: avisos.append(f"legenda do TikTok com {len(desc_tk)} caracteres (máx. 2200)")
    if not 3 <= len(tk["hashtags"]) <= 6: avisos.append("TikTok: use de 3 a 6 hashtags")
    if len(titulo_yt) > 100: avisos.append(f"título do YouTube com {len(titulo_yt)} caracteres (máx. 100)")
    elif len(titulo_yt) > 70: avisos.append(f"título do YouTube com {len(titulo_yt)} caracteres (ideal ≤ 70, senão corta no celular)")
    if len(desc_yt) > 5000: avisos.append("descrição do YouTube passa de 5000 caracteres")
    if not any(t.lower() == "#shorts" for t in yt["hashtags"]): avisos.append("YouTube: inclua #shorts")
    if any(" " in t for t in tk["hashtags"] + yt["hashtags"]): avisos.append("hashtag com espaço")
    chave = yt.get("palavra_chave", "").lower()
    if not chave: avisos.append("YouTube: falta palavra_chave em publicacao.json (escolha com ferramentas/sinais.py)")
    elif titulo_yt.lower().find(chave) == -1 or titulo_yt.lower().find(chave) > len(titulo_yt) // 2:
        avisos.append(f'YouTube: "{chave}" precisa estar na primeira metade do título')
    if chave and chave not in tk["legenda"].lower(): avisos.append(f'TikTok: "{chave}" não aparece na legenda (o valor de busca conta no pagamento)')

    if ig:
        if len(desc_ig) > 2200: avisos.append(f"legenda do Instagram com {len(desc_ig)} caracteres (máx. 2200)")
        n_tags_ig = len(tags_ig) + len(re.findall(r"#\w+", ig["legenda"]))
        if n_tags_ig > 5: avisos.append(f"Instagram: {n_tags_ig} hashtags (máx. 5, contando as do texto)")
        if any(" " in t for t in tags_ig): avisos.append("hashtag com espaço")
        if difflib.SequenceMatcher(None, ig["legenda"].strip().lower(), tk["legenda"].strip().lower()).ratio() > 0.8:
            avisos.append("legenda do Instagram quase igual à do TikTok: reescreva")

    for f in ["TIKTOK.txt", "YOUTUBE.txt"]:
        (dst / f).unlink(missing_ok=True)
    (dst / "DESCRICAO-TIKTOK.txt").write_text(desc_tk + "\n")
    (dst / "TITULO-YOUTUBE.txt").write_text(titulo_yt + "\n")
    (dst / "DESCRICAO-YOUTUBE.txt").write_text(desc_yt + "\n")
    (dst / "COMENTARIO-FIXADO.txt").write_text(comentario + "\n")
    if ig:
        (dst / "DESCRICAO-INSTAGRAM.txt").write_text(desc_ig + "\n")
    else:  # não deixa sobrar texto de uma versão anterior do publicacao.json
        (dst / "DESCRICAO-INSTAGRAM.txt").unlink(missing_ok=True)
    textos_ig = f"""## Instagram Reels — legenda (cole inteira)
```
{desc_ig}
```

""" if ig else ""
    redes_comentario = "TikTok, YouTube e Instagram" if ig else "TikTok e YouTube"
    som_ig = ("3. Som: a trilha já está no vídeo. **Não** adicione música do app." if musica else
              "3. Som (opcional): adicionar música do app no mesmo clima, volume baixo.")
    checklist_ig = f"""## Instagram Reels (app do Instagram)
1. Criar um Reel com `{nome}`. Capa: `capa.jpg` ou o primeiro frame.
2. Colar a legenda inteira de `DESCRICAO-INSTAGRAM.txt` (já tem as hashtags e o crédito da música).
{som_ig}
4. Configurações avançadas → ativar o **rótulo de IA** (a narração é voz sintética).
5. Compartilhar.
6. Comentar o texto de `COMENTARIO-FIXADO.txt` e fixar.

""" if ig else ""
    links_publicado = "tiktok=<link> youtube=<link>" + (" instagram=<link>" if ig else "")
    (dst / "TEXTOS.md").write_text(f"""# Textos para publicar — Rebobina {rot['id']}

## TikTok — legenda (cole inteira)
```
{desc_tk}
```

## YouTube Shorts — título
```
{titulo_yt}
```

## YouTube Shorts — descrição (cole inteira)
```
{desc_yt}
```

{textos_ig}## Comentário fixado ({redes_comentario})
```
{comentario}
```
""")
    fontes = "\n".join(f"- {u}" for u in fontes_urls)
    (dst / "CHECKLIST.md").write_text(f"""# Publicar: Rebobina {rot['id']} · {rot['slug']}

Arquivo: `{nome}` · capa: `capa.jpg` · horário sugerido: {pub.get('horario', '19h (Brasília)')}

## TikTok (app ou tiktok.com/tiktokstudio/upload)
1. Enviar `{nome}`. Capa: usar `capa.jpg` se o app deixar enviar imagem; se não, o primeiro frame.
2. Colar a legenda inteira de `DESCRICAO-TIKTOK.txt` (já tem as hashtags).
{som_tk}
4. Mais opções → ativar **"Conteúdo gerado por IA"** (a narração é voz sintética).
5. Permitir comentários, Dueto e Costura. Publicar.
6. Comentar o texto de `COMENTARIO-FIXADO.txt` e fixar o comentário.

## YouTube Shorts (app do YouTube ou studio.youtube.com)
1. Enviar `{nome}` (vertical e com menos de 3 min ⇒ vira Short automaticamente).
2. Título de `TITULO-YOUTUBE.txt`; descrição inteira de `DESCRICAO-YOUTUBE.txt` (já tem as hashtags).
{som_yt}
4. "Conteúdo alterado ou sintético": **Não** (animação gráfica, nada realista). Público: não é conteúdo para crianças.
5. Publicar.
6. Comentar o texto de `COMENTARIO-FIXADO.txt` e fixar.

{checklist_ig}## Depois de publicar
Cole os links aqui e rode:
`python3 ferramentas/pacote_publicacao.py episodios/{ep.name} --publicado {links_publicado}`

## Fontes (para responder comentários)
{fontes}
""")
    print(f"✓ pacote pronto em {dst.relative_to(RAIZ)}/: {nome}, capa.jpg, TEXTOS.md, DESCRICAO-TIKTOK.txt, "
          f"TITULO-YOUTUBE.txt, DESCRICAO-YOUTUBE.txt, {'DESCRICAO-INSTAGRAM.txt, ' if ig else ''}COMENTARIO-FIXADO.txt, CHECKLIST.md")
    for a in avisos:
        print(f"⚠ {a}")
    print("\n" + (dst / "TEXTOS.md").read_text())


if __name__ == "__main__":
    main()
