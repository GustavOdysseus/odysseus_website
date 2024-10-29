import openai
import os
from datetime import date
import hashlib
import time
from dotenv import load_dotenv 
import logging

# Configurar o logging
logging.basicConfig(
    filename='upload_errors.log',
    filemode='a',  # Acrescenta ao arquivo existente
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Set OpenAI API key como uma variável de ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializa o cliente OpenAI
openai.api_key = OPENAI_API_KEY

# Cria uma versão baseada na data para o nome do Vector Store
def generate_version_tag():
    today = date.today()
    timestamp = int(time.time())
    commit_hash = hashlib.sha1(str(timestamp).encode()).hexdigest()[:4].upper()
    version_tag = today.strftime("%m.%d.%Y")
    return version_tag

version_tag = generate_version_tag()
assistant_name = f"QuantGPT {version_tag}"

assistant_instructions = f"""You are a helpful assistant that has a knowledge base uploaded to you containing information on how the closed-source VectorBT (PRO) Python library and its modules work for building financial backtests and simulations.

VectorBT PRO (vectorbtpro) is a next-generation engine for backtesting, algorithmic trading, and research. It's a high-performance, actively-developed, proprietary successor to the vectorbt library, one of the world's most innovative open-source backtesting packages. The PRO version extends the open-source package with new impressive features and useful enhancements.

You are an expert at reading through the provided VectorBT (PRO) documentation and coming up with clear, accurate answers to users' queries.

You have been given a massive index to search through which contains all of the text from VBT (PRO)'s documentation. If you cannot find/retrieve the answer in your vector store, you simply let the user know. Respond saying that you can't find any information on that topic specifically.

Also, FYI, VectorBT (PRO) can also be referred to in this context as VBT, so if VBT is mentioned in the messages, assume the user is referring to this closed source version, NOT the open source `vectorbt`. VectorBT PRO has been completely refactored to improve performance and enable new groundbreaking features, such as parallelization support, so many things are different from how the older, open source version worked."""

# Step 1: Create a new Assistant with File Search Enabled
assistant = openai.Client().beta.assistants.create(
    name=assistant_name,
    instructions=assistant_instructions,
    model="gpt-4o-mini",  # Verifique se este modelo está correto
    temperature=0.40,
    tools=[
        {
            "type": "file_search" # Define o número máximo de resultados
        },
        {"type": "code_interpreter"}
    ],
)
print(f"Assistant created successfully ✔")
print(f"Assistant Name: {assistant.name}")
print(f"Assistant ID: {assistant.id}")

# Step 2: Criação do Vector Store
# Cria um vector store com um nome descritivo
vector_store = openai.Client().beta.vector_stores.create(name=f"{assistant_name} Vector Store")

# Verificação de Status do vector_store
def wait_for_vector_store_ready(vector_store_id, timeout=300, interval=5):
    """
    Aguarda até que o vector_store esteja no status 'ready' ou até atingir o timeout.

    :param vector_store_id: ID do vector_store a ser verificado.
    :param timeout: Tempo máximo em segundos para aguardar.
    :param interval: Intervalo em segundos entre as verificações.
    :return: True se o vector_store estiver pronto, False caso contrário.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        vs = openai.Client().beta.vector_stores.retrieve(vector_store_id)
        if vs.status == "completed":
            print(f"Vector Store {vector_store_id} está pronto para uso.")
            return True
        elif vs.status == "failed":
            print(f"Falha na criação do Vector Store {vector_store_id}.")
            logging.error(f"Vector Store {vector_store_id} falhou na criação.")
            return False
        else:
            print(f"Status atual do Vector Store {vector_store_id}: {vs.status}. Aguardando...")
            time.sleep(interval)
    print(f"Timeout atingido. Vector Store {vector_store_id} não está pronto.")
    logging.error(f"Timeout ao aguardar o Vector Store {vector_store_id} estar pronto.")
    return False

# Chama a função para aguardar o vector_store estar pronto
if not wait_for_vector_store_ready(vector_store.id):
    raise Exception(f"Vector Store {vector_store.id} não está pronto. Abortando o processo de upload.")

# Prepara os arquivos para upload
directories = ['./output/']  # Ajuste o caminho conforme necessário
supported_extensions = {
    '.c', '.cs', '.cpp', '.doc', '.docx', '.html', '.java', '.json', '.md', 
    '.pdf', '.php', '.pptx', '.py', '.rb', '.tex', '.txt', '.css', '.js', 
    '.sh', '.ts'
}

file_paths = [
    os.path.join(directory, filename) 
    for directory in directories
    for filename in os.listdir(directory) 
    if os.path.isfile(os.path.join(directory, filename)) and os.path.splitext(filename)[1] in supported_extensions
]

# Abre um arquivo de log para registrar erros
with open('upload_errors.log', 'a', encoding='utf-8') as log_file:
    # Batch the file uploads
    batch_size = 500
    file_ids = []
    for i in range(0, len(file_paths), batch_size):
        batch = file_paths[i:i+batch_size]
        try:
            file_streams = [open(path, "rb") for path in batch]
            file_batch = openai.Client().beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id, files=file_streams
            )
            
            # Exibe informações do lote
            print(f"Full file_batch response: {file_batch}")
            print(f"Has attribute 'errors': {hasattr(file_batch, 'errors')}")
            if hasattr(file_batch, 'errors'):
                print(f"Errors: {file_batch.errors}")
            
            print(file_batch)
            print(file_batch.status)
            print(file_batch.file_counts)
        
            # Se houver erros, registre-os no arquivo de log e tente novamente
            if hasattr(file_batch, 'errors') and file_batch.errors:
                for error in file_batch.errors:
                    error_message = f"Error uploading file {error.file}: {error.message}"
                    print(error_message)
                    logging.error(error_message)
                    
                    # Implementar uma re-tentativa para falhas específicas
                    retries = 3
                    for attempt in range(retries):
                        try:
                            with open(error.file, "rb") as f:
                                retry_response = openai.Client().beta.vector_stores.file_batches.upload_and_poll(
                                    vector_store_id=vector_store.id, files=[f]
                                )
                            print(f"Retry {attempt+1}: Successfully uploaded {error.file}")
                            break  # Sai do loop de re-tentativas se bem-sucedido
                        except Exception as retry_e:
                            retry_error_message = f"Retry {attempt+1} failed for file {error.file}: {retry_e}"
                            print(retry_error_message)
                            logging.error(retry_error_message)
                            time.sleep(2)  # Aguarda 2 segundos antes da próxima re-tentativa
                    else:
                        # Se todas as re-tentativas falharem, logue novamente
                        final_error = f"Failed to upload {error.file} after {retries} attempts."
                        print(final_error)
                        logging.error(final_error)
        
            # Fecha os streams de arquivos
            for file_stream in file_streams:
                file_stream.close()
        
        except Exception as e:
            error_message = f"Exception during file upload: {e}"
            print(error_message)
            logging.error(error_message)

# Step 3: Update the assistant to use the new Vector Store
assistant = openai.Client().beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)
print(f"Assistant updated with vector store: {vector_store.id}")
