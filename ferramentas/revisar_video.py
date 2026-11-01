#!/usr/bin/env python3
"""Mede o vídeo renderizado e gera as folhas de frames para o agente revisor-frames.

Uso:
    python3 ferramentas/revisar_video.py episodios/001-acre-cavalo [render/rascunho.mp4]

Gera em <ep>/revisao/:
    metricas.json        duração, resolução, fps, áudio (LUFS, pico), trechos pretos/congelados, veredito
    folha-01.jpg …       2 frames por segundo, 30 por folha (15 s), com as zonas proibidas desenhadas
    chave/<cena>-*.jpg   3 frames por cena (início, meio, fim) em tamanho real, para ler texto
As zonas desenhadas: vermelho = UI do app (topo < 168 px, base > 1330 px, trilho direito
x > 940 entre y 700–1600); amarelo = faixa das legendas (1110–1300).
"""
import json, re, subprocess, sys
from pathlib import Path

MIN_TIKTOK, MIN_SEGURO, MAX_IDEAL, MAX_SHORTS = 60.0, 65.0, 120.0, 180.0


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    ep = Path(sys.argv[1]).resolve()
    video = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if video and not video.is_absolute():
        video = ep / video
    if not video:
        cands = sorted((ep / "render").glob("*.mp4"), key=lambda p: p.stat().st_mtime)
        if not cands:
            sys.exit("✗ nenhum .mp4 em render/. Renderize antes.")
        video = cands[-1]
    out = ep / "revisao"
    (out / "chave").mkdir(parents=True, exist_ok=True)
    for f in list(out.glob("folha-*.jpg")) + list((out / "chave").glob("*.jpg")):
        f.unlink()

    probe = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
                            "-of", "json", str(video)]).stdout)
    dur = float(probe["format"]["duration"])
    v = next(s for s in probe["streams"] if s["codec_type"] == "video")
    tem_audio = any(s["codec_type"] == "audio" for s in probe["streams"])
    num, den = map(int, v["r_frame_rate"].split("/"))
    m = {"video": str(video.relative_to(ep)), "duracao": round(dur, 2), "largura": v["width"], "altura": v["height"],
         "fps": round(num / den, 2), "tem_audio": tem_audio, "problemas": [], "avisos": []}

    # duração (regra que define a monetização)
    if dur <= MIN_TIKTOK:
        m["problemas"].append(f"P0 duração {dur:.1f}s: o TikTok só paga vídeos com MAIS de 60 s")
    elif dur < MIN_SEGURO:
        m["problemas"].append(f"P0 duração {dur:.1f}s: abaixo da margem de segurança de 65 s")
    elif dur > MAX_SHORTS:
        m["problemas"].append(f"P0 duração {dur:.1f}s: o Shorts aceita no máximo 3 min")
    elif dur > MAX_IDEAL:
        m["avisos"].append(f"P1 duração {dur:.1f}s: acima do ideal de 90 s (retenção cai)")
    if (v["width"], v["height"]) != (1080, 1920):
        m["problemas"].append(f"P0 resolução {v['width']}x{v['height']}: precisa ser 1080x1920")
    tempos = ep / "tempos.json"
    if tempos.exists():
        esperado = json.loads(tempos.read_text())["duracao_video"]
        if abs(esperado - dur) > 0.25:
            m["problemas"].append(f"P0 duração {dur:.2f}s ≠ esperado {esperado:.2f}s (render cortado?)")

    # áudio
    if not tem_audio:
        m["problemas"].append("P0 o vídeo não tem trilha de áudio")
    else:
        e = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
        lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", e)
        peak = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)
        m["lufs"] = float(lufs[-1]) if lufs else None
        m["pico_dbtp"] = float(peak[-1]) if peak else None
        if m["lufs"] is not None and not (-18 <= m["lufs"] <= -12):
            m["avisos"].append(f"P1 volume {m['lufs']} LUFS (alvo −16 a −14)")
        if m["pico_dbtp"] is not None and m["pico_dbtp"] > -0.5:
            m["avisos"].append(f"P1 pico {m['pico_dbtp']} dBTP (pode distorcer; alvo ≤ −1)")
        s = run(["ffmpeg", "-hide_banner", "-i", str(video), "-af", "silencedetect=noise=-45dB:d=1.5", "-f", "null", "-"]).stderr
        sil = [(float(a), float(b)) for a, b in zip(re.findall(r"silence_start: ([\d.]+)", s), re.findall(r"silence_end: ([\d.]+)", s))]
        sil = [x for x in sil if x[1] < dur - 2.0]
        if sil:
            m["avisos"].append(f"P1 silêncio longo em {', '.join(f'{a:.1f}–{b:.1f}s' for a, b in sil)}")

    # imagem: trechos pretos e congelados
    b = run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf", "blackdetect=d=0.3:pix_th=0.08", "-an", "-f", "null", "-"]).stderr
    pretos = [(float(a), float(c)) for a, c in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", b)]
    pretos = [p for p in pretos if p[0] < dur - 1.0]
    if pretos:
        m["problemas"].append(f"P0 tela preta em {', '.join(f'{a:.1f}–{c:.1f}s' for a, c in pretos)}")
    fz = run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf", "crop=1080:1100:0:300,freezedetect=n=0.002:d=3", "-an", "-f", "null", "-"]).stderr
    congel = re.findall(r"freeze_start: ([\d.]+).*?freeze_end: ([\d.]+)", fz, re.S)
    if congel:
        m["avisos"].append(f"P1 palco parado ≥ 3 s em {', '.join(f'{float(a):.1f}–{float(c):.1f}s' for a, c in congel)}")

    # folhas de contato com zonas desenhadas
    zonas = ("drawbox=x=0:y=0:w=1080:h=168:color=red@0.35:t=fill,"
             "drawbox=x=0:y=1330:w=1080:h=590:color=red@0.25:t=fill,"
             "drawbox=x=940:y=700:w=140:h=900:color=red@0.25:t=fill,"
             "drawbox=x=0:y=1110:w=1080:h=190:color=yellow@0.9:t=4")
    relogio = "drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,"
    for rel in (relogio, ""):  # o ffmpeg do Homebrew pode vir sem drawtext: sem relógio, cada folha ainda cobre 15 s
        run(["ffmpeg", "-y", "-hide_banner", "-i", str(video), "-vf",
             f"fps=2,{zonas},scale=216:384,{rel}tile=6x5:padding=4:color=0x333333",
             "-q:v", "3", str(out / "folha-%02d.jpg")])
        if list(out.glob("folha-*.jpg")):
            break
    m["folhas"] = sorted(p.name for p in out.glob("folha-*.jpg"))

    # frames-chave por cena, em tamanho real
    if tempos.exists():
        t = json.loads(tempos.read_text())
        for c in t["cenas"]:
            for nome, ts in (("a-inicio", c["inicio"] + 0.35), ("b-meio", (c["inicio"] + c["fim"]) / 2), ("c-fim", c["fim"] - 0.1)):
                run(["ffmpeg", "-y", "-hide_banner", "-ss", f"{max(ts, 0):.2f}", "-i", str(video), "-frames:v", "1", "-q:v", "3",
                     str(out / "chave" / f"{c['id']}-{nome}.jpg")])
    m["veredito"] = "REPROVADO" if m["problemas"] else "APROVADO NAS MÉTRICAS (falta a revisão visual)"
    (out / "metricas.json").write_text(json.dumps(m, ensure_ascii=False, indent=1))
    print(f"{'✗' if m['problemas'] else '✓'} {video.name}: {dur:.1f}s · {v['width']}x{v['height']} · {m['fps']}fps · "
          f"áudio {m.get('lufs')} LUFS / pico {m.get('pico_dbtp')} dBTP")
    for p in m["problemas"] + m["avisos"]:
        print("  ", p)
    print(f"   folhas: {len(m['folhas'])} em {out.relative_to(ep.parent.parent)}/ · frames-chave em revisao/chave/")


if __name__ == "__main__":
    main()
