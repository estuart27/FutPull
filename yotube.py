import os
from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from Pesquisa import pesquisar_na_web
from Raspagem import obter_resumos_dos_links
import json


# # URL da notícia
# URL = [
#         'https://www.fotmob.com/pt-BR/matches/athletic-club-vs-rayo-vallecano/2avs59#4507055',

#         'https://www.fotmob.com/pt-BR/matches/athletic-club-vs-rayo-vallecano/2avs59#4507055:tab=table',

#         'https://www.sofascore.com/football/match/athletic-club-rayo-vallecano/tgbsAgb#id:12437621',

#         'https://1xbet.whoscored.com/matches/1821685/preview/spain-laliga-2024-2025-athletic-club-rayo-vallecano',
#     ]

# # Testando a função
# time = input("Digite o nome do time: ")

# adicional_manual = input("Digite informações adicionais: ")

# Carregar os dados da análise
try:
    with open("dados_analise.json", "r") as f:
        dados = json.load(f)
    
    time = dados["partida"]
    adicional_manual  = dados["observacoes"]
    URL = dados["links"]
    
    # Continue seu processamento aqui...
    
except Exception as e:
    print(f"Erro ao carregar dados: {e}")

# Caminho do arquivo PDF
# CAMINHO_PDF = 'static/DadosTokens.pdf'
CAMINHO_PDF = 'static/DadosTokens2.pdf'


# api_key = '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' # chave de API antiga Hub
api_key = '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' # chave de API atualizada Estuartos.environ['GROQ_API_KEY'] = api_key

# Função para carregar o conteúdo de um PDF
def carregar_documento_pdf(caminho: str) -> str:
    """Carrega e retorna o conteúdo textual de um PDF."""
    loader = PyMuPDFLoader(caminho)
    documentos = loader.load()
    return " ".join(doc.page_content for doc in documentos if doc.page_content)

# Função principal para responder com base no PDF e na web
def responder_com_pdf(mensagem: str, time: str, adicional_manual: str) -> str:
    """Gera uma resposta baseada no conteúdo do PDF, da web e da pesquisa SerpAPI."""
    chat = ChatGroq(model="llama-3.3-70b-versatile")

    documento_web = obter_resumos_dos_links(URL)
    documento_pdf = carregar_documento_pdf(CAMINHO_PDF)
    documento_web += adicional_manual

    # Só faz a pesquisa se o time for fornecido
    if time.strip():
        dados_pesquisa = pesquisar_na_web(time)
    else:
        print("⚠️ Nenhum time inserido. Pulando a pesquisa na web.")
        dados_pesquisa = "Nenhum dado de pesquisa disponível."

    template = ChatPromptTemplate.from_messages([
        ("system", """
        Você é um analista especializado em apostas esportivas que avalia partidas de futebol com precisão.
        
        Analise a partida {time} utilizando os dados fornecidos: {informações_jogo}, {dados_pesquisa}.
        
        Siga rigorosamente estes parâmetros de análise: {parametro}
        
        Após sua análise, forneça APENAS 3-4 apostas específicas com maior probabilidade de acerto.
        
        Seu formato de resposta DEVE ser:
        
        1. [Tipo de Aposta]: [Seleção específica]
           * Confiança: [Alta/Média]
           * Razão: [Uma frase curta com justificativa]
        
        2. [Tipo de Aposta]: [Seleção específica]
           * Confiança: [Alta/Média]
           * Razão: [Uma frase curta com justificativa]
        
        3. [Tipo de Aposta]: [Seleção específica]
           * Confiança: [Alta/Média]
           * Razão: [Uma frase curta com justificativa]
        
        [4. Opcional - apenas se houver forte valor]

        com base nos dados que você tem, faça uma análise de 0 a 100% de confiança, com base nos dados que você tem. e entregue nesse formato [Confiaça: 0-100%].
        
        FOQUE apenas nos mercados mais assertivos: Dupla Chance, Draw No Bet, Under/Over 1.5 ou 2.5 gols, Ambas Marcam, 
        Handicap Asiático, Time a Marcar Primeiro ou Gols em um tempo específico.
        
        NÃO INCLUA análises detalhadas, explicações adicionais ou qualquer outro texto além do formato solicitado.
        """),
        ("user", "{input}")
    ])
    
    prompt_formatado = template.format_prompt(
        informações_jogo=documento_web, 
        dados_pesquisa=dados_pesquisa,
        parametro=documento_pdf,
        time=time or "Time não especificado",
        input=mensagem
    )

    print(documento_web)
    resposta = chat.invoke(prompt_formatado.to_messages())
    return resposta.content

resposta = responder_com_pdf("Quais são as apostas mais precisas para esta partida?",  time, adicional_manual)
# resposta = responder_com_pdf("analisando esses dados , quantos por centro ele esta completo para uma analise assertiva esportiva?  ", time, adicional_manual)
print(resposta)