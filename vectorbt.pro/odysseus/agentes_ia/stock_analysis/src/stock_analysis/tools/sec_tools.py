import os
from typing import Any, Optional, Type
from pydantic import BaseModel, Field
from crewai_tools import RagTool
from sec_api import QueryApi  # Make sure to have sec_api installed
from embedchain.models.data_type import DataType
import requests
import html2text
import re

class FixedSEC10KToolSchema(BaseModel):
    """Input para SEC10KTool."""
    search_query: str = Field(
        ...,
        description="Consulta obrigatória que você deseja pesquisar no relatório 10-K",
    )
    
    class Config:
        arbitrary_types_allowed = True

class SEC10KToolSchema(FixedSEC10KToolSchema):
    """Input para SEC10KTool."""
    stock_name: str = Field(
        ..., description="Nome válido da ação que você deseja pesquisar"
    )
    
    class Config:
        arbitrary_types_allowed = True

class SEC10KTool(RagTool):
    name: str = "Pesquisar no formulário 10-K especificado"
    description: str = "Uma ferramenta que pode ser usada para fazer busca semântica em um formulário 10-K de uma empresa específica."
    args_schema: Type[BaseModel] = SEC10KToolSchema

    def __init__(self, stock_name: Optional[str] = None, **kwargs):
        print("iniciando init")
        super().__init__(**kwargs)
        if stock_name is not None:
            content = self.get_10k_url_content(stock_name)
            if content:
                self.add(content)
                self.description = f"Uma ferramenta que pode ser usada para fazer busca semântica no conteúdo do último formulário 10-K SEC de {stock_name} como arquivo txt."
                self.args_schema = FixedSEC10KToolSchema
                self._generate_description()

    def get_10k_url_content(self, stock_name: str) -> Optional[str]:
        """Busca o conteúdo URL como txt do último formulário 10-K para o nome da ação fornecido."""
        try:
            queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
            query = {
                "query": {
                    "query_string": {
                        "query": f"ticker:{stock_name} AND formType:\"10-K\""
                    }
                },
                "from": "0",
                "size": "1",
                "sort": [{ "filedAt": { "order": "desc" }}]
            }
            filings = queryApi.get_filings(query)['filings']
            if len(filings) == 0:
                print("Nenhum arquivo encontrado para esta ação.")
                return None

            url = filings[0]['linkToFilingDetails']
            
            headers = {
                "User-Agent": "crewai.com bisan@crewai.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  
            h = html2text.HTML2Text()
            h.ignore_links = False
            text = h.handle(response.content.decode("utf-8"))

            text = re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)
            return text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error fetching 10-K URL: {e}")
            return None

    def add(self, *args: Any, **kwargs: Any) -> None:
        kwargs["data_type"] = DataType.TEXT
        super().add(*args, **kwargs)

    def _run(self, search_query: str, **kwargs: Any) -> Any:
        return super()._run(query=search_query, **kwargs)


class FixedSEC10QToolSchema(BaseModel):
    """Input para SEC10QTool."""
    search_query: str = Field(
        ...,
        description="Consulta obrigatória que você deseja pesquisar no relatório 10-Q",
    )
    
    class Config:
        arbitrary_types_allowed = True

class SEC10QToolSchema(FixedSEC10QToolSchema):
    """Input para SEC10QTool."""
    stock_name: str = Field(
        ..., description="Nome válido da ação que você deseja pesquisar"
    )
    
    class Config:
        arbitrary_types_allowed = True

class SEC10QTool(RagTool):
    name: str = "Pesquisar no formulário 10-Q especificado"
    description: str = "Uma ferramenta que pode ser usada para fazer busca semântica em um formulário 10-Q de uma empresa específica."
    args_schema: Type[BaseModel] = SEC10QToolSchema

    def __init__(self, stock_name: Optional[str] = None, **kwargs):
        print("iniciando init")
        super().__init__(**kwargs)
        if stock_name is not None:
            content = self.get_10q_url_content(stock_name)
            if content:
                self.add(content)
                self.description = f"Uma ferramenta que pode ser usada para fazer busca semântica no conteúdo do último formulário 10-Q SEC de {stock_name} como arquivo txt."
                self.args_schema = FixedSEC10QToolSchema
                self._generate_description()

    def get_10q_url_content(self, stock_name: str) -> Optional[str]:
        """Busca o conteúdo URL como txt do último formulário 10-Q para o nome da ação fornecido."""
        try:
            queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
            query = {
                "query": {
                    "query_string": {
                        "query": f"ticker:{stock_name} AND formType:\"10-Q\""
                    }
                },
                "from": "0",
                "size": "1",
                "sort": [{ "filedAt": { "order": "desc" }}]
            }
            filings = queryApi.get_filings(query)['filings']
            if len(filings) == 0:
                print("Nenhum arquivo encontrado para esta ação.")
                return None

            url = filings[0]['linkToFilingDetails']
            
            headers = {
                "User-Agent": "crewai.com bisan@crewai.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            h = html2text.HTML2Text()
            h.ignore_links = False
            text = h.handle(response.content.decode("utf-8"))

            # Removing all non-English words, dollar signs, numbers, and newlines from text
            text = re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)
            return text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error fetching 10-Q URL: {e}")
            return None

    def add(self, *args: Any, **kwargs: Any) -> None:
        kwargs["data_type"] = DataType.TEXT
        super().add(*args, **kwargs)

    def _run(self, search_query: str, **kwargs: Any) -> Any:
        return super()._run(query=search_query, **kwargs)

