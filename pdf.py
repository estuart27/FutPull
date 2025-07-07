from langchain_docling import DoclingLoader


# Caminho para o arquivo local (ex: PDF salvo no seu computador)
FILE_PATH = ["dados.pdf"]  # ajuste o caminho conforme o seu arquivo

# Carrega o documento local
loader = DoclingLoader(file_path=FILE_PATH)

docs = loader.load()

print(docs)
#quero exibir o texto do pdf
for doc in docs:
    print(doc.page_content)  # Exibe o conteúdo de cada página do PDF
    print("===" * 20)  # Separador entre páginas