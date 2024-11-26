from typing import List, Optional, Dict, Any, Callable
from pydantic import BaseModel, Field, PrivateAttr
from crewai.tools import BaseTool
from crewai_tools import PDFSearchTool, FileReadTool
import arxiv
import os
from pathlib import Path
import json
from datetime import datetime
import pymupdf 
from src.logging.logging_config import LoggingConfig
import yaml
import logging

# Carrega os prompts do arquivo YAML
PROMPTS_FILE = Path(__file__).parent / "prompts" / "arxiv.yaml"
with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
    PROMPTS = yaml.safe_load(f)["tools"]

class ArxivSearchSchema(BaseModel):
    """Schema para busca no Arxiv."""
    query: str = Field(
        ..., 
        description="Query de busca para o Arxiv",
        min_length=3
    )
    max_results: int = Field(
        default=10, 
        description="Número máximo de resultados",
        ge=1,
        le=100
    )
    sort_by: str = Field(
        default="relevance",
        description="Ordenação dos resultados",
        enum=["relevance", "lastUpdatedDate", "submittedDate"]
    )
    sort_order: str = Field(
        default="descending",
        description="Ordem de classificação (ascending/descending)",
        enum=["ascending", "descending"]
    )

class ArxivDownloadSchema(BaseModel):
    """Schema para download de artigos do Arxiv."""
    article_id: str = Field(..., description="ID do artigo no Arxiv")
    save_dir: str = Field(default="downloads", description="Diretório para salvar o PDF")

class ArxivExtractSchema(BaseModel):
    """Schema para extração de conteúdo do PDF."""
    pdf_path: str = Field(..., description="Caminho do arquivo PDF")
    output_format: str = Field(
        default="json",
        description="Formato de saída (json, txt, md)",
        enum=["json", "txt", "md"]
    )

class ArxivSearchContentSchema(BaseModel):
    """Schema para busca semântica no conteúdo do PDF."""
    pdf_path: str = Field(..., description="Caminho do arquivo PDF para busca")
    query: str = Field(
        ..., 
        description="Query para busca semântica no conteúdo",
        min_length=3
    )
    summarize: bool = Field(
        default=True,
        description="Se deve resumir o resultado da busca"
    )

class ArxivReadContentSchema(BaseModel):
    """Schema para leitura do conteúdo extraído do PDF."""
    file_path: str = Field(..., description="Caminho do arquivo extraído (json, txt ou md)")

class ArxivSearchTool(BaseTool):
    """Ferramenta para pesquisar artigos no Arxiv."""
    name: str = PROMPTS["arxiv_search"]["name"]
    description: str = PROMPTS["arxiv_search"]["description"]
    args_schema: type[BaseModel] = ArxivSearchSchema
    cache_function: Callable = lambda _args, _result: True
    result_as_answer: bool = False
    _logger: Optional[logging.Logger] = PrivateAttr(default=None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = LoggingConfig().get_logger(__name__)

    def _run(
        self,
        query: str,
        max_results: int = 10,
        sort_by: str = "relevance",
        sort_order: str = "descending"
    ) -> List[Dict[str, Any]]:
        """Executa a busca no Arxiv."""
        try:
            # Configura o cliente Arxiv
            client = arxiv.Client()
            
            # Mapeamento de valores para SortCriterion e SortOrder
            sort_mapping = {
                "relevance": arxiv.SortCriterion.Relevance,
                "lastupdateddate": arxiv.SortCriterion.LastUpdatedDate,
                "submitteddate": arxiv.SortCriterion.SubmittedDate
            }
            
            order_mapping = {
                "ascending": arxiv.SortOrder.Ascending,
                "descending": arxiv.SortOrder.Descending
            }
            
            # Configura a busca
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=sort_mapping[sort_by.lower()],
                sort_order=order_mapping[sort_order.lower()]
            )
            
            # Realiza a busca
            results = []
            for result in client.results(search):
                article = {
                    "id": result.get_short_id(),
                    "title": result.title,
                    "authors": [author.name for author in result.authors],
                    "summary": result.summary,
                    "published": result.published.isoformat(),
                    "updated": result.updated.isoformat(),
                    "pdf_url": result.pdf_url,
                    "categories": result.categories
                }
                results.append(article)
            
            self._logger.info(f"Encontrados {len(results)} artigos para a query: {query}")
            return results
            
        except Exception as e:
            self._logger.error(f"Erro na busca do Arxiv: {e}")
            raise

class ArxivDownloadTool(BaseTool):
    """Ferramenta para download de artigos do Arxiv."""
    name: str = PROMPTS["arxiv_download"]["name"]
    description: str = PROMPTS["arxiv_download"]["description"]
    args_schema: type[BaseModel] = ArxivDownloadSchema
    cache_function: Callable = lambda _args, _result: True
    result_as_answer: bool = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = LoggingConfig().get_logger(__name__)

    def _run(
        self,
        article_id: str,
        save_dir: str = "papers"
    ) -> str:
        """Realiza o download do artigo."""
        try:
            # Configura o diretório de download
            base_dir = Path(__file__).parent / "downloads" / "arxiv_artigos"
            save_path = base_dir / save_dir
            save_path.mkdir(parents=True, exist_ok=True)
            
            # Verifica se o arquivo já existe
            pdf_path = save_path / f"{article_id}.pdf"
            if pdf_path.exists():
                self._logger.info(f"Artigo já existe no caminho: {pdf_path}")
                return str(pdf_path)
            
            # Busca o artigo
            client = arxiv.Client()
            search = arxiv.Search(id_list=[article_id])
            paper = next(client.results(search))
            
            # Realiza o download
            paper.download_pdf(filename=str(pdf_path))
            
            self._logger.info(f"Artigo baixado com sucesso: {pdf_path}")
            return str(pdf_path)
            
        except Exception as e:
            self._logger.error(f"Erro no download do artigo {article_id}: {e}")
            raise

class ArxivExtractTool(BaseTool):
    """Ferramenta para extrair e estruturar conteúdo de PDFs do Arxiv."""
    name: str = PROMPTS["arxiv_extract"]["name"]
    description: str = PROMPTS["arxiv_extract"]["description"]
    args_schema: type[BaseModel] = ArxivExtractSchema
    cache_function: Callable = lambda _args, _result: True  # Habilita cache
    result_as_answer: bool = False  # Não é resposta final
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = LoggingConfig().get_logger(__name__)

    def _run(
        self,
        pdf_path: str,
        output_format: str = "json"
    ) -> str:
        """Extrai e estrutura o conteúdo do PDF."""
        try:
            # Abre o PDF
            doc = pymupdf.open(pdf_path)
            
            # Extrai o conteúdo
            content = {
                "metadata": {
                    "title": doc.metadata.get("title", ""),
                    "author": doc.metadata.get("author", ""),
                    "subject": doc.metadata.get("subject", ""),
                    "keywords": doc.metadata.get("keywords", ""),
                    "creator": doc.metadata.get("creator", ""),
                    "producer": doc.metadata.get("producer", ""),
                },
                "document_info": {
                    "page_count": len(doc),
                    "file_size": os.path.getsize(pdf_path),
                },
                "content": [],
                "extracted_date": datetime.now().isoformat()
            }
            
            # Extrai texto e informações adicionais de cada página
            for page_num in range(len(doc)):
                page = doc[page_num]
                tables_found = page.find_tables()  # Chama a função find_tables
                page_content = {
                    "page": page_num + 1,
                    "text": page.get_text(),
                    "images": len(page.get_images()),
                    "links": len(page.get_links()),
                    "tables": len(tables_found.tables)  # Acessa o atributo que contém as tabelas
                }
                
                # Tenta extrair o layout da página
                try:
                    blocks = page.get_text("blocks")
                    page_content["blocks"] = [
                        {
                            "text": block[4],
                            "bbox": block[:4],
                            "block_type": block[6]
                        }
                        for block in blocks
                    ]
                except Exception as e:
                    self._logger.warning(f"Erro ao extrair blocos da página {page_num + 1}: {e}")
                
                content["content"].append(page_content)
            
            # Fecha o documento
            doc.close()
            
            # Define o caminho de saída
            base_dir = Path(__file__).parent / "downloads" / "arxiv_artigos"
            output_dir = base_dir / "extracted"
            output_dir.mkdir(parents=True, exist_ok=True)
            base_name = Path(pdf_path).stem
            
            # Salva o conteúdo no formato especificado
            if output_format == "json":
                output_path = output_dir / f"{base_name}.json"
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(content, f, ensure_ascii=False, indent=2)
            
            elif output_format == "txt":
                output_path = output_dir / f"{base_name}.txt"
                with open(output_path, "w", encoding="utf-8") as f:
                    # Metadados
                    f.write("=== Metadados ===\n")
                    for key, value in content["metadata"].items():
                        f.write(f"{key.title()}: {value}\n")
                    
                    # Informações do documento
                    f.write("\n=== Informações do Documento ===\n")
                    for key, value in content["document_info"].items():
                        f.write(f"{key.replace('_', ' ').title()}: {value}\n")
                    
                    # Conteúdo
                    f.write("\n=== Conteúdo ===\n")
                    for page in content["content"]:
                        f.write(f"\n--- Página {page['page']} ---\n")
                        f.write(f"Imagens: {page['images']}\n")
                        f.write(f"Links: {page['links']}\n")
                        f.write(f"Tabelas: {page['tables']}\n\n")
                        f.write(page["text"])
            
            elif output_format == "md":
                output_path = output_dir / f"{base_name}.md"
                with open(output_path, "w", encoding="utf-8") as f:
                    # Título e metadados
                    f.write(f"# {content['metadata']['title']}\n\n")
                    f.write("## Metadados\n\n")
                    for key, value in content["metadata"].items():
                        if value:
                            f.write(f"**{key.title()}:** {value}\n")
                    
                    # Informações do documento
                    f.write("\n## Informações do Documento\n\n")
                    for key, value in content["document_info"].items():
                        f.write(f"**{key.replace('_', ' ').title()}:** {value}\n")
                    
                    # Conteúdo
                    f.write("\n## Conteúdo\n")
                    for page in content["content"]:
                        f.write(f"\n### Página {page['page']}\n\n")
                        f.write(f"- **Imagens:** {page['images']}\n")
                        f.write(f"- **Links:** {page['links']}\n")
                        f.write(f"- **Tabelas:** {page['tables']}\n\n")
                        f.write(page["text"] + "\n")
            
            self._logger.info(f"Conteúdo extraído e salvo em: {output_path}")
            return str(output_path)
            
        except Exception as e:
            self._logger.error(f"Erro na extração do PDF {pdf_path}: {e}")
            raise

class ArxivSearchContentTool(BaseTool):
    """Ferramenta para busca semântica em PDFs do Arxiv."""
    name: str = PROMPTS["arxiv_search_content"]["name"]
    description: str = PROMPTS["arxiv_search_content"]["description"]
    args_schema: type[BaseModel] = ArxivSearchContentSchema
    cache_function: Callable = lambda _args, _result: True
    result_as_answer: bool = False
    _logger: Optional[logging.Logger] = PrivateAttr(default=None)
    _pdf_search: Any = PrivateAttr(default=None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = LoggingConfig().get_logger(__name__)
        self._pdf_search = PDFSearchTool()

    def _run(
        self,
        pdf_path: str,
        query: str,
        summarize: bool = True
    ) -> str:
        """Realiza busca semântica no conteúdo do PDF."""
        try:
            # Configura a ferramenta de busca com o PDF específico
            pdf_search = PDFSearchTool(pdf=pdf_path)
            
            # Realiza a busca semântica
            result = pdf_search.run(query=query)
            
            self._logger.info(f"Busca realizada com sucesso no PDF: {pdf_path}")
            return result
            
        except Exception as e:
            self._logger.error(f"Erro na busca semântica do PDF {pdf_path}: {e}")
            raise

class ArxivReadContentTool(BaseTool):
    """Ferramenta para ler o conteúdo extraído de PDFs do Arxiv."""
    name: str = PROMPTS["arxiv_read_content"]["name"]
    description: str = PROMPTS["arxiv_read_content"]["description"]
    args_schema: type[BaseModel] = ArxivReadContentSchema
    cache_function: Callable = lambda _args, _result: True
    result_as_answer: bool = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = LoggingConfig().get_logger(__name__)
        self._file_reader = FileReadTool()

    def _run(
        self,
        file_path: str
    ) -> str:
        """Lê o conteúdo do arquivo extraído."""
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
            # Lê o conteúdo do arquivo
            content = self.file_reader.run(file_path=file_path)
            
            # Se for JSON, tenta formatar para melhor legibilidade
            if file_path.endswith('.json'):
                try:
                    content_dict = json.loads(content)
                    content = json.dumps(content_dict, ensure_ascii=False, indent=2)
                except json.JSONDecodeError:
                    self._logger.warning("Não foi possível formatar o JSON")
            
            self._logger.info(f"Conteúdo lido com sucesso: {file_path}")
            return content
            
        except Exception as e:
            self._logger.error(f"Erro na leitura do arquivo {file_path}: {e}")
            raise

# Exemplo de uso
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    # Configura logging
    logging_config = LoggingConfig()
    logger = logging_config.get_logger(__name__)
    
    try:
        # Testa a busca
        search_tool = ArxivSearchTool()
        results = search_tool.run(
            query="quantum computing AND machine learning",
            max_results=5
        )
        
        if results:
            # Testa o download
            download_tool = ArxivDownloadTool()
            pdf_path = download_tool.run(
                article_id=results[0]["id"],
                save_dir="papers"
            )
            
            # Testa a extração
            extract_tool = ArxivExtractTool()
            for format in ["json", "txt", "md"]:
                output_path = extract_tool.run(
                    pdf_path=pdf_path,
                    output_format=format
                )
                logger.info(f"Arquivo extraído em formato {format}: {output_path}")
                
            # Testa a busca semântica
            search_content_tool = ArxivSearchContentTool()
            content_result = search_content_tool.run(
                pdf_path=pdf_path,
                query="What are the main findings of this paper?"
            )
            logger.info(f"Resultado da busca semântica: {content_result}")
                
            # Testa a leitura do conteúdo
            read_content_tool = ArxivReadContentTool()
            for format in ["json", "txt", "md"]:
                extracted_file = Path(pdf_path).parent / "extracted" / f"{Path(pdf_path).stem}.{format}"
                if extracted_file.exists():
                    content = read_content_tool.run(file_path=str(extracted_file))
                    logger.info(f"Conteúdo lido do arquivo {format}: {len(content)} caracteres")
                
    except Exception as e:
        logger.error(f"Erro nos testes: {e}")
        logger.exception("Traceback completo:")