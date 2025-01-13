from typing import Optional, List
from pydantic import BaseModel, Field
from crewai_tools import BaseTool
import vectorbt as vbt

class VBTQuerySchema(BaseModel):
    query: str = Field(
        description="A pergunta ou consulta sobre o VectorBT Pro"
    )
    object_name: Optional[str] = Field(
        default=None,
        description="Nome do objeto VBT específico para consulta (ex: 'Portfolio', 'Trades', 'PFO')"
    )
    search_type: Optional[str] = Field(
        default="all",
        description="Tipo de busca: 'api' (documentação API), 'docs' (documentação geral), 'messages' (mensagens Discord), 'examples' (exemplos de código), ou 'all'"
    )
    code_only: Optional[bool] = Field(
        default=False,
        description="Se True, retorna apenas exemplos de código relacionados"
    )

class VectorBTProKnowledgeTool(BaseTool):
    name: str = "VectorBT Pro Knowledge Assistant"
    description: str = """
    Ferramenta avançada para consultar o conhecimento do VectorBT Pro, incluindo:
    - Documentação oficial da API
    - Exemplos práticos de código
    - Discussões da comunidade no Discord
    - Tutoriais e guias
    - Padrões de uso e melhores práticas
    """
    args_schema: type[BaseModel] = VBTQuerySchema

    def _execute(
        self, 
        query: str, 
        object_name: Optional[str] = None,
        search_type: str = "all",
        code_only: bool = False
    ) -> str:
        try:
            # Inicializa os assets de conhecimento
            pages_asset = vbt.PagesAsset.pull()
            messages_asset = vbt.MessagesAsset.pull()
            
            if object_name:
                # Busca específica por objeto
                asset_names = [search_type] if search_type != "all" else None
                
                if hasattr(vbt, object_name):
                    obj = getattr(vbt, object_name)
                    if code_only:
                        return vbt.find_examples(obj).minimize()
                    else:
                        return vbt.find_assets(
                            obj,
                            asset_names=asset_names,
                            minimize=True
                        ).chat(query)
                else:
                    # Busca por palavra-chave
                    combined_asset = (
                        pages_asset.find(object_name, mode="substring") +
                        messages_asset.find(object_name, mode="substring")
                    )
                    if code_only:
                        return combined_asset.find_code().minimize()
                    else:
                        return combined_asset.minimize().chat(query)
            else:
                # Busca geral
                if code_only:
                    combined_asset = (
                        pages_asset.find(query, mode="substring").find_code() +
                        messages_asset.find(query, mode="substring").find_code()
                    )
                    return combined_asset.minimize()
                else:
                    combined_asset = (
                        pages_asset.find(query, mode="substring") +
                        messages_asset.find(query, mode="substring")
                    )
                    return combined_asset.minimize().chat(query)

        except Exception as e:
            return f"Erro ao consultar VectorBT Pro: {str(e)}"