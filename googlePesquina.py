from googlesearch import search
from docling.document_converter import DocumentConverter
from Raspagem import obter_resumos_dos_links
from googlesearch import search

def buscar_links_esportivos(consulta: str, num_resultados: int = 5):
    # Adiciona instrução para buscar nos sites específicos
    consulta_formatada = (
        f"{consulta} site:whoscored.com OR site:fotmob.com OR site:sofascore.com"
    )
    
    # Realiza a pesquisa
    resultados = list(search(consulta_formatada, num_results=num_resultados))

    # Filtra apenas os domínios desejados (por segurança extra)
    dominios_desejados = ["whoscored.com", "fotmob.com", "sofascore.com"]
    links_filtrados = [
        url for url in resultados if any(dominio in url for dominio in dominios_desejados)
    ]

    return links_filtrados

# Exemplo de uso
consulta = input("Digite a partida para pesquisa: ")
links_desejados = buscar_links_esportivos(consulta)
Resultado = obter_resumos_dos_links(links_desejados)

print()


print("\n📊 Links relevantes encontrados:")
for link in links_desejados:
    print(link)


























# # Sua pergunta ou termo de pesquisa
# consulta = input("Digite a partida de pesquisa:")

# consulta += " Pesquise o Jogo no site - https://1xbet.whoscored.com/ , https://www.fotmob.com/ , https://www.sofascore.com/",

# URL = list(search("Palmeiras último jogo - Sites de dados esportivos", num_results=10))

# # Resultado = obter_resumos_dos_links(URL)

# print("\n📊 Resumo Consolidado para Análise da IA:\n")
# print(URL)


# resultados = search(consulta, num_results=3)



# # Mostra os links encontrados
# print("🔗 Links encontrados:")
# for link in resultados:
#     print(link)
#     result = converter.convert(link)
#     print(result.document.export_to_markdown())

# for i, link in enumerate(resultados, start=1):
#     result = converter.convert(link)
#     print(result.document.export_to_markdown())
#     print(f"{i}. {result}")


# from googlesearch import search

# resultados = list(search("Palmeiras último jogo - Sites de dados esportivos", num_results=3))

# print(resultados)
