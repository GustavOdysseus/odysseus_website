from crewai.tools import BaseTool
from typing import List, Type
from pydantic import BaseModel, Field
import vectorbtpro as vbt

class TALibIndicatorParamsInput(BaseModel):
    """Schema de entrada para a ferramenta TALibIndicatorParamsTool."""
    indicators: List[str] = Field(
        ..., 
        description="Lista de nomes de indicadores TA-Lib para obter informações detalhadas"
    )

class TALibIndicatorParamsTool(BaseTool):
    name: str = "talib_indicator_params"
    description: str = (
        "Obtém informações detalhadas sobre os parâmetros necessários "
        "para um ou mais indicadores TA-Lib específicos"
    )
    args_schema: Type[BaseModel] = TALibIndicatorParamsInput
    
    def _run(self, indicators: List[str]) -> dict:
        """Executa a ferramenta para obter parâmetros dos indicadores."""
        try:
            result = {}
            for indicator_name in indicators:
                try:
                    indicator_class = vbt.IF.get_indicator(indicator_name)
                    if not indicator_class:
                        result[indicator_name] = {
                            "error": f"Indicador '{indicator_name}' não encontrado no TA-Lib"
                        }
                        continue
                        
                    result[indicator_name] = {
                        "input_names": indicator_class.input_names,
                        "param_names": indicator_class.param_names,
                        "param_defaults": indicator_class.param_defaults,
                        "output_names": indicator_class.output_names,
                        "short_name": indicator_class.short_name if hasattr(indicator_class, 'short_name') else None,
                        "group_name": indicator_class.group_name if hasattr(indicator_class, 'group_name') else None
                    }
                except Exception as e:
                    result[indicator_name] = {
                        "error": f"Erro ao obter informações do indicador: {str(e)}"
                    }
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "message": "Erro ao obter parâmetros dos indicadores"
            }

if __name__ == "__main__":
    tool = TALibIndicatorParamsTool()
    
    # Exemplo com um único indicador
    print("\nParâmetros do RSI:")
    result = tool.run(indicators=["RSI"])
    print(result)
    
    # Exemplo com múltiplos indicadores
    print("\nParâmetros de múltiplos indicadores:")
    result = tool.run(indicators=["MACD", "BBANDS", "ADX"])
    print(result)