# Roda DENTRO da VM do Colab, enviado por ferramentas/testar_pronuncia.sh. Gera uma faixa por grafia candidata
# com a voz do canal, sempre com a mesma semente, para a comparação ser só da grafia.
import json, os, zipfile
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

BASE = "/content/rebobina"
SEMENTE = 7
assert torch.cuda.is_available(), "sem GPU — crie a sessão com --gpu T4"
DTYPE = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
clone = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base", device_map="cuda:0",
                                      dtype=DTYPE, attn_implementation="sdpa")
ref_txt = open(f"{BASE}/voz-rebobina.txt", encoding="utf-8").read().strip()
prompt = clone.create_voice_clone_prompt(ref_audio=f"{BASE}/voz-rebobina.wav", ref_text=ref_txt)
os.makedirs(f"{BASE}/teste", exist_ok=True)
for item in json.load(open(f"{BASE}/candidatos.json", encoding="utf-8")):
    for n, opcao in enumerate(item["opcoes"]):
        torch.manual_seed(SEMENTE)
        wavs, sr = clone.generate_voice_clone(text=item["frase"].replace("{}", opcao), language="Portuguese",
                                              voice_clone_prompt=prompt)
        sf.write(f"{BASE}/teste/{item['id']}-{n}.wav", wavs[0], sr)
        print("✓", item["id"], n, opcao, flush=True)
with zipfile.ZipFile(f"{BASE}/teste.zip", "w") as z:
    for f in sorted(os.listdir(f"{BASE}/teste")):
        z.write(f"{BASE}/teste/{f}", f)
print("TESTE_OK")
