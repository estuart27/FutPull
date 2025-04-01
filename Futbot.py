import os
from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from Analise_Dados import carregar_documento_web
from PesquisaMulti import pesquisar

# URL da notícia
URL = 'https://www.sofascore.com/football/match/club-atletico-union-de-santa-fe-cruzeiro/eOseob#id:13640387'

# Caminho do arquivo PDF
CAMINHO_PDF = 'static/dados.pdf'

api_key = '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'# Configuração da API Key de forma segura

os.environ['GROQ_API_KEY'] = api_key  # Substituir por variável de ambiente segura


def carregar_documento_pdf(caminho: str) -> str:
    """Carrega e retorna o conteúdo textual de um PDF."""
    loader = PyMuPDFLoader(caminho)
    documentos = loader.load()
    return " ".join(doc.page_content for doc in documentos if doc.page_content)


# Função principal para responder com base no PDF e na web
# Adapte a função para incluir os dados da pesquisa na web
def responder_com_pdf(mensagem: str, time: str) -> str:
    """Gera uma resposta baseada no conteúdo do PDF, da web e da pesquisa SerpAPI."""
    chat = ChatGroq(model="llama-3.3-70b-versatile")

    # Carrega os dados da web, do PDF e da pesquisa
    documento_web = carregar_documento_web(URL)
    documento_pdf = carregar_documento_pdf(CAMINHO_PDF)
    dados_pesquisa = pesquisar(time)  # Obtém os dados da pesquisa

    # Formata o prompt corretamente
    template = ChatPromptTemplate.from_messages([
        ("system", "Você é um apostador esportivo e faz análise da partida com base nas seguintes informações: {informações_jogo}, {dados_pesquisa}."),
        ("system", "Agora crie apostas com base nesses parâmetros: {parametro}."),
        ("system", "Quero que você me passe qual aposta devo fazer como palpite, com pelo menos 4 variações de apostas."),
        ("user", "{input}")
    ])
    
    prompt_formatado = template.format_prompt(
        informações_jogo=documento_web,
        dados_pesquisa=dados_pesquisa,  # Inclui os dados da pesquisa
        parametro=documento_pdf,
        input=mensagem
    )

    resposta = chat.invoke(prompt_formatado.to_messages())
    return resposta.content

# Testando a função
time = "Cruzeiro x Union de Santa Fe"
# resposta = responder_com_pdf("Qual é o time que vai ganhar? Me dê somente 4 apostas e o nome do time que vai ganhar", time)
resposta = responder_com_pdf("Verifique todos essas dados e de 1 a 10 , que nota vc da pra minha informaçoes ? estam completas para tirar uma analise esportiva precisa ? cosideraçoes ?", time)
print(resposta)







# def carregar_documento_web(url: str) -> str:
#     """Carrega e retorna o conteúdo textual de uma página web."""
#     loader = WebBaseLoader(url)
#     documentos = loader.load()
#     return " ".join(doc.page_content for doc in documentos if doc.page_content)