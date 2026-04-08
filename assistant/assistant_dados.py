import os
import openai
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(
  base_url="https://api.groq.com/openai/v1",
  api_key=os.environ.get("GROQ_API")
)

try:
    df = pd.read_csv("sales_data.csv")
except FileNotFoundError:
    print("arquivo não encontrado")
    exit()

contexto_dados = f"Colunas disponíveis: {list(df.columns)}\nAmostra dos dados (3 linhas):\n{df.head(3).to_string()}"

'''exemplo de prompt usado para teste:
pergunta = "Gere um gráfico de pizza com o percentual de vendas por linha de produto. Salve o gráfico com o nome 'files/grafico_pizza_raiz.png'."
'''
pergunta = input("Instruções para análise de sales_data.csv: ")
prompt_sistema = """O usuário tem um DataFrame Pandas já carregado na memória na variável chamada 'df'
Sua única função é escrever o código Python necessário para resolver o pedido do usuário

REGRAS ABSOLUTAS:
1. Retorne APENAS código Python válido
2. NUNCA escreva explicações, saudações ou formatação markdown
3. Se o usuário pedir para calcular algo ou fizer uma pergunta, você DEVE usar a função print() no código para exibir a resposta final
4. Se o usuário pedir um gráfico, NUNCA use plt.show(). Você DEVE sempre salvar o gráfico usando plt.savefig('files/nome_do_grafico_gerado.png')
5. Use a variável 'df' diretamente"""

prompt_usuario = f"Contexto do DataFrame:\n{contexto_dados}\n\nPedido: {pergunta}"

resposta = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": prompt_sistema},
        {"role": "user", "content": prompt_usuario}
    ],
    temperature=0 #determinístico
)

codigo_gerado = resposta.choices[0].message.content.strip()
codigo_gerado = codigo_gerado.replace("```python", "").replace("```", "").strip()

print("\nCódigo Python Gerado")
print(codigo_gerado)
os.makedirs("files", exist_ok=True)

print("Executando o código gerado")
try:
    exec(codigo_gerado, globals(), locals())
except Exception as e:
    print(f"Ocorreu um erro: {e}")