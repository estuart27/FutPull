from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os


def carregar_documento_web(url: str) -> str:
    loader = WebBaseLoader(url)
    lista_documentos = loader.load()

    # Concatena conteúdo dos documentos
    documento = ''
    for doc in lista_documentos:
        documento = documento + doc.page_content

    api_key = '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'
    os.environ['GROQ_API_KEY'] = api_key

    # Inicializa o ChatGroq
    chat = ChatGroq(model='deepseek-r1-distill-llama-70b')

    # Template de prompt para o assistente
    template = ChatPromptTemplate.from_messages([
        ('system', 'Vai ser uma analista de informação para um apostador esportivo, com base nesses dados:{documentos_informados}'),
        ('user', '{input}')
    ])

    # Invoca o chat com entrada específica
    chain = template | chat
    # resposta = chain.invoke({'documentos_informados': documento, 'input': "Quero saber 2 duvidas , essas informação acima sao suficiente para ter uma analise acertiva ? se nao , o que falta?"})

    resposta = chain.invoke({'documentos_informados': documento, 'input': "Quero que você faça resumo e deixe esses dados mais organizada para analise que vou fazer para uma apostar esportiva mais acertiva!"})
    # print('Informação organizada')
    print(resposta.content)

    return resposta.content

if __name__ == "__main__":
    # URL da notícia
    URL = 'https://www.ogol.com.br/estatisticas/bahia-corinthians/t2231-t2234'
    carregar_documento_web(URL)