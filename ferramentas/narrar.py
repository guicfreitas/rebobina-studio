#!/usr/bin/env python3
"""Gera a narração de um episódio e o tempo de cada cena e de cada palavra.

Uso:
    python3 ferramentas/narrar.py episodios/001-acre-cavalo [--motor kokoro|elevenlabs|gravacao]

Entrada:  <ep>/roteiro.json  (campo "cenas"[].fala, opcional "fala_tts" com grafia fonética, "voz", "velocidade")
Saída:    <ep>/assets/voz/narracao.wav   (áudio final, mono 44.1 kHz)
          <ep>/tempos.json               (início/fim de cada cena e de cada palavra)

Motores:
  kokoro      voz local grátis via `npx hyperframes tts`. Uma fala por cena.
  elevenlabs  precisa de ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID no ambiente ou em .env.
  colab       (padrão) Qwen3-TTS numa GPU T4 do Google Colab, comandada pelo terminal com o
              Colab CLI (ferramentas/narrar_colab.sh). Automático: liga a GPU, narra, baixa, desliga.
  arquivos    uma faixa pronta por cena (ex.: do notebook ferramentas/colab/narracao_qwen3.ipynb):
              o zip narracao-*.zip ou c01.wav, c02.wav… em <ep>/assets/voz/ (ou assets/voz/cenas/).
  gravacao    sua própria voz: grave tudo em <ep>/assets/voz/gravacao.wav (ou .m4a/.mp3).
              Exige transcrição (whisper-cpp: `brew install whisper-cpp`).

Pausas: cada faixa perde o silêncio das pontas e tem as pausas internas reduzidas a PAUSA_MAX
(PAUSA_APOS_PONTO depois de ponto final), sem mexer na velocidade nem nas palavras. A voz é reconhecida
por dois envelopes, o geral e o de agudos: o "s" final é fraco no geral e forte nos agudos.

Tempos das palavras: cada faixa é transcrita (whisper-cli) e alinhada ao texto do roteiro; depois os
tempos são encaixados nos trechos em que há voz, de modo que nenhuma palavra começa em silêncio.
Palavra casada com a transcrição fica com "medido": true. O resto ("medido": false) é estimado por
sílabas no intervalo entre as palavras medidas: números por extenso (o whisper devolve algarismos),
nomes que ele não reconheceu e trechos sem transcrição.
"""
import argparse, array, difflib, json, math, os, re, shutil, subprocess, sys, unicodedata, urllib.request, wave, zipfile
from pathlib import Path
from pronuncia import aplicar_roteiro

GAP_ENTRE_CENAS = 0.28   # respiro entre falas (s)
INICIO = 0.15            # a primeira palavra começa aqui (legenda em 0 parece pré-existente)
CAUDA = 2.0             # segundos após a última palavra (a frase final respira + assinatura STOP)
PAUSA_MAX = 0.30         # limite das pausas dentro de uma faixa (s)
PAUSA_APOS_PONTO = 0.40  # limite depois de . ! ? … (s)
MARGEM_INICIO = 0.08     # silêncio mantido antes da primeira palavra da faixa (s)
MARGEM_FIM = 0.12        # silêncio mantido depois da última palavra da faixa (s)
LIMIAR_VOZ = -30         # dB abaixo do pico do envelope geral; acima disso é voz
LIMIAR_AGUDOS = -52      # dB abaixo do mesmo pico, medido acima de 3 kHz (é o que segura "s" e "x" finais)
JANELA = 0.01            # passo dos envelopes (s)
TOLERANCIA = 0.30         # distância máxima entre o tempo do whisper e a estimativa por sílabas no bloco de fala (s)
FRONTEIRA_MIN = 0.18     # silêncio a partir do qual uma pausa é tratada como divisa entre palavras (s)


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def duracao(wav):
    out = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)])
    return float(out.stdout.strip())


def envelope(wav, filtro=None):
    """Nível em dB a cada JANELA segundos."""
    cmd = ["ffmpeg", "-v", "error", "-i", str(wav)] + (["-af", filtro] if filtro else []) + ["-f", "s16le", "-ac", "1", "-ar", "44100", "-"]
    amostras = array.array("h", subprocess.run(cmd, check=True, capture_output=True).stdout)
    n = int(44100 * JANELA)
    return [10 * math.log10(sum(v * v for v in amostras[i:i + n]) / n / 32768 ** 2 + 1e-12) for i in range(0, len(amostras) - n + 1, n)]


def trechos_voz(wav):
    """Lista de (inicio, fim) com voz. O piso de ruído das faixas fica em torno de -47 dB, longe do digital."""
    geral, agudos = envelope(wav), envelope(wav, "highpass=f=3000,highpass=f=3000")
    pico = max(geral, default=0)
    voz = [g > pico + LIMIAR_VOZ or h > pico + LIMIAR_AGUDOS for g, h in zip(geral, agudos)]
    ilhas, i = [], 0
    while i < len(voz):
        if voz[i]:
            j = i
            while j < len(voz) and voz[j]:
                j += 1
            ilhas.append([i, j])
            i = j
        else:
            i += 1
    unidas = []
    for ini, fim in ilhas:  # oclusivas (t, p, k) abrem furos curtos dentro da palavra
        if unidas and (ini - unidas[-1][1]) * JANELA < 0.05:
            unidas[-1][1] = fim
        else:
            unidas.append([ini, fim])

    def e_ruido(k):  # clique ou respiração: curto, fraco e afastado do resto
        ini, fim = unidas[k]
        ant = (ini - unidas[k - 1][1]) * JANELA if k else 9
        prox = (unidas[k + 1][0] - fim) * JANELA if k + 1 < len(unidas) else 9
        return (fim - ini) * JANELA < 0.12 and max(geral[ini:fim]) < pico - 20 and min(ant, prox) >= 0.15
    limpas = [u for k, u in enumerate(unidas) if not e_ruido(k)] or unidas

    # ruído antes da primeira fala: tudo o que é fraco e está separado da voz por uma pausa fica de fora.
    # Um "s" inicial, também fraco no geral, vem colado na vogal e continua dentro.
    forte = next((k for k, (ini, fim) in enumerate(limpas) if max(geral[ini:fim]) >= pico - 20), 0)
    while forte and (limpas[forte][0] - limpas[forte - 1][1]) * JANELA < 0.15:
        forte -= 1
    limpas = limpas[forte:]
    return [(ini * JANELA, fim * JANELA) for ini, fim in limpas] or [(0.0, len(voz) * JANELA)]


def cortar_pausas(bruto, saida, ilhas, alvos):
    """Grava a faixa sem o silêncio das pontas e com cada pausa i limitada a alvos[i].
    Só retira o miolo do silêncio. Devolve os trechos de voz na nova linha do tempo."""
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(bruto), "-f", "s16le", "-ac", "1", "-ar", "44100", "-"],
                         check=True, capture_output=True).stdout
    a = array.array("h", pcm)
    sr, x = 44100, int(44100 * 0.01)  # emenda de 10 ms
    amostra = lambda s: min(max(int(round(s * sr)), 0), len(a))
    pos = amostra(ilhas[0][0] - MARGEM_INICIO)
    saidas, novas = array.array("h"), []
    for k, (ini, fim) in enumerate(ilhas):
        i0, i1 = amostra(ini), amostra(fim)
        saidas.extend(a[pos:i0])
        novo_ini = len(saidas) / sr
        saidas.extend(a[i0:i1])
        novas.append((novo_ini, len(saidas) / sr))
        pos = i1
        if k + 1 == len(ilhas):
            break
        prox = amostra(ilhas[k + 1][0])
        alvo = int(alvos[k] * sr)
        if prox - i1 > alvo + 2 * x:
            cab = int(alvo * 0.6)  # a palavra que acaba fica com mais ar que a que começa
            saidas.extend(a[i1:i1 + cab])
            resto = alvo - cab
            for n in range(x):  # silêncio com silêncio; a rampa só evita degrau no ruído de fundo
                f = n / x
                saidas.append(int(a[i1 + cab + n] * (1 - f) + a[prox - resto - x + n] * f))
            saidas.extend(a[prox - resto:prox])
            pos = prox
    saidas.extend(a[pos:amostra(ilhas[-1][1] + MARGEM_FIM)])
    with wave.open(str(saida), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(saidas.tobytes())
    return novas


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def silabas(w):
    v = re.findall(r"[aeiouáéíóúâêôãõày]+", w.lower())
    return max(1, len(v))


def distribuir(palavras, ini, fim):
    """Reparte [ini, fim] entre as palavras por sílabas. Devolve [(inicio, fim), ...]."""
    pesos = [silabas(w) + 0.35 for w in palavras]
    t, total, out = ini, sum(pesos) or 1, []
    for p in pesos:
        d = max(fim - ini, 0) * p / total
        out.append((t, t + d))
        t += d
    return out


UNIDADES = ("zero um dois três quatro cinco seis sete oito nove dez onze doze treze catorze quinze dezesseis "
            "dezessete dezoito dezenove").split()
DEZENAS = "_ _ vinte trinta quarenta cinquenta sessenta setenta oitenta noventa".split()
CENTENAS = "_ cento duzentos trezentos quatrocentos quinhentos seiscentos setecentos oitocentos novecentos".split()


def extenso(n):
    """Número por extenso, como o roteiro escreve o que o whisper devolve em algarismos (1692, 329…)."""
    if n < 20:
        return UNIDADES[n]
    if n < 100:
        return DEZENAS[n // 10] + (" e " + UNIDADES[n % 10] if n % 10 else "")
    if n == 100:
        return "cem"
    if n < 1000:
        return CENTENAS[n // 100] + (" e " + extenso(n % 100) if n % 100 else "")
    mil = "mil" if n // 1000 == 1 else extenso(n // 1000) + " mil"
    r = n % 1000
    if not r:
        return mil
    return mil + (" e " if r < 100 or r % 100 == 0 else " ") + extenso(r)


def tts_kokoro(texto, voz, velocidade, saida):
    sh(["npx", "--yes", "hyperframes", "tts", texto, "--voice", voz, "--speed", str(velocidade), "-o", str(saida)])


def carregar_env(ep):
    for d in [ep, *ep.parents][:4]:
        f = d / ".env"
        if f.exists():
            for linha in f.read_text().splitlines():
                if "=" in linha and not linha.strip().startswith("#"):
                    k, v = linha.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"'))


def tts_elevenlabs(texto, saida):
    key, voz = os.environ.get("ELEVENLABS_API_KEY"), os.environ.get("ELEVENLABS_VOICE_ID")
    if not key or not voz:
        sys.exit("✗ Defina ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID no .env do projeto.")
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voz}",
        data=json.dumps({"text": texto, "model_id": "eleven_multilingual_v2"}).encode(),
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    mp3 = saida.with_suffix(".mp3")
    mp3.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    sh(["ffmpeg", "-y", "-i", str(mp3), "-ac", "1", "-ar", "44100", str(saida)])
    mp3.unlink()


def transcrever(ep, wav):
    """Tenta medir o tempo real de cada palavra. Retorna lista ou None."""
    try:
        sh(["npx", "--yes", "hyperframes", "transcribe", str(wav), "--model", "small", "--language", "pt", "--json"], cwd=ep, timeout=900)
        t = json.loads((ep / "assets" / "transcript.json").read_text())
        palavras = t if isinstance(t, list) else t.get("words", [])
        return [w for w in palavras if norm(w.get("text", ""))] or None
    except Exception as e:  # whisper ausente, modelo indisponível etc.
        return transcrever_cpu(wav) or print(f"  (transcrição indisponível: {str(e)[:120]} — usando estimativa)")


def transcrever_cpu(wav):
    """Plano B: o whisper-cli do HyperFrames sem GPU (no Mac Intel ele aborta no backend Metal)."""
    cache = Path.home() / ".cache" / "hyperframes" / "whisper"
    cli, modelo = cache / "whisper.cpp" / "build" / "bin" / "whisper-cli", cache / "models" / "ggml-small.bin"
    if not cli.exists() or not modelo.exists():
        return None
    tmp = wav.with_name("_transcricao")
    try:
        sh(["ffmpeg", "-y", "-i", str(wav), "-ar", "16000", "-ac", "1", f"{tmp}.wav"])
        sh([str(cli), "-m", str(modelo), "-f", f"{tmp}.wav", "-l", "pt", "-ng", "-ml", "1", "-sow", "-oj", "-of", str(tmp)], timeout=900)
        segs = json.loads(Path(f"{tmp}.json").read_text())["transcription"]
        return [{"text": s["text"].strip(), "start": s["offsets"]["from"] / 1000, "end": s["offsets"]["to"] / 1000}
                for s in segs if norm(s["text"])] or None
    except Exception:
        return None
    finally:
        Path(f"{tmp}.wav").unlink(missing_ok=True)
        Path(f"{tmp}.json").unlink(missing_ok=True)


def alinhar(script_words, trans, fim=None):
    """Tempo de cada palavra do roteiro: [(inicio, fim, medido), ...]. medido=True só para a palavra casada
    com uma palavra transcrita. As outras (números em algarismos, nomes não reconhecidos) são repartidas por
    sílabas entre as vizinhas medidas. `fim` é o fim do áudio, para as palavras depois da última medida."""
    b = []  # transcrição com os algarismos por extenso; a palavra do número não conta como âncora
    for tw in trans or []:
        n = norm(tw["text"])
        if n.isdigit() and int(n) < 10000:
            b += [(norm(x), None) for x in extenso(int(n)).split()]
        elif n:
            b.append((n, (float(tw["start"]), float(tw["end"]))))
    a = [norm(w) for w in script_words]
    ponto = lambda x, y: 2.0 if x == y else (1.2 if difflib.SequenceMatcher(None, x, y).ratio() >= 0.6 else None)
    # alinhamento global: tolera palavra ouvida errado ("Massachussi", "Inglês")
    L, C = len(a), len(b)
    nota = [[0.0] * (C + 1) for _ in range(L + 1)]
    for i in range(1, L + 1):
        for j in range(1, C + 1):
            p = ponto(a[i - 1], b[j - 1][0])
            nota[i][j] = max(nota[i - 1][j], nota[i][j - 1], nota[i - 1][j - 1] + p if p else 0.0)
    ancora, i, j = [None] * L, L, C
    while i and j:
        p = ponto(a[i - 1], b[j - 1][0])
        if p and abs(nota[i][j] - nota[i - 1][j - 1] - p) < 1e-9:
            ancora[i - 1] = b[j - 1][1]
            i, j = i - 1, j - 1
        elif nota[i - 1][j] >= nota[i][j - 1]:
            i -= 1
        else:
            j -= 1
    tempos, i = [None] * L, 0
    while i < L:
        if ancora[i]:
            tempos[i] = (ancora[i][0], ancora[i][1], True)
            i += 1
            continue
        j = i
        while j < L and not ancora[j]:
            j += 1
        ini = tempos[i - 1][1] if i else 0.0
        if j < L:
            lim = ancora[j][0]
        else:
            lim = max(fim if fim is not None else 0.0, ini + 0.3 * sum(silabas(w) for w in script_words[i:j]))
        for k, (s, e) in enumerate(distribuir(script_words[i:j], ini, max(lim, ini))):
            tempos[i + k] = (s, e, False)
        i = j
    return tempos


def escolher_fronteiras(palavras, tempos, pausas):
    """Diz qual divisa entre palavras cada pausa é: {índice da pausa: índice da palavra antes dela}.
    O whisper erra perto das pausas, mas a ordem é fixa e pausa cai quase sempre em pontuação."""
    custo = lambda p, k: abs((pausas[p][0] + pausas[p][1]) / 2 - (tempos[k][1] + tempos[k + 1][0]) / 2) - \
        (0.6 if re.search(r"[.,;:!?…]$", palavras[k]) else 0)
    PULA = 0.3
    n, m = len(pausas), len(palavras) - 1
    INF = 1e9
    # d[p][k]: menor custo das p primeiras pausas usando só as k primeiras divisas
    d = [[0.0] * (m + 1)] + [[INF] * (m + 1) for _ in range(n)]
    for p in range(1, n + 1):
        d[p][0] = p * PULA
        for k in range(1, m + 1):
            d[p][k] = min(d[p][k - 1], d[p - 1][k] + PULA, d[p - 1][k - 1] + custo(p - 1, k - 1))
    esc, p, k = {}, n, m
    while p and k:
        if d[p][k] == d[p][k - 1]:
            k -= 1
        elif d[p][k] == d[p - 1][k] + PULA:
            p -= 1
        else:
            esc[p - 1] = k - 1
            p, k = p - 1, k - 1
    return esc


def encaixar_na_voz(palavras, tempos, ilhas):
    """Põe os tempos dentro dos trechos com voz. Devolve (tempos, {índice da ilha antes da pausa: palavra antes dela})."""
    idx = [k for k in range(len(ilhas) - 1) if ilhas[k + 1][0] - ilhas[k][1] >= FRONTEIRA_MIN]
    pausas = [(ilhas[k][1], ilhas[k + 1][0]) for k in idx]
    esc = escolher_fronteiras(palavras, tempos, pausas) if pausas and len(palavras) > 1 else {}
    # blocos de fala: cada um é contínuo e tem as suas palavras
    blocos, ini_b, ini_p = [], ilhas[0][0], 0
    for p in sorted(esc):
        blocos.append((ini_b, pausas[p][0], ini_p, esc[p] + 1))
        ini_b, ini_p = pausas[p][1], esc[p] + 1
    blocos.append((ini_b, ilhas[-1][1], ini_p, len(palavras)))
    out = [None] * len(palavras)
    for bi, bf, pi, pf in blocos:
        # num bloco curto as sílabas erram pouco; o whisper às vezes erra 0,5 s. Vale o medido que concorda com elas.
        base = distribuir(palavras[pi:pf], bi, bf)
        marcos = [(pi, bi, tempos[pi][2])]
        for k in range(pi + 1, pf):
            s, _, medido = tempos[k]
            cabe = s - marcos[-1][1] >= 0.07 * sum(silabas(w) for w in palavras[marcos[-1][0]:k])
            if medido and abs(s - base[k - pi][0]) <= TOLERANCIA and cabe:
                marcos.append((k, s, True))
        marcos.append((pf, bf, False))
        for (k0, s0, med), (k1, s1, _) in zip(marcos, marcos[1:]):
            for n, (s, e) in enumerate(distribuir(palavras[k0:k1], s0, s1)):
                out[k0 + n] = (s, e, med and n == 0)
    # palavra não começa em silêncio: um furo que sobrou no bloco empurra o início para a voz
    corrigidas = []
    for k, (s, e, medido) in enumerate(out):
        furo = next((il for il in ilhas if il[0] <= s < il[1]), None)
        if furo is None:
            prox = next((il[0] for il in ilhas if il[0] > s), None)
            if prox is not None and prox < e:
                s = prox
        ant = next((il[1] for il in reversed(ilhas) if il[1] <= e), None)
        dentro = next((il for il in ilhas if il[0] < e <= il[1]), None)
        if dentro is None and ant is not None and ant > s:
            e = ant
        corrigidas.append((s, max(e, s + 0.02), medido))
    return corrigidas, {idx[p]: k for p, k in esc.items()}


def preparar_faixa(bruto, limpo, palavras, transcrever_faixa):
    """Corta as pausas de uma faixa e mede as palavras nela. Devolve (tempos locais, faixa transcrita?)."""
    ilhas = trechos_voz(bruto)
    alvos = [PAUSA_MAX] * (len(ilhas) - 1)
    novas = cortar_pausas(bruto, limpo, ilhas, alvos)
    trans = transcrever_cpu(limpo) if transcrever_faixa else None
    d = duracao(limpo)
    tempos, fronteiras = encaixar_na_voz(palavras, alinhar(palavras, trans, fim=d), novas)
    # segunda passada: a pausa depois de ponto final recebe um pouco mais de ar, se a faixa tinha esse ar
    extras = {}
    for k, w in fronteiras.items():
        if re.search(r"[.!?…]$", palavras[w]):
            original = ilhas[k + 1][0] - ilhas[k][1]
            alvo = min(PAUSA_APOS_PONTO, original)
            if alvo > PAUSA_MAX:
                alvos[k] = alvo
                extras[novas[k][1]] = alvo - PAUSA_MAX
    if extras:
        cortar_pausas(bruto, limpo, ilhas, alvos)
        def desloca(x):
            return x + sum(v for fim, v in extras.items() if fim < x)
        tempos = [(desloca(s), desloca(e), m) for s, e, m in tempos]
    return tempos, bool(trans)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodio")
    ap.add_argument("--motor", default=None, choices=["kokoro", "elevenlabs", "gravacao", "arquivos", "colab"])
    ap.add_argument("--sem-transcricao", action="store_true", help="força a estimativa de tempos")
    args = ap.parse_args()

    ep = Path(args.episodio).resolve()
    carregar_env(ep)
    rot = aplicar_roteiro(json.loads((ep / "roteiro.json").read_text()))  # dicionário do canal em fala_tts
    voz, vel = rot.get("voz", "pm_alex"), rot.get("velocidade", 1.0)
    vdir = ep / "assets" / "voz"
    vdir.mkdir(parents=True, exist_ok=True)
    motor = args.motor or rot.get("motor_voz", "colab")
    if motor == "colab":
        # sem zip/faixas ainda: gera no Colab pelo terminal (ferramentas/narrar_colab.sh, Colab CLI)
        if not list(vdir.glob("narracao*.zip")) and not (vdir / "cenas").exists():
            script = Path(__file__).resolve().parent / "narrar_colab.sh"
            print("▶ sem narração do Colab ainda: rodando", script.name)
            r = subprocess.run([str(script), str(ep)])
            if r.returncode != 0:
                sys.exit("✗ narração no Colab falhou. Alternativas: rode de novo, use o notebook "
                         "ferramentas/colab/narracao_qwen3.ipynb, ou --motor kokoro")
        motor = "arquivos"

    cenas = rot["cenas"]
    resultado = {"motor": motor, "voz": voz, "cenas": [], "palavras": []}

    if motor == "gravacao":
        src = next((vdir / f"gravacao{e}" for e in (".wav", ".m4a", ".mp3", ".aac") if (vdir / f"gravacao{e}").exists()), None)
        if not src:
            sys.exit(f"✗ Coloque sua gravação em {vdir}/gravacao.wav (ou .m4a/.mp3).")
        final = vdir / "narracao.wav"
        sh(["ffmpeg", "-y", "-i", str(src), "-ac", "1", "-ar", "44100",
            "-af", f"silenceremove=start_periods=1:start_threshold=-40dB,adelay={int(INICIO*1000)},loudnorm=I=-16:TP=-1.5", str(final)])
        trans = transcrever(ep, final)
        if not trans:
            sys.exit("✗ O modo gravação precisa de transcrição. Instale: brew install whisper-cpp")
        todas = [(ci, w) for ci, c in enumerate(cenas) for w in c["fala"].split()]
        tempos = alinhar([w for _, w in todas], trans)
        for ci, c in enumerate(cenas):
            idx = [k for k, (cj, _) in enumerate(todas) if cj == ci]
            resultado["cenas"].append({"id": c["id"], "inicio": round(tempos[idx[0]][0], 3), "fim": round(tempos[idx[-1]][1], 3)})
        for k, (ci, w) in enumerate(todas):
            resultado["palavras"].append({"id": f"w{k}", "cena": cenas[ci]["id"], "text": w,
                                          "start": round(tempos[k][0], 3), "end": round(tempos[k][1], 3), "medido": tempos[k][2]})
    else:
        t = INICIO
        partes, lista = [], vdir / "concat.txt"
        silencio = vdir / "_gap.wav"
        sh(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(GAP_ENTRE_CENAS), str(silencio)])
        lead = vdir / "_lead.wav"
        sh(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(INICIO), str(lead)])
        partes.append(lead)
        if motor == "arquivos":
            pasta = vdir / "cenas"
            zips = sorted(vdir.glob("narracao*.zip"), key=lambda p: p.stat().st_mtime)
            if zips:
                pasta.mkdir(exist_ok=True)
                with zipfile.ZipFile(zips[-1]) as z:
                    z.extractall(pasta)
                print(f"  usando {zips[-1].name}")
            def fonte(cid):
                for d in (pasta, vdir):
                    for ext in (".wav", ".mp3", ".m4a", ".flac"):
                        f = d / f"{cid}{ext}"
                        if f.exists():
                            return f
                return None
            faltando = [c["id"] for c in cenas if not fonte(c["id"])]
            if faltando:
                sys.exit(f"✗ faltam faixas para: {', '.join(faltando)}. Coloque narracao-*.zip ou cNN.wav em {vdir}")
            originais = {c["id"]: vdir / f"_{c['id']}_orig.wav" for c in cenas}
            for c in cenas:  # copia antes de qualquer coisa: a saída limpa usa o mesmo nome cNN.wav
                sh(["ffmpeg", "-y", "-i", str(fonte(c["id"])), "-ac", "1", "-ar", "44100", str(originais[c["id"]])])
        k, faixas_medidas = 0, 0
        for c in cenas:
            bruto, limpo = vdir / f"_{c['id']}_bruto.wav", vdir / f"{c['id']}.wav"
            print(f"  {'preparando' if motor == 'arquivos' else 'narrando'} {c['id']}: {c['fala'][:60]}…")
            if motor == "kokoro":
                tts_kokoro(c.get("fala_tts", c["fala"]), voz, vel, bruto)
            elif motor == "arquivos":
                originais[c["id"]].replace(bruto)
            else:
                tts_elevenlabs(c.get("fala_tts", c["fala"]), bruto)
            palavras = c["fala"].split()
            tempos, medida = preparar_faixa(bruto, limpo, palavras, not args.sem_transcricao)
            faixas_medidas += medida
            bruto.unlink()
            d = duracao(limpo)
            for w, (s, e, medido) in zip(palavras, tempos):
                resultado["palavras"].append({"id": f"w{k}", "cena": c["id"], "text": w, "start": round(t + s, 3),
                                              "end": round(min(t + e, t + d), 3), "medido": medido}); k += 1
            resultado["cenas"].append({"id": c["id"], "inicio": round(t, 3), "fim": round(t + d, 3)})
            partes += [limpo, silencio]
            t += d + GAP_ENTRE_CENAS
        lista.write_text("".join(f"file '{p.name}'\n" for p in partes[:-1]))
        bruto_total = vdir / "_narracao_bruta.wav"
        sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-c", "copy", str(bruto_total)], cwd=vdir)
        final = vdir / "narracao.wav"
        sh(["ffmpeg", "-y", "-i", str(bruto_total), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", str(final)])
        for p in [bruto_total, lista, silencio, lead]:
            p.unlink(missing_ok=True)
        print(f"  faixas transcritas: {faixas_medidas}/{len(cenas)}")
        if not args.sem_transcricao and not faixas_medidas:
            trans = transcrever(ep, final)
            if trans:
                tempos = alinhar([w["text"] for w in resultado["palavras"]], trans, fim=duracao(final))
                for w, (s, e, medido) in zip(resultado["palavras"], tempos):
                    w["start"], w["end"], w["medido"] = round(s, 3), round(e, 3), medido

    ultimo = max(w["end"] for w in resultado["palavras"])
    resultado["duracao_narracao"] = round(duracao(final), 3)
    resultado["duracao_video"] = round(max(ultimo, resultado["duracao_narracao"]) + CAUDA, 2)
    medidas = sum(bool(w.get("medido")) for w in resultado["palavras"])
    resultado["palavras_medidas"] = medidas
    resultado["tempos_medidos"] = medidas == len(resultado["palavras"])
    (ep / "tempos.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1))
    n = len(resultado["palavras"])
    dv = resultado["duracao_video"]
    print(f"✓ narração: {resultado['duracao_narracao']:.1f}s · {n} palavras · vídeo terá {dv:.1f}s "
          f"({medidas}/{n} medidas; as demais, estimadas por sílabas)")
    if dv < 65:
        print(f"⚠ ABAIXO DE 65 s ({dv:.1f}s): o TikTok só paga vídeos com mais de 60 s. Alongue o roteiro.")
    elif dv > 120:
        print(f"⚠ ACIMA DE 120 s ({dv:.1f}s): enxugue o roteiro.")


if __name__ == "__main__":
    main()
