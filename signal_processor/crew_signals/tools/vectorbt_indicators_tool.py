from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import vectorbtpro as vbt

class VectorBTIndicatorInput(BaseModel):
    """Schema de entrada para a ferramenta VectorBTIndicatorTool."""
    action: str = Field(
        ..., 
        description="Ação a executar: 'list' para listar indicadores, 'info' para obter detalhes de um indicador específico"
    )
    location: Optional[str] = Field(
        None,
        description="Local para buscar indicadores (ex: 'vbt', 'talib', 'smc', 'wqa101', 'ta', 'technical', 'techcon')"
    )
    indicator_name: Optional[str] = Field(
        None,
        description="Nome do indicador para obter informações detalhadas"
    )

class VectorBTIndicatorTool(BaseTool):
    name: str = "vectorbt_indicators"
    description: str = (
        "Ferramenta para explorar indicadores técnicos disponíveis no VectorBT Pro. "
        "Pode listar todos os indicadores ou obter informações detalhadas de um indicador específico."
    )
    args_schema: Type[BaseModel] = VectorBTIndicatorInput

    def _run(self, action: str, location: Optional[str] = None, indicator_name: Optional[str] = None) -> str:
        try:
            if action == "list":
                # Listar indicadores
                if location:
                    indicators = vbt.IF.list_indicators(location=location)
                else:
                    indicators = vbt.IF.list_indicators()
                locations = vbt.IF.list_locations()
                
                return {
                    "total_indicators": len(indicators),
                    "indicators": indicators,
                    "available_locations": locations
                }
                
            elif action == "info":
                # Obter informações de um indicador específico
                if not indicator_name:
                    return {"error": "indicator_name é obrigatório para action='info'"}
                    
                indicator_class = vbt.IF.get_indicator(indicator_name)
                return {
                    "name": indicator_name,
                    "input_names": indicator_class.input_names,
                    "param_names": indicator_class.param_names,
                    "param_defaults": indicator_class.param_defaults,
                    "output_names": indicator_class.output_names
                }
            
            else:
                return {
                    "error": f"Ação '{action}' inválida",
                    "valid_actions": ["list", "info"]
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "message": "Erro ao acessar indicadores"
            }

# Exemplo de uso:
if __name__ == "__main__":
    tool = VectorBTIndicatorTool()
    
    # Listar todos os indicadores
    print("\nTodos os indicadores:")
    result = tool.run(action="list")
    print(result)

    # Listar indicadores do VectorBT
    print("\nIndicadores do VectorBT:")
    result = tool.run(action="list", location="vbt")
    print(result)
    
    # Listar indicadores do TA-Lib
    print("\nIndicadores do TA-Lib:")
    result = tool.run(action="list", location="talib")
    print(result)

    # Listar indicadores do pandas_ta
    print("\nIndicadores do pandas_ta:")
    result = tool.run(action="list", location="pandas_ta")
    print(result)

    # Listar indicadores do ta
    print("\nIndicadores do ta:")
    result = tool.run(action="list", location="ta")
    print(result)

    # Listar indicadores do technical
    print("\nIndicadores do technical:")
    result = tool.run(action="list", location="technical")
    print(result)

    # Listar indicadores do techcon
    print("\nIndicadores do techcon:")
    result = tool.run(action="list", location="techcon")
    print(result)

    # Listar indicadores do smc
    print("\nIndicadores do smc:")
    result = tool.run(action="list", location="smc")
    print(result)

    # Listar indicadores do wqa101
    print("\nIndicadores do wqa101:")
    result = tool.run(action="list", location="wqa101")
    print(result)
    
    # Obter informações do RSI
    print("\nInformações do RSI:")
    result = tool.run(action="info", indicator_name="RSI")
    print(result)

    # Obter informações do BBANDS
    print("\nInformações do BBANDS:")
    result = tool.run(action="info", indicator_name="BBANDS")
    print(result)

    # Obter informações do 99
    print("\nInformações do 99:")
    result = tool.run(action="info", indicator_name="99")
    print(result)

    # Obter informações do PREVIOUS_HIGH_LOW
    print("\nInformações do PREVIOUS_HIGH_LOW:")
    result = tool.run(action="info", indicator_name="PREVIOUS_HIGH_LOW")
    print(result)

    # Obter informações do SUMCON
    print("\nInformações do SUMCON:")
    result = tool.run(action="info", indicator_name="SUMCON")
    print(result)

    # Obter informações do CHAIKIN_MONEY_FLOW
    #print("\nInformações do CHAIKIN_MONEY_FLOW:")
    #result = tool.run(action="info", indicator_name="CHAIKIN_MONEY_FLOW")
    #print(result)

    # Obter informações do KSTIndicator
    print("\nInformações do KSTIndicator:")
    result = tool.run(action="info", indicator_name="KSTIndicator")
    print(result)

    # Obter informações do KURTOSIS
    #print("\nInformações do KURTOSIS:")
    #result = tool.run(action="info", indicator_name="KURTOSIS")
    #print(result)

    # Obter informações do CDLGAPSIDESIDEWHITE
    print("\nInformações do CDLGAPSIDESIDEWHITE:")
    result = tool.run(action="info", indicator_name="CDLGAPSIDESIDEWHITE")
    print(result)

    # Obter informações do PATSIM
    print("\nInformações do PATSIM:")
    result = tool.run(action="info", indicator_name="PATSIM")
    print(result)

    # Obter informações do RPROBNX
    print("\nInformações do RPROBNX:")
    result = tool.run(action="info", indicator_name="RPROBNX")
    print(result)

