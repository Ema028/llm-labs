import os
import openai
import speech_recognition as sr
from playsound import playsound
from pathlib import Path
from io import BytesIO
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

client = openai.OpenAI(
  base_url="https://api.groq.com/openai/v1",
  api_key=os.environ.get("GROQ_API")
)

arquivo_audio = "resposta.mp3"

recognizer = sr.Recognizer()

def main():
    mensagens = []
    while True:
        audio = grava_audio()
        transcricao = transcricao_audio(audio)

        if not transcricao:
            print("Não foi possível transcrever o áudio. Tente novamente")
            continue

        mensagens.append({"role": "user", "content": transcricao})
        #print(f"User: {mensagens[-1]["content"]}")

        resposta_texto = completa_texto(mensagens)
        mensagens.append({"role": "assistant", "content": resposta_texto})
        #print(f"Assistant: {mensagens[-1]["content"]}")

        cria_audio(resposta_texto)
        roda_audio()

def grava_audio():
    with sr.Microphone(0) as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    return audio

def transcricao_audio(audio):
    try:
        wav_data = BytesIO(audio.get_wav_data())
        wav_data.name = "audio.wav"
        transcricao = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=wav_data
        )
        return transcricao.text
    except Exception as e:
        print(f"Erro na transcrição do audio {e}")
        return
    
def completa_texto(mensagens):
    try:
        resposta = client.chat.completions.create(
            messages=mensagens,
            model="openai/gpt-oss-120b",
            max_tokens=1000,
            temperature=0
        )
        return resposta.choices[0].message.content
    except Exception as e:
        print(f"Erro na geração de resposta {e}")
        return "Desculpe, não entendi"
    
def cria_audio(texto):
    if Path(arquivo_audio).exists():
        Path(arquivo_audio).unlink()
    try:
        tts = gTTS(text=texto, lang='pt')
        tts.save(arquivo_audio)
    except Exception as e:
        print(f"Erro na criação de áudio: {e}")
        
def roda_audio():
    if Path(arquivo_audio).exists():
        playsound(arquivo_audio)
    else:
        print("Erro: O arquivo de áudio não foi encontrado.")

main()