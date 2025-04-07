from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os

os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

def carregar_documentos_web(urls: list) -> str:
    documento = ''

    for url in urls:
        loader = WebBaseLoader(url)
        lista_documentos = loader.load()

        # Concatena o conteúdo de cada documento
        for doc in lista_documentos:
            documento += doc.page_content + '\n'

    # Define a chave da API do ChatGroq
    api_key = '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'
    os.environ['GROQ_API_KEY'] = api_key

    # Inicializa o ChatGroq
    chat = ChatGroq(model='deepseek-r1-distill-llama-70b')

    # Template de prompt para o assistente
    template = ChatPromptTemplate.from_messages([
        ('system', 'Você é uma analista de informação para um apostador esportivo. Com base nos seguintes dados: {documentos_informados}'),
        ('user', '{input}')
    ])

    # Cria a cadeia de execução
    chain = template | chat

    # Executa a análise
    resposta = chain.invoke({
        'documentos_informados': documento,
        'input': "Quero que você faça um resumo e organize essas informações de forma estratégica para uma análise esportiva mais assertiva."
    })

    return resposta.content


if __name__ == "__main__":
    # Lista de URLs de partidas
    urls = [
        'https://www.sofascore.com/football/match/real-madrid-arsenal/RsEgb#id:13513403',
        'https://www.fotmob.com/pt-BR/matches/real-madrid-vs-arsenal/2tfkqo#4737568',
        'https://1xbet.whoscored.com/matches/1894555/preview/europe-champions-league-2024-2025-arsenal-real-madrid'
    ]

    resultado = carregar_documentos_web(urls)
    print("🔍 Análise Consolidada:\n")
    print(resultado)




























# def carregar_documento_web(url: str) -> str:
#     # loader = WebBaseLoader(url)
#     headers = {
#         "User-Agent": os.environ["USER_AGENT"]
#     }

#     loader = WebBaseLoader(url, header_template=headers)

#     lista_documentos = loader.load()

#     # Concatena conteúdo dos documentos
#     documento = ''
#     for doc in lista_documentos:
#         documento = documento + doc.page_content

#     api_key = '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'
#     os.environ['GROQ_API_KEY'] = api_key

#     # Inicializa o ChatGroq
#     chat = ChatGroq(model='deepseek-r1-distill-llama-70b')

#     # Template de prompt para o assistente
#     template = ChatPromptTemplate.from_messages([
#         ('system', 'Vai ser uma analista de informação para um apostador esportivo, com base nesses dados:{documentos_informados}'),
#         ('user', '{input}')
#     ])

#     # Invoca o chat com entrada específica
#     chain = template | chat
#     # resposta = chain.invoke({'documentos_informados': documento, 'input': "Quero saber 2 duvidas , essas informação acima sao suficiente para ter uma analise acertiva ? se nao , o que falta?"})

#     resposta = chain.invoke({'documentos_informados': documento, 'input': "Quero que você faça resumo e deixe esses dados mais organizada para analise que vou fazer para uma apostar esportiva mais acertiva!"})
#     # print('Informação organizada')
#     # print(resposta.content)

#     return resposta.content 

# if __name__ == "__main__":
#     # URL da notícia
#     URL = 'https://www.sofascore.com/football/match/real-madrid-arsenal/RsEgb#id:13513403'
#     resultado = carregar_documento_web(URL)
#     print("🔍 Análise Consolidada:\n")
#     print(resultado)