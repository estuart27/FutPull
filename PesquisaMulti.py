from langchain_community.utilities import SerpAPIWrapper

def pesquisar(time: str) -> dict:
    """Pesquisa na web usando SerpAPI para obter informações sobre um time de futebol."""
    
    search = SerpAPIWrapper(
        serpapi_api_key="1991f75cf0526b14f610e0b7dded6cebafa5a24fd2ba2ab6293b07738292ae84",  # Substitua pela sua chave real
        params={"num": 5, "hl": "pt", "gl": "br"}
    )

    consultas = [
        "Tabela do Campeonato Brasileiro",
        f"jogadores lesionados e suspensos hoje de {time}",
        f"Local do jogo {time}, qual estádio, clima e temperatura?",
        f"Estilo de jogo e formação tática dos time {time}",
        f"Pontos fortes e fracos do {time} na temporada"
        f"Destaques e jogadores-chave para {time} neste confronto"

    ]

    resultados = {}
    
    for consulta in consultas:
        resultados[consulta] = search.run(consulta)

    return resultados


if __name__ == "__main__":
    time = "Cruzeiro x Union de Santa Fe"
    resultados = pesquisar(time)

    # Exibir os resultados
    for pergunta, resposta in resultados.items():
        print(f"\n{pergunta}:\n{resposta}\n")