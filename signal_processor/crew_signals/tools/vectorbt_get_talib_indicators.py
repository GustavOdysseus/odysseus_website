from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel
import vectorbtpro as vbt

class TALibAvailableIndicatorsTool(BaseTool):
    name: str = "talib_available_indicators"
    description: str = (
        "Lista todos os indicadores técnicos disponíveis no TA-Lib, "
        "retornando uma lista ordenada com o total de indicadores disponíveis"
    )
    
    def _run(self) -> dict:
        """Executa a ferramenta para listar indicadores TA-Lib disponíveis."""
        try:
            # Obtém apenas os indicadores do TA-Lib
            indicators = vbt.IF.list_indicators(location="talib")
            
            # Organiza os indicadores por grupos
            grouped_indicators = {}
            for ind in sorted(indicators):
                try:
                    indicator_class = vbt.IF.get_indicator(ind)
                    group = (
                        indicator_class.group_name 
                        if hasattr(indicator_class, 'group_name') 
                        else "Outros"
                    )
                    
                    if group not in grouped_indicators:
                        grouped_indicators[group] = []
                    
                    grouped_indicators[group].append({
                        "name": ind,
                        "short_name": (
                            indicator_class.short_name 
                            if hasattr(indicator_class, 'short_name') 
                            else ind
                        )
                    })
                except:
                    if "Não Classificados" not in grouped_indicators:
                        grouped_indicators["Não Classificados"] = []
                    grouped_indicators["Não Classificados"].append({
                        "name": ind,
                        "short_name": ind
                    })
            
            return {
                "total_indicators": len(indicators),
                "indicators_by_group": grouped_indicators,
                "all_indicators": sorted(indicators)
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "message": "Erro ao listar indicadores TA-Lib"
            }

if __name__ == "__main__":
    tool = TALibAvailableIndicatorsTool()
    
    # Listar indicadores TA-Lib
    print("\nIndicadores TA-Lib disponíveis:")
    result = tool.run()
    
    # Exibe o resultado de forma organizada
    print(f"\nTotal de indicadores: {result['total_indicators']}")
    print("\nIndicadores por grupo:")
    for group, indicators in result['indicators_by_group'].items():
        print(f"\n{group}:")
        for ind in indicators:
            print(f"  - {ind['name']} ({ind['short_name']})")