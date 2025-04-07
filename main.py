# main.py
from scraper import carregar_pagina_html, extrair_texto_puro

if __name__ == "__main__":
    URL = 'https://www.sofascore.com/football/match/real-madrid-arsenal/RsEgb#id:13513403'
    html = carregar_pagina_html(URL)
    texto = extrair_texto_puro(html)

    print("🔍 Análise Consolidada:\n")
    print(texto)
