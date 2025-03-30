import os
from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from Analise_Dados import carregar_documento_web

# URL da notícia
URL = 'https://www.sofascore.com/football/match/corinthians-bahia/fOshO#id:13473345'

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
def responder_com_pdf(mensagem: str) -> str:
    """Gera uma resposta baseada no conteúdo do PDF e da web."""
    # Inicializa o modelo
    # chat = ChatGroq(model='llama-3.3-70b-versatile')
    chat = ChatGroq(model="llama-3.3-70b-versatile")

    # Carrega os dados da web e do PDF
    documento_web = carregar_documento_web(URL)
    documento_pdf = carregar_documento_pdf(CAMINHO_PDF)

    template = ChatPromptTemplate.from_messages([
        ("system", "Você é um apostador esportivo, e faça analise da partida, com base na seguintes informações: {informações_jogo}."), #Colocar aqui o perfil de um apostador que ter mais acertabilidade 
        ("system", "Agora Cria aposta com base nesses parametros: {parametro}."),
        ("system", "Quero que voce me passe qual aposta eu fazer como palpite , pelo menos 4 variação de apostas "),
        ("user", "{input}")
    ])
    
    # Formata o prompt corretamente
    prompt_formatado = template.format_prompt(
        informações_jogo=documento_web,
        parametro=documento_pdf,
        input=mensagem  # Alterado de 'pergunta' para 'input' para corresponder ao template
    )

    # Faz a chamada ao modelo e retorna a resposta
    resposta = chat.invoke(prompt_formatado.to_messages())
    return resposta.content

# Testando a função
resposta = responder_com_pdf("Qual é o time que vai ganhar? me de somente 4 apostas e o nome do time que vai ganhar")
print(resposta)







# def carregar_documento_web(url: str) -> str:
#     """Carrega e retorna o conteúdo textual de uma página web."""
#     loader = WebBaseLoader(url)
#     documentos = loader.load()
#     return " ".join(doc.page_content for doc in documentos if doc.page_content)