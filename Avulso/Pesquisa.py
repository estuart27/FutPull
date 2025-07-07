from langchain.tools import Tool
from langchain_community.utilities import SerpAPIWrapper

def pesquisar_na_web(consulta: str) -> str:
    """Faz uma pesquisa na web e retorna os principais resultados."""
    search = SerpAPIWrapper(serpapi_api_key="1991f75cf0526b14f610e0b7dded6cebafa5a24fd2ba2ab6293b07738292ae84")
    return search.run(consulta)

if __name__ == "__main__":
  resultado = pesquisar_na_web("tabela do brasileirão")
  print(resultado)




