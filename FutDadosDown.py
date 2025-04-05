import os
import pandas as pd
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import json
import shutil
# Adicione estas importações
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.document_loaders import Docx2txtLoader, UnstructuredExcelLoader


# Set API key
groq_api_key = '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'
os.environ['GROQ_API_KEY'] = groq_api_key

def load_and_process_pdf(pdf_path):
    """Carrega e processa um arquivo PDF"""
    # Carregar PDF
    loader = PyPDFLoader(pdf_path)
    pdf_documents = loader.load()
    
    # Extrair metadados básicos
    summary = {
        "total_pages": len(pdf_documents),
        "filename": os.path.basename(pdf_path),
        "filesize": os.path.getsize(pdf_path)
    }
    
    return pdf_documents, summary

def create_vector_db_from_document(document_path, force_recreate=True):
    """Cria uma base de dados vetorial a partir de Excel ou PDF"""
    if os.path.exists(VECTOR_DB_PATH) and force_recreate:
        print("Removendo base de dados vetorial existente...")
        shutil.rmtree(VECTOR_DB_PATH, ignore_errors=True)
    
    print(f"Criando nova base de dados vetorial a partir de {document_path}...")
    
    # Determinar o tipo de documento pela extensão
    ext = os.path.splitext(document_path)[1].lower()
    
    if ext == '.xlsx' or ext == '.xls':
        # Usar o processamento de Excel existente
        df, summary = preprocess_excel(document_path)
        
        # Converter cada linha em um documento para armazenamento vetorial
        documents = [Document(
            page_content=f"Excel Summary: {json.dumps(summary)}",
            metadata={"source": "summary", "document_path": document_path}
        )]
        
        for j, row in df.iterrows():
            content = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
            metadata = {
                "source": f"row_{j}", 
                "document_path": document_path,
                "row_index": j
            }
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)
            
    elif ext == '.pdf':
        # Processar PDF
        pdf_documents, summary = load_and_process_pdf(document_path)
        
        # Adicionar sumário como documento
        documents = [Document(
            page_content=f"PDF Summary: {json.dumps(summary)}",
            metadata={"source": "summary", "document_path": document_path}
        )]
        
        # Adicionar cada página do PDF
        documents.extend(pdf_documents)
        
    else:
        raise ValueError(f"Formato de arquivo não suportado: {ext}")
    
    print(f"Processados {len(documents)} documentos...")
    
    # Dividir documentos longos em chunks menores
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Tamanho de cada chunk
        chunk_overlap=100, # Sobreposição para manter contexto
        separators=["\n\n", "\n", " | ", ", ", " "]
    )
    split_docs = text_splitter.split_documents(documents)
    
    # Criar embeddings usando HuggingFace
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    # Criar base de dados vetorial
    vector_store = FAISS.from_documents(split_docs, embeddings)
    
    # Salvar para uso futuro
    vector_store.save_local(VECTOR_DB_PATH)
    
    return vector_store


def answer_query_with_rag(query, document_path):
    """Responde a uma consulta sobre dados usando abordagem RAG"""
    # Criar base vetorial (sempre recriar por segurança)
    vector_store = create_vector_db_from_document(document_path, force_recreate=True)
    
    # Recuperar documentos relevantes baseados na consulta
    relevant_docs = vector_store.similarity_search(query, k=20)
    
    # Extrair o conteúdo dos documentos relevantes
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # Configurar o LLM
    chat = ChatGroq(model="llama-3.3-70b-versatile")
    
    # Criar template de prompt que inclui o contexto
    template = ChatPromptTemplate.from_messages([
        ("system", """Você é um assistente especializado em análise de documentos.
        
        DADOS RELEVANTES DO DOCUMENTO (baseados na consulta):
        {context}
        
        Responda à pergunta do usuário com base apenas nos dados fornecidos acima.
        Se a resposta não puder ser determinada com certeza a partir dos dados fornecidos, explique o que falta.
        Cite trechos específicos do documento quando relevante.
        """),
        ("user", "{query}")
    ])
    
    # Formatar o prompt com o contexto recuperado
    prompt_formatted = template.format_prompt(
        context=context,
        query=query
    )
    
    # Obter resposta
    response = chat.invoke(prompt_formatted.to_messages())
    return response.content

EXCEL_PATH = 'static/Subway.xlsx'
VECTOR_DB_PATH = 'subway_vector_db'  # Path to save vector database

def preprocess_excel(excel_path):
    """Preprocesses the Excel file and creates a summary"""
    df = pd.read_excel(excel_path)
    
    # Create a summary of the dataframe
    summary = {
        "total_rows": len(df),
        "columns": list(df.columns),
    }
    
    # Check for common columns and add their info
    if "order_id" in df.columns:
        summary["num_unique_orders"] = df["order_id"].nunique()
    if "date" in df.columns:
        summary["date_range"] = f"{df['date'].min()} to {df['date'].max()}"
    
    return df, summary

def create_vector_db_from_excel(excel_path, force_recreate=True):
    """Create a vector database from Excel data for efficient retrieval"""
    # For safety, we'll always recreate the database to avoid deserialization issues
    if os.path.exists(VECTOR_DB_PATH) and force_recreate:
        print("Removing existing vector database...")
        shutil.rmtree(VECTOR_DB_PATH, ignore_errors=True)
    
    print("Creating new vector database from Excel data...")
    # Load and preprocess Excel data
    df, summary = preprocess_excel(excel_path)
    
    # Create a summary document
    summary_doc = Document(
        page_content=f"Excel Summary: {json.dumps(summary)}",
        metadata={"source": "summary", "excel_path": excel_path}
    )
    
    # Convert each row to a document for vector storage
    documents = [summary_doc]  # Start with the summary
    
    # Process in batches to handle large files better
    batch_size = 100
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        
        for j, row in batch.iterrows():
            # Convert row to a cleaner string representation
            content = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
            
            # Add metadata to help with retrieval
            metadata = {
                "source": f"row_{j}", 
                "excel_path": excel_path,
                "row_index": j
            }
            
            # Add any key columns as metadata if they exist
            for key_col in ["order_id", "date", "restaurant_id", "total"]:
                if key_col in row and pd.notna(row[key_col]):
                    metadata[key_col] = str(row[key_col])
            
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)
    
    print(f"Processed {len(documents)} documents...")
    
    # Split longer documents if needed
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100,
        separators=["\n\n", "\n", " | ", ", ", " "]
    )
    split_docs = text_splitter.split_documents(documents)
    
    # Create vector embeddings using HuggingFace
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    # Create vector store
    vector_store = FAISS.from_documents(split_docs, embeddings)
    
    # Save the vector store for future use
    vector_store.save_local(VECTOR_DB_PATH)
    
    return vector_store

# Example usage
if __name__ == "__main__":
    document_path = "static/dados.pdf"
    query = "Resuma pra mim o que fala esse documento?"
    answer = answer_query_with_rag(query, document_path)
    print(answer)










# import os
# from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader
# from langchain_groq import ChatGroq
# from langchain.prompts import ChatPromptTemplate
# from Analise_Dados import carregar_documento_web
# import pandas as pd

# api_key = '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'# Configuração da API Key de forma segura

# os.environ['GROQ_API_KEY'] = api_key  # Substituir por variável de ambiente segura

# CAMINHO_EXCEL = 'static/Subway.xlsx'  # Caminho do seu arquivo Excel

# def carregar_excel(caminho: str) -> str:
#     df = pd.read_excel(caminho)
#     return df.to_json(orient="records", lines=False)

#     # return df.to_string(index=False)


# def responder_com_pdf_e_excel(mensagem: str) -> str:
#     chat = ChatGroq(model="llama-3.3-70b-versatile")

#     documento_excel = carregar_excel(CAMINHO_EXCEL)

#     template = ChatPromptTemplate.from_messages([
#         ("system", "Você tira duvidas de uma planilha do restaurtante com base nessas informações: {dados_excel}"),
#         ("user", "{input}")
#     ])

#     prompt_formatado = template.format_prompt(
#         dados_excel=documento_excel,
#         input=mensagem
#     )

#     resposta = chat.invoke(prompt_formatado.to_messages())
#     return resposta.content


# # Testando a função
# mensagem = "Qual é o maior valor comprado ? " # Exemplo de mensagem para testar a função
# resposta = responder_com_pdf_e_excel(mensagem)
# print(resposta)