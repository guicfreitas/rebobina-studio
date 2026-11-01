# Roda DENTRO da VM do Google Colab (GPU T4), enviado por ferramentas/narrar_colab.sh via `colab exec -f`.
# Entrada (enviada antes por `colab upload`):  /content/rebobina/roteiro.json
#                                              /content/rebobina/voz-rebobina.wav + .txt  (opcional)
# Saída:  /content/rebobina/narracao.zip  (c01.wav, c02.wav…)  e, se a voz foi criada agora,
#         /content/rebobina/voz-rebobina.wav + voz-rebobina.txt  (o script local baixa para canal/voz/)
# Modelo: Qwen3-TTS (Alibaba, Apache 2.0). Fluxo oficial "design → clone": a voz do canal é desenhada
# uma vez (VoiceDesign) e clonada em toda cena (Base), para o narrador ser sempre o mesmo.
import json, os, zipfile
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

BASE = "/content/rebobina"
INSTRUCAO_VOZ = ("Brazilian Portuguese male narrator in his 40s, deep warm baritone, neutral Brazilian accent, "
                 "calm documentary pacing with subtle intrigue, very clear diction, natural pauses")
TEXTO_REFERENCIA = ("Toda fita tem um começo. Hoje, a gente rebobina até o momento em que essa história "
                    "aconteceu de verdade, com datas, documentos e mapas.")
SEMENTE = 7

assert torch.cuda.is_available(), "sem GPU — crie a sessão com --gpu T4"
DTYPE = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16  # T4 não tem bf16
ATTN = "sdpa"                                                                   # T4 não roda FlashAttention 2
print("GPU:", torch.cuda.get_device_name(0), "· dtype:", DTYPE)

ref_wav, ref_txt = f"{BASE}/voz-rebobina.wav", f"{BASE}/voz-rebobina.txt"
if os.path.exists(ref_wav) and os.path.exists(ref_txt):
    TEXTO_REFERENCIA = open(ref_txt, encoding="utf-8").read().strip()
    print("voz do canal: usando voz-rebobina.wav enviada")
else:
    print("voz do canal: criando com VoiceDesign (primeira vez)")
    torch.manual_seed(int.from_bytes(os.urandom(2), "big"))  # cada criação sorteia uma voz diferente
    design = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign", device_map="cuda:0",
                                           dtype=DTYPE, attn_implementation=ATTN)
    wavs, sr = design.generate_voice_design(text=TEXTO_REFERENCIA, language="Portuguese", instruct=INSTRUCAO_VOZ)
    sf.write(ref_wav, wavs[0], sr)
    open(ref_txt, "w", encoding="utf-8").write(TEXTO_REFERENCIA)
    del design
    torch.cuda.empty_cache()

roteiro = json.load(open(f"{BASE}/roteiro.json", encoding="utf-8"))
clone = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base", device_map="cuda:0",
                                      dtype=DTYPE, attn_implementation=ATTN)
prompt = clone.create_voice_clone_prompt(ref_audio=ref_wav, ref_text=TEXTO_REFERENCIA)

os.makedirs(f"{BASE}/cenas", exist_ok=True)
for c in roteiro["cenas"]:
    texto = c.get("fala_tts") or c["fala"]
    esperado = len(c["fala"].split()) / 2.7  # ~160 palavras/min
    for tentativa in range(4):               # refaz se sair cortado ou "alucinado"
        torch.manual_seed(SEMENTE + tentativa)
        wavs, sr = clone.generate_voice_clone(text=texto, language="Portuguese", voice_clone_prompt=prompt)
        dur = len(wavs[0]) / sr
        if 0.5 * esperado <= dur <= 1.8 * esperado + 1.0:
            break
        print(f"  {c['id']}: {dur:.1f}s fora do esperado ({esperado:.1f}s), tentando de novo")
    sf.write(f"{BASE}/cenas/{c['id']}.wav", wavs[0], sr)
    print(f"✓ {c['id']} {dur:5.1f}s  {c['fala'][:60]}")

with zipfile.ZipFile(f"{BASE}/narracao.zip", "w") as z:
    for c in roteiro["cenas"]:
        z.write(f"{BASE}/cenas/{c['id']}.wav", f"{c['id']}.wav")
print("NARRACAO_OK")
