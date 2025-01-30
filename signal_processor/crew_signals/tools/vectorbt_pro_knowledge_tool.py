from typing import Type, Optional
import os
import re

from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
import vectorbtpro as vbt


class VBTQuerySchema(BaseModel):
    """Schema de entrada para a ferramenta VectorBT Pro Knowledge."""

    query: str = Field(
        ...,
        description="A pergunta ou consulta sobre o VectorBT Pro"
    )
    object_name: Optional[str] = Field(
        None,
        description="Nome do objeto VBT específico para consulta (ex: 'Portfolio', 'Trades', 'PFO')"
    )
    search_type: Optional[str] = Field(
        "all",
        description="Tipo de busca: 'api' (documentação API), 'docs' (documentação geral), 'messages' (mensagens Discord), 'examples' (exemplos de código), ou 'all'"
    )
    code_only: Optional[bool] = Field(
        False,
        description="Se True, retorna apenas exemplos de código relacionados"
    )


class VectorBTProKnowledgeTool(BaseTool):
    """Ferramenta para consultar a base de conhecimento do VectorBT Pro."""
    name: str = "VectorBT Pro Knowledge Tool"
    description: str = (
        "Consulta a base de conhecimento do VectorBT Pro para encontrar informações "
        "sobre uso, exemplos e documentação."
    )
    args_schema: Type[BaseModel] = VBTQuerySchema

    # Atributos privados como campos da classe
    _pages_asset: Optional[vbt.PagesAsset] = PrivateAttr(default=None)
    _messages_asset: Optional[vbt.MessagesAsset] = PrivateAttr(default=None)

    def __init__(self, **kwargs):
        """Inicializa a ferramenta de conhecimento do VectorBT Pro."""
        super().__init__(**kwargs)
        self.load_assets()

    def load_assets(self):
        """Carrega os assets de conhecimento do VectorBT Pro."""
        # Por enquanto, vamos usar assets vazios
        self._pages_asset = None
        self._messages_asset = None
        print("Usando VectorBT Pro Knowledge Tool sem assets (modo offline)")

    def _extract_code_blocks(self, content: str) -> str:
        """Extrai blocos de código do conteúdo."""
        if not content:
            return ""
        
        # Remove títulos duplicados
        content = re.sub(r'(?:python|pycon)\s+title="[^"]*"\s*\n', '\n', content)
        
        # Busca código em blocos de código
        code_blocks = []
        pattern = r'```(?:python|pycon)?\s*(.*?)\s*```'
        matches = re.finditer(pattern, content, re.DOTALL)
        for match in matches:
            code = match.group(1).strip()
            if code:
                # Remove comentários de título
                code = re.sub(r'title="[^"]*"\s*\n', '\n', code)
                # Remove linhas vazias extras
                code = re.sub(r'\n{3,}', '\n\n', code)
                code_blocks.append(code)
                
        # Busca código em backticks simples
        pattern = r'`([^`]+)`'
        matches = re.finditer(pattern, content)
        for match in matches:
            code = match.group(1).strip()
            if code and len(code.split()) > 1:  # Ignora palavras únicas
                code_blocks.append(code)
                
        if not code_blocks:
            return ""
            
        # Formata os blocos de código
        formatted_blocks = []
        for block in code_blocks:
            # Remove linhas vazias no início e fim
            block = block.strip()
            # Adiciona marcadores de código Python
            formatted_blocks.append(f"```python\n{block}\n```")
            
        return "\n\n".join(formatted_blocks)

    def _score_relevance(self, result: str, query: str) -> float:
        """Calcula pontuação de relevância do resultado."""
        result = str(result).lower()
        query = query.lower()
        
        # Pontuação base pela ocorrência exata
        score = result.count(query) * 2
        
        # Pontuação por palavras individuais
        for word in query.split():
            score += result.count(word)
            
        # Bônus se contiver código
        if "```" in result:
            score *= 1.5
            
        # Normaliza pelo tamanho do resultado
        return score / (len(result) + 1)

    def _get_top_results(self, results: list[str], query: str, limit: int = 5) -> list[str]:
        """Retorna os resultados mais relevantes."""
        if not results:
            return []
            
        # Calcula relevância e ordena
        scored_results = [
            (self._score_relevance(r, query), r) 
            for r in results
        ]
        scored_results.sort(reverse=True)
        
        # Retorna os top N resultados
        return [r for _, r in scored_results[:limit]]

    def _run(
        self,
        query: str,
        object_name: Optional[str] = None,
        search_type: str = "all",
        code_only: bool = False
    ) -> str:
        """Executa a busca de conhecimento."""
        if not self._pages_asset and not self._messages_asset:
            return "VectorBT Pro Knowledge Tool está operando em modo offline. Para habilitar todas as funcionalidades, configure o GITHUB_TOKEN ou forneça os arquivos pages.json e messages.json."
        
        try:
            find_kwargs = {
                "find_all": True,
                "silence_warnings": True
            }
            
            # Se houver um objeto específico
            if object_name:
                try:
                    # Busca na API
                    api_results = self._pages_asset.find_obj_api(
                        object_name,
                        incl_bases=True,
                        incl_refs=True
                    ).get()
                    
                    # Busca na documentação
                    doc_results = self._pages_asset.find_obj_docs(
                        object_name,
                        up_aggregate=True
                    ).get()
                    
                    all_results = []
                    if api_results:
                        all_results.extend([str(r) for r in api_results])
                    if doc_results:
                        all_results.extend([str(r) for r in doc_results])
                    
                    if not all_results:
                        return f"Nenhuma informação encontrada para o objeto {object_name}"
                    
                    return "\n\n".join(all_results[:5])  # Limita a 5 resultados
                
                except Exception as e:
                    return f"Erro ao buscar objeto {object_name}: {str(e)}"

            # Busca por código
            if code_only:
                try:
                    # Busca código diretamente
                    code_results = self._pages_asset.find_code(
                        query,
                        in_blocks=True,
                        language="python"
                    ).get()
                    
                    if code_results:
                        return "\n\n".join(code_results[:5])  # Limita a 5 blocos de código
                    
                    # Se não encontrar, tenta buscar em exemplos
                    example_results = self._pages_asset.find(
                        query,
                        path="examples",
                        find_all=True
                    ).get()
                    
                    if example_results:
                        codes = []
                        for result in example_results[:5]:
                            code = self._extract_code_blocks(str(result))
                            if code:
                                codes.append(code)
                        if codes:
                            return "\n\n".join(codes)
                    
                    return "Nenhum exemplo de código encontrado."
                    
                except Exception as e:
                    return f"Erro na busca de código: {str(e)}"

            # Busca geral combinada
            try:
                # Busca em páginas
                page_results = self._pages_asset.find(
                    query,
                    path="content",
                    find_all=True
                ).get()
                
                # Busca em mensagens
                message_results = self._messages_asset.find(
                    query,
                    path="content",
                    find_all=True
                ).get()
                
                # Busca em exemplos
                example_results = self._pages_asset.find(
                    query,
                    path="examples",
                    find_all=True
                ).get()
                
                # Combina resultados
                all_results = []
                if page_results:
                    all_results.extend([str(r) for r in page_results[:10]])
                if message_results:
                    all_results.extend([str(r) for r in message_results[:10]])
                if example_results:
                    all_results.extend([str(r) for r in example_results[:10]])
                    
                # Filtra os mais relevantes
                top_results = self._get_top_results(all_results, query, limit=5)
                
                if not top_results:
                    return "Nenhuma informação encontrada."
                    
                return "\n\n".join(top_results)
                
            except Exception as e:
                if "too long" in str(e).lower():
                    return "O contexto é muito grande. Por favor, tente uma consulta mais específica."
                return f"Erro na busca geral: {str(e)}"

        except Exception as e:
            return f"Erro ao consultar VectorBT Pro: {str(e)}"


if __name__ == "__main__":
    # Criar instância da ferramenta
    tool = VectorBTProKnowledgeTool()
    
    # Exemplos de uso
    print("\n=== Exemplo 1: Busca por objeto específico ===")
    result = tool._run(
        query="Como fazer rebalanceamento semanal?",
        object_name="Portfolio",
        search_type="docs"
    )
    print(result)
    
    print("\n=== Exemplo 2: Busca por código ===")
    result = tool._run(
        query="signal_func_nb",
        code_only=True
    )
    print(result)
    
    print("\n=== Exemplo 3: Busca geral ===")
    result = tool._run(
        query="Como criar um indicador personalizado?"
    )
    print(result)
