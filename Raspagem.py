import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import os

api_key = 'API' # chave de API atualizada Estuartos.environ['GROQ_API_KEY'] = api_key
os.environ['GROQ_API_KEY'] = api_key

def carregar_pagina_html(url: str) -> str:
    chromedriver_autoinstaller.install()

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ative se quiser rodar em segundo plano
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)

    html = driver.page_source
    driver.quit()
    return html

def extrair_texto_limpo(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(["script", "style", "nav", "footer", "header", "button"]):
        tag.decompose()
    return soup.get_text(separator='\n', strip=True)

def resumir_com_ia(texto: str, fonte: str) -> str:
    chat = ChatGroq(model="llama-3.3-70b-versatile")

    template = ChatPromptTemplate.from_messages([
    ("system", 
     "Você é um assistente de dados. Seu trabalho é organizar e resumir o conteúdo extraído de páginas esportivas, "
     "mantendo as estatísticas, informações sobre jogadores, na cada de que time vai ser o jogo ,desempenho dos times, e dados objetivos relevantes . "
     "Não faça análises, não dê palpites e não interprete os dados. Apenas reestruture de forma clara e objetiva."),
    ("user", "{input}")
    ])
    
    prompt_formatado = template.format_prompt(input=f"Fonte: {fonte}\n\nTexto extraído:\n{texto}")
    resposta = chat.invoke(prompt_formatado.to_messages())
    return resposta.content

def obter_resumos_dos_links(links: list[str]) -> str:
    resumos_finais = ""

    for i, link in enumerate(links, start=1):
        print(f"\n🔗 Coletando e resumindo dados do link {i}: {link}\n")
        html = carregar_pagina_html(link)
        texto_limpo = extrair_texto_limpo(html)
        resumo = resumir_com_ia(texto_limpo, f"Fonte {i}")
        resumos_finais += f"\n\n=== 🧠 Resumo Inteligente da Fonte {i} ===\n{resumo}"

    # print(resumos_finais)
    return resumos_finais


if __name__ == "__main__":
    LINKS = [
        'https://www.sofascore.com/football/match/real-madrid-arsenal/RsEgb#id:13513403',
    ]

    resumo_final = obter_resumos_dos_links(LINKS)

    print("\n📊 Resumo Consolidado para Análise da IA:\n")
    print(resumo_final)
