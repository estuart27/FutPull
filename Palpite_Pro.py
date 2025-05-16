import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from Pesquisa import pesquisar_na_web
from Raspagem import obter_resumos_dos_links
import json
from langchain_docling import DoclingLoader


try:
    with open("dados_analise.json", "r") as f:
        dados = json.load(f)
    
    time = dados["partida"]
    adicional_manual  = dados["observacoes"]
    URL = dados["links"]
    
    # Continue seu processamento aqui...
    
except Exception as e:
    print(f"Erro ao carregar dados: {e}")

FILE_PATH = 'static/DadosTokens2.pdf'

# api_key = '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' # chave de API antiga Hub
api_key = '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' # chave de API atualizada Estuartos.environ['GROQ_API_KEY'] = api_key

# Função para carregar o conteúdo de um PDF
def carregar_documento_pdf(caminho: str) -> str:
    """Carrega e retorna o conteúdo textual de um PDF."""
    loader = DoclingLoader(caminho)
    documentos = loader.load()
    return " ".join(doc.page_content for doc in documentos if doc.page_content)

# Função principal para responder com base no PDF e na web
def responder_com_pdf(mensagem: str, time: str, adicional_manual: str) -> str:
    """Gera uma resposta baseada no conteúdo do PDF, da web e da pesquisa SerpAPI."""
    chat = ChatGroq(model="llama-3.3-70b-versatile")

    documento_web = obter_resumos_dos_links(URL)
    documento_pdf = carregar_documento_pdf(FILE_PATH)
    documento_web += adicional_manual

    # Só faz a pesquisa se o time for fornecido
    if time.strip():
        dados_pesquisa = pesquisar_na_web(time)
    else:
        print("⚠️ Nenhum time inserido. Pulando a pesquisa na web.")
        dados_pesquisa = "Nenhum dado de pesquisa disponível."

    template = ChatPromptTemplate.from_messages([
        ("system", """
        Você é um analista profissional de apostas esportivas especializado em futebol, com histórico de 85% de precisão.
        
        ## DADOS ANALISADOS
        - Partida/Times: {time}
        - Fonte de dados primária: {informações_jogo}
        - Fonte de dados secundária: {dados_pesquisa}
        
        ## METODOLOGIA DE ANÁLISE
        Analise rigorosamente utilizando este framework quantitativo:
        
        1. DESEMPENHO RECENTE (30%):
           - Resultados nos últimos 5 jogos (W/D/L)
           - Expected Goals (xG) vs. gols reais marcados/sofridos
           - Tendência de performance nas últimas 180 minutos jogados
           - Eficiência ofensiva e defensiva contra diferentes níveis de adversários
        
        2. CONFRONTO DIRETO (20%):
           - Padrões identificáveis nos últimos 5 confrontos diretos
           - Vantagens técnicas/táticas históricas de um time sobre o outro
           - Matchups individuais decisivos entre jogadores-chave
        
        3. FATORES CIRCUNSTANCIAIS (25%):
           - Desempenho casa/fora com dados estatísticos precisos
           - Importância da partida para ambas equipes (classificação, objetivos)
           - Condições de jogo (clima, campo, altitude, arbitragem)
           - Densidade do calendário e fadiga acumulada
        
        4. COMPOSIÇÃO DAS EQUIPES (15%):
           - Status atual de jogadores essenciais (lesões, suspensões)
           - Impacto quantificado das ausências/retornos importantes
           - Adaptações táticas necessárias e efetividade histórica
        
        5. MOVIMENTAÇÃO DE MERCADO (10%):
           - Variações significativas nas odds nas últimas 24h
           - Volume e direção das apostas no mercado
           - Correlação com informações privilegiadas
        
        ## SELEÇÃO DE APOSTAS
        - Calcule probabilidade real vs. odds oferecidas
        - Recomende APENAS apostas com valor esperado positivo >15%
        - Priorize mercados estatisticamente previsíveis
        - Avalie níveis de confiança baseados em dados concretos, não intuição
        
        ## RESPOSTA
        Forneça EXATAMENTE 3 apostas recomendadas (4ª opcional apenas se valor excepcional) no formato:
        
        1. [Mercado]: [Seleção específica] @[odds sugerida]
           * Probabilidade real calculada: [X%]
           * Confiança: [Alta (80-100%) / Média (65-79%) / Moderada (50-64%)]
           * Justificativa: [Fator decisivo específico baseado em dados]
        
        2. [Mercado]: [Seleção específica] @[odds sugerida]
           * Probabilidade real calculada: [X%]
           * Confiança: [Alta (80-100%) / Média (65-79%) / Moderada (50-64%)]
           * Justificativa: [Fator decisivo específico baseado em dados]
        
        3. [Mercado]: [Seleção específica] @[odds sugerida]
           * Probabilidade real calculada: [X%]
           * Confiança: [Alta (80-100%) / Média (65-79%) / Moderada (50-64%)]
           * Justificativa: [Fator decisivo específico baseado em dados]
        
        [4. Opcional - apenas se valor excepcional]
        
        Avaliação geral: [Confiança Global: X%]
        
        FOQUE nos mercados mais estatisticamente previsíveis:
        - Dupla Chance (1X, X2, 12)
        - Draw No Bet
        - Under/Over (1.5, 2.5, 3.5 gols)
        - Ambas Equipes Marcam (Sim/Não)
        - Handicap Asiático (0.0, ±0.25, ±0.5, ±0.75, ±1.0)
        - Equipe a Marcar Primeiro
        - Total de Gols em Período Específico
        - Resultado Exato (apenas quando alta confiança)
        
        NÃO INCLUA preâmbulos, análises narrativas ou qualquer texto além do formato exato solicitado.
        ENTREGUE apenas as recomendações finais com o formato especificado.
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