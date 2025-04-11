import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def carregar_pagina_html(url: str) -> str:
    chromedriver_autoinstaller.install()

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Se quiser rodar em segundo plano
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

    # Remove scripts, estilos e partes irrelevantes
    for tag in soup(["script", "style", "nav", "footer", "header", "button"]):
        tag.decompose()

    texto = soup.get_text(separator='\n', strip=True)
    return texto

def obter_analise_dos_links(links: list[str]) -> str:
    analise_completa = ""

    for i, link in enumerate(links, start=1):
        print(f"\n🔗 Coletando dados do link {i}: {link}\n")
        html = carregar_pagina_html(link)
        texto = extrair_texto_limpo(html)

        analise_completa += f"\n\n=== 🔎 Fonte {i} ===\n{texto}"

    return analise_completa


if __name__ == "__main__":
    LINKS = [
        'https://www.sofascore.com/football/match/real-madrid-arsenal/RsEgb#id:13513403',
        'https://www.fotmob.com/pt-BR/matches/real-madrid-vs-arsenal/2tfkqo#4737568',
        'https://1xbet.whoscored.com/matches/1894555/preview/europe-champions-league-2024-2025-arsenal-real-madrid',
    ]

    texto_final = obter_analise_dos_links(LINKS)

    print("\n📊 Análise Consolidada para IA:\n")
    print(texto_final)
