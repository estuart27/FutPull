import os
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from Raspagem import obter_resumos_dos_links
import json
from langchain_docling import DoclingLoader

FILE_PATH = 'static/DadosTokens2.pdf'

adicional_manual = input("Digite as informaçãos: ")




# Função para carregar o conteúdo de um PDF
def carregar_documento_pdf(caminho: str) -> str:
    """Carrega e retorna o conteúdo textual de um PDF."""
    loader = DoclingLoader(caminho)
    documentos = loader.load()
    return " ".join(doc.page_content for doc in documentos if doc.page_content)

# Função principal para responder com base no PDF e na web
def responder_com_pdf(mensagem: str,adicional_manual: str) -> str:
    """Gera uma resposta baseada no conteúdo do PDF, da web e da pesquisa SerpAPI."""
    chat = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key="apI"
        )

    # documento_web = obter_resumos_dos_links(URL)
    documento_pdf = carregar_documento_pdf(FILE_PATH)

    # Só faz a pesquisa se o time for fornecid

    template = ChatPromptTemplate.from_messages([
        ("system", """
        Você é um analista profissional de apostas esportivas especializado em futebol, com histórico de 85% de precisão.
        
        ## DADOS ANALISADOS
        - Paramentro da analise: {parametro}
        - Fonte de dados primária: {informações_jogo}
        - Fonte de dados secundária: 
        ## SELEÇÃO DE APOSTAS
        - Recomende APENAS apostas com valor esperado positivo >15%
        - Priorize mercados estatisticamente previsíveis
        - Avalie níveis de confiança baseados em dados concretos, não intuição
        
        ## RESPOSTA
        Forneça de 3 a 5 apostas recomendadas (6ª opcional apenas se valor excepcional) no formato:
        
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
        - Under/Over (1.5, 2.5, 3.5 gols)
        - Ambas Equipes Marcam (Sim/Não)
        - Equipe a Marcar Primeiro
        - Total de Gols em Período Específico
        - Resultado Exato (apenas quando alta confiança)
        - Escanteios  Mais/Menos
        - Cartões Mais/Menos
        - Total de Gols Mais/Menos
        - Resultado no Intervalo 
        
        NÃO INCLUA preâmbulos, análises narrativas ou qualquer texto além do formato exato solicitado.
        ENTREGUE apenas as recomendações finais com o formato especificado.
        """),
        ("user", "{input}")
    ])
    
    prompt_formatado = template.format_prompt(
        informações_jogo=adicional_manual,
        parametro=documento_pdf,
        input=mensagem
    )

    resposta = chat.invoke(prompt_formatado.to_messages())
    return resposta.content

resposta = responder_com_pdf("Quais são as apostas mais precisas para esta partida?",adicional_manual)
# resposta = responder_com_pdf("analisando esses dados , quantos por centro ele esta completo para uma analise assertiva esportiva?  ", time, adicional_manual)
print(resposta)