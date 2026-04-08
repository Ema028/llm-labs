from colorama import Fore, Style, init
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API"))
init(autoreset=True)

def geracao_texto(mensagens, modelo="openai/gpt-oss-120b",temperatura=0,max_tokens=1000,stream=True):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model=modelo,
        temperature=temperatura,
        max_tokens=max_tokens,
        stream=stream
    )
    print(f"{Fore.CYAN}Bot:", end="")
    texto_completo = ""
    for resposta_stream in resposta:
        #primeira opção de resposta, acessa o que mudou e extrai o texto puro
        texto = resposta_stream.choices[0].delta.content
        if texto:
            print(texto, end="")
            texto_completo += texto
    print() #pular 1 linha depois da resposta
    mensagens.append({"role":"assistant", "content": texto_completo})
    return mensagens

if __name__ == "__main__":
    print(f"{Fore.YELLOW}Bem Vindo ao Chatbot")
    mensagens = []
    while True:
        input_user = input(f"{Fore.GREEN}User: {Style.RESET_ALL}")
        mensagens.append({"role":"user", "content": input_user})
        mensagens = geracao_texto(mensagens)