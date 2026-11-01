import os,subprocess,sys,textwrap
B="/content/v"
TXT="Dizem que um programa de rádio fez os Estados Unidos entrarem em pânico com uma invasão de marcianos. O programa existiu. O pânico em massa… nem tanto. Por que exagerar? Segundo historiadores, o rádio estava roubando anunciantes dos jornais."
REF=open(f"{B}/ref.txt",encoding="utf-8").read()
open(f"{B}/t.txt","w",encoding="utf-8").write(TXT)
QW=r'''
import torch,soundfile as sf
from qwen_tts import Qwen3TTSModel
B="/content/v";T=open(f"{B}/t.txt",encoding="utf-8").read();R=open(f"{B}/ref.txt",encoding="utf-8").read()
k=dict(device_map="cuda:0",dtype=torch.float16,attn_implementation="sdpa")
m=Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base",**k)
p=m.create_voice_clone_prompt(ref_audio=f"{B}/ref.wav",ref_text=R)
torch.manual_seed(7);w,s=m.generate_voice_clone(text=T,language="Portuguese",voice_clone_prompt=p);sf.write(f"{B}/out/A-qwen-clone-ptbr.wav",w[0],s)
'''
CB=r'''
import torch,torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS as C
B="/content/v";T=open(f"{B}/t.txt",encoding="utf-8").read()
m=C.from_pretrained(device="cuda")
for nome,ex,cfg in (("B-chatterbox-ptbr",0.6,0.4),("C-chatterbox-ptbr-intenso",0.85,0.3)):
    torch.manual_seed(7);w=m.generate(T,language_id="pt",audio_prompt_path=f"{B}/ref_curto.wav",exaggeration=ex,cfg_weight=cfg);ta.save(f"{B}/out/{nome}.wav",w.cpu(),m.sr)
'''
F5=r'''
from huggingface_hub import list_repo_files,hf_hub_download as d
from f5_tts.api import F5TTS
B="/content/v";T=open(f"{B}/t.txt",encoding="utf-8").read();R=open(f"{B}/ref_curto.txt",encoding="utf-8").read()
r="firstpixel/F5-TTS-pt-br";fs=list(list_repo_files(r));print(fs)
c=[f for f in fs if f.endswith((".safetensors",".pt"))][-1]
m=F5TTS(ckpt_file=d(r,c))
m.infer(ref_file=f"{B}/ref_curto.wav",ref_text=R,gen_text=T,file_wave=f"{B}/out/D-f5-ptbr.wav",seed=7)
'''
def rodar(nome,cod,pacotes):
    py=sys.executable
    if pacotes:
        subprocess.run([py,"-m","pip","install","-q","uv"],check=True)
        subprocess.run([py,"-m","uv","venv","--seed","--python","3.11",f"/content/{nome}"],check=True)
        py=f"/content/{nome}/bin/python"
        i=subprocess.run([py,"-m","pip","install","-q",*pacotes],capture_output=True,text=True);print(nome,"pip",i.returncode,i.stderr[-400:])
    f=f"{B}/{nome}.py";open(f,"w",encoding="utf-8").write(cod)
    r=subprocess.run([py,f],capture_output=True,text=True,env={**os.environ,"MPLBACKEND":"agg"});print(nome,"rc",r.returncode,r.stdout[-300:],r.stderr[-1500:],flush=True)
rodar("qw",QW,[])
try: rodar("cb",CB,["chatterbox-tts"])
except Exception as e: print("cb falhou",e)
try: rodar("f5",F5,["f5-tts"])
except Exception as e: print("f5 falhou",e)
import zipfile
with zipfile.ZipFile(f"{B}/amostras.zip","w") as z:
    for a in os.listdir(f"{B}/out"): z.write(f"{B}/out/{a}",a)
print("OK",os.listdir(f"{B}/out"))
