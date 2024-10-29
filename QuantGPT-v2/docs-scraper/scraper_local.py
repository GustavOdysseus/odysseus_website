import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import html2text
import hashlib
import shutil
from readability.readability import Document

# Conjunto de URLs visitadas para evitar recursão infinita
visited_urls = set()

def download_page(file_path):
    """
    Lê o conteúdo de um arquivo HTML local.

    Args:
        file_path (str): O caminho para o arquivo HTML.

    Returns:
        str: O conteúdo do arquivo HTML como uma string, ou None se houver um erro.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}")
        return None

def extract_urls(html, base_url, ignored_extensions=['.txt', '.pdf', '.docx']):
    """
    Extrai todas as URLs do conteúdo HTML fornecido, resolvendo URLs relativas e ignorando fragmentos de hash.

    Args:
        html (str): O conteúdo HTML para extrair URLs.
        base_url (str): A URL base usada para resolver URLs relativas.

    Returns:
        set: Um conjunto de URLs extraídas do conteúdo HTML.
    """
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Resolve URLs relativas e filtra por fragmento de hash
        full_url = urljoin(base_url, href.split('#', 1)[0])
        # Ignora URLs que terminam com extensões específicas de arquivo
        if any(full_url.endswith(ext) for ext in ignored_extensions):
            continue
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            urls.add(full_url)
    return urls

def html_to_markdown(html):
    """
    Converte conteúdo HTML para o formato Markdown.

    Parameters:
    html (str): O conteúdo HTML a ser convertido.

    Returns:
    str: A representação em Markdown do conteúdo HTML.
    """
    # Usando readability para extrair o conteúdo principal
    document = Document(html)
    summary = document.summary()

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    return converter.handle(summary)

def generate_filename(file_path, base_folder):
    """
    Gera um nome de arquivo com base no caminho do arquivo e na pasta base.

    Args:
        file_path (str): O caminho completo do arquivo HTML.
        base_folder (str): O diretório base onde os arquivos HTML estão armazenados.

    Returns:
        str: O nome do arquivo gerado.
    """
    # Obtém o caminho relativo do arquivo em relação à pasta base
    relative_path = os.path.relpath(file_path, base_folder)
    
    # Remove a extensão do arquivo
    relative_path_no_ext = os.path.splitext(relative_path)[0]
    
    # Substitui os separadores de caminho por hífens
    filename = relative_path_no_ext.replace(os.sep, '-').lower() + ".md"
    
    return filename

def save_markdown(markdown, folder, filename):
    # Cria todos os diretórios necessários
    os.makedirs(folder, exist_ok=True)
    
    filepath = os.path.join(folder, filename)
    print(f"Salvando {filename} em {folder}")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)

def scrape_site(base_folder, base_url):
    """
    Faz o scraping de arquivos HTML locais, salvando o conteúdo como arquivos markdown.

    Args:
        base_folder (str): O diretório base onde os arquivos HTML estão armazenados.
        base_url (str): A URL base do site.

    Returns:
        None
    """

    # Define o caminho para o diretório de saída
    output_folder = os.path.join(os.path.dirname(__file__), 'output')
    
    # Cria o diretório de saída se não existir
    os.makedirs(output_folder, exist_ok=True)
    print(f"Salvando arquivos em {output_folder}")
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                html = download_page(file_path)
                if html:
                    markdown = html_to_markdown(html)
                    filename = generate_filename(file_path, base_folder)
                    save_markdown(markdown, output_folder, filename)

def clean_directory(folder):
    """
    Deleta todos os arquivos e pastas no diretório especificado.

    Args:
        folder (str): O caminho para o diretório a ser limpo.

    Raises:
        OSError: Se houver um erro ao deletar arquivos ou pastas.
    """
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Falha ao deletar {file_path}. Motivo: {e}')

# Obtém o diretório raiz do projeto, subindo dois níveis
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
print(project_root)
# Constrói o caminho para a pasta vectorbt_pro_site
base_folder = os.path.join(project_root, 'vectorbt_pro_site')

# Verifica se a pasta existe
if not os.path.exists(base_folder):
    raise FileNotFoundError(f"A pasta {base_folder} não foi encontrada.")

# Continua com o restante do código
base_url = 'https://vectorbt.pro/'  # Mantenha isso para compatibilidade com a função generate_filename

clean_directory('output')
scrape_site(base_folder, base_url)
print("Scraping completo.")
