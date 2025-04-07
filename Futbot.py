import os
from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from PesquisaMulti import pesquisar
from Raspagem import obter_resumos_dos_links

# URL da notícia
URL = [
        'https://www.sofascore.com/football/match/real-madrid-arsenal/RsEgb#id:13513403',
        'https://www.fotmob.com/pt-BR/matches/real-madrid-vs-arsenal/2tfkqo#4737568',
        'https://1xbet.whoscored.com/matches/1894555/preview/europe-champions-league-2024-2025-arsenal-real-madrid',
    ]

# Caminho do arquivo PDF
CAMINHO_PDF = 'static/DadosTokens.pdf'

api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

# Função para carregar o conteúdo de um PDF
def carregar_documento_pdf(caminho: str) -> str:
    """Carrega e retorna o conteúdo textual de um PDF."""
    loader = PyMuPDFLoader(caminho)
    documentos = loader.load()
    return " ".join(doc.page_content for doc in documentos if doc.page_content)

# Função principal para responder com base no PDF e na web
def responder_com_pdf(mensagem: str, time: str) -> str:
    """Gera uma resposta baseada no conteúdo do PDF, da web e da pesquisa SerpAPI."""
    chat = ChatGroq(model="llama-3.3-70b-versatile")
    # chat = ChatGroq(model="llama3-70b-8192") # modelo otimizado para análise de apostas esportivas

    # Carrega os dados da web, do PDF e da pesquisa
    documento_web = obter_resumos_dos_links(URL)
    documento_pdf = carregar_documento_pdf(CAMINHO_PDF)
    dados_pesquisa = pesquisar(time)

    # Template otimizado para fornecer 3-4 apostas de alto valor
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
        
        FOQUE apenas nos mercados mais assertivos: Dupla Chance, Draw No Bet, Under/Over 1.5 ou 2.5 gols, Ambas Marcam, 
        Handicap Asiático, Time a Marcar Primeiro ou Gols em um tempo específico.
        
        NÃO INCLUA análises detalhadas, explicações adicionais ou qualquer outro texto além do formato solicitado.
        """),
        ("user", "{input}")
    ])
    
    prompt_formatado = template.format_prompt(
        informações_jogo=documento_web, 
        dados_pesquisa=dados_pesquisa,
        parametro=documento_pdf, # Parâmetro de análise ajustado e acertivo
        time=time, #Formato otimizado para o time
        input=mensagem  #Mensagem de entrada otimizada para o usuário
    )

    resposta = chat.invoke(prompt_formatado.to_messages())
    return resposta.content

# Testando a função
time = "arsenal x real madrid"
# resposta = responder_com_pdf("Quais são as apostas mais precisas para esta partida?", time)
resposta = responder_com_pdf("de 1 a 10 as informação estao completas paa uma analise acertiva ?  ", time)

print(resposta)