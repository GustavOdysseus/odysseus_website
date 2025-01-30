from typing import Dict, List, Optional, Type, Union, Any
import warnings
import numpy as np

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import vectorbtpro as vbt
import pandas as pd

# Filtrar warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

# Monkey patch para o pandas_ta
np.NaN = np.nan  # Adiciona NaN como atributo do numpy

class VectorBTRunIndicatorInput(BaseModel):
    """Schema de entrada para a ferramenta VectorBTRunIndicator."""
    
    indicators: Union[str, List[str]] = Field(
        ...,
        description=(
            "Indicador ou lista de indicadores a serem executados. Pode ser:\n"
            "1. Um único indicador: 'vbt:BBANDS'\n"
            "2. Lista de indicadores: ['talib:BBANDS', 'talib:RSI']\n"
            "3. Todos os indicadores de uma fonte: 'provider:*'\n"
            "\nProvedores disponíveis:\n"
            "- vbt: 37 indicadores do VectorBT\n"
            "- talib: 174 indicadores do TA-Lib\n"
            "- pandas_ta: 130 indicadores do Pandas TA\n"
            "- ta: 83 indicadores do Technical Analysis\n"
            "- technical: 91 indicadores do Technical\n"
            "- techcon: 18 indicadores do TechCon\n"
            "- smc: 23 indicadores do Smart Money Concepts\n"
            "- wqa101: 101 indicadores do World Quant Alphas"
        )
    )
    data: Any = Field(
        ...,
        description="Objeto vbt.Data contendo os dados de mercado"
    )
    symbol: Optional[str] = Field(
        None,
        description="Símbolo específico para executar o indicador. Se None, usa todos os símbolos"
    )
    params: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "Parâmetros para os indicadores. Pode ser:\n"
            "1. Parâmetros simples: {'window': 20}\n"
            "2. Múltiplos valores: {'window': [10, 20, 30]}\n"
            "3. Por indicador: {'talib_bbands': {'window': 20}, 'talib_rsi': {'window': 14}}"
        )
    )
    unpack: Union[bool, str] = Field(
        False,
        description=(
            "Como desempacotar os resultados:\n"
            "- True: Desempacota em arrays separados\n"
            "- 'dict': Converte para dicionário\n"
            "- 'frame': Converte para DataFrame\n"
            "- 'data': Converte para objeto Data"
        )
    )
    concat: bool = Field(
        True,
        description="Se True, concatena os resultados em um único DataFrame"
    )
    hide_params: bool = Field(
        True,
        description="Se True, oculta os parâmetros nos nomes das colunas"
    )
    param_product: bool = Field(
        False,
        description="Se True, cria produto cartesiano dos parâmetros"
    )
    parallel: bool = Field(
        False,
        description="Se True, executa em paralelo"
    )
    execute_kwargs: Optional[Dict[str, Any]] = Field(
        None,
        description="Argumentos adicionais para execução em paralelo"
    )
    filter_results: bool = Field(
        True,
        description="Se True, filtra resultados vazios"
    )
    raise_no_results: bool = Field(
        True,
        description="Se True, levanta erro quando não há resultados"
    )

class VectorBTRunIndicator(BaseTool):
    """Ferramenta para executar indicadores do VectorBT Pro."""
    
    name: str = "VectorBT Run Indicator"
    description: str = """
    Executa indicadores técnicos usando o VectorBT Pro.
    
    Provedores disponíveis:
    - vbt: 37 indicadores do VectorBT
    - talib: 174 indicadores do TA-Lib
    - pandas_ta: +130 indicadores do Pandas TA
    - ta: 83 indicadores do Technical Analysis
    - technical: Médias móveis e outros
    - techcon: 18 indicadores do TechCon
    - smc: 23 indicadores do Smart Money Concepts
    - wqa101: 101 indicadores do World Quant Alphas
    
    Exemplos de uso:
    1. Indicador único:
       - indicators="talib:RSI"
       - params={"window": 14}
    
    2. Múltiplos indicadores:
       - indicators=["talib:BBANDS", "vbt:RSI"]
       - params={
           "talib_bbands": {"window": 20},
           "rsi": {"window": 14}
         }
    
    3. Todos indicadores de um provedor:
       - indicators="talib:*"
    """
    args_schema: Type[BaseModel] = VectorBTRunIndicatorInput

    def _format_output(self, result: Any) -> Any:
        """Formata a saída para ser mais legível."""
        if isinstance(result, pd.DataFrame):
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.float_format', lambda x: '%.2f' % x if pd.notnull(x) else '')
            
            # Remover colunas com todos os valores NaN
            if len(result.columns) > 10:  # Só limpa se tiver muitas colunas
                result = result.dropna(axis=1, how='all')
            
            return result
        elif isinstance(result, tuple):
            return tuple(self._format_output(r) for r in result)
        elif isinstance(result, dict):
            if "error" in result:
                return f"Erro: {result['error']}\nMensagem: {result['message']}"
        elif hasattr(result, 'to_frame'):
            # Converter resultado para DataFrame
            try:
                return self._format_output(result.to_frame())
            except:
                try:
                    # Tentar converter usando o método main_output
                    return self._format_output(result.main_output.to_frame())
                except:
                    pass
        return result

    def _run(
            self,
            indicators: Union[str, List[str]],
            data: vbt.Data,
            symbol: Optional[str] = None,
            params: Optional[Dict[str, Any]] = None,
            unpack: Union[bool, str] = False,
            concat: bool = True,
            hide_params: bool = True,
            param_product: bool = False,
            parallel: bool = False,
            execute_kwargs: Optional[Dict[str, Any]] = None,
            filter_results: bool = True,
            raise_no_results: bool = True
        ) -> Any:
        """
        Executa indicadores no VectorBT.
        """
        try:
            # Selecionar símbolo específico se fornecido
            if symbol is not None:
                data = data.select_symbols(symbol)
            
            # Preparar parâmetros base
            run_kwargs = {
                "unpack": unpack,
                "concat": concat,
                "hide_params": hide_params,
                "param_product": param_product,
                "filter_results": filter_results,
                "raise_no_results": raise_no_results
            }

            # Adicionar execute_kwargs se parallel=True
            if parallel and execute_kwargs:
                run_kwargs["execute_kwargs"] = execute_kwargs

            # Identificar o provedor
            if isinstance(indicators, str):
                provider = indicators.split(":")[0] if ":" in indicators else "vbt"
            else:
                provider = "vbt"  # assume vbt para lista de indicadores

            # Remover parâmetros não suportados baseado no provedor
            if provider not in ["vbt", "smc", "wqa101"]:
                # Esses provedores não suportam parallel
                run_kwargs.pop("execute_kwargs", None)
                if params:
                    params = {k: v for k, v in params.items() if k != "parallel"}

            # Executar indicador(es)
            result = data.run(
                indicators,
                func_kwargs=params,
                **run_kwargs
            )

            return self._format_output(result)

        except Exception as e:
            return {
                "error": str(type(e).__name__),
                "message": str(e)
            }

if __name__ == "__main__":
    # Exemplo de uso
    from tools.fetch_binance_data import FetchBinanceDataTool
    
    # Criar instâncias das ferramentas
    data_tool = FetchBinanceDataTool()
    indicator_tool = VectorBTRunIndicator()
    
    # Baixar dados
    print("\nBaixando dados da Binance...")
    market_data = data_tool._run(
        ["DOGEUSDT"],
        timeframe="1h",
        start="3 months ago",
        market_type="futures"
    )
    print(f"\nDados obtidos: {list(market_data.features)}")
    print(market_data)
    print(market_data.symbols)
    
    # Testar indicadores de cada provedor
    providers = [
        ("vbt", "Indicadores nativos do VectorBT"),
        ("talib", "Indicadores do TA-Lib"),
        ("pandas_ta", "Indicadores do Pandas TA"),
        ("ta", "Indicadores do Technical Analysis"),
        ("technical", "Indicadores do Technical"),
        ("techcon", "Indicadores de Consenso Técnico"),
        ("smc", "Smart Money Concepts"),
        ("wqa101", "World Quant Alphas")
    ]
    
    for provider, description in providers:
        print(f"\n{'='*80}")
        print(f"Testando indicadores do provedor: {provider} - {description}")
        print('='*80)
        
        # 1. Testar um indicador específico
        if provider == "vbt":
            indicator = "BBANDS"
            params = {"window": 20}
        elif provider == "talib":
            indicator = "RSI"
            params = {"timeperiod": 14}
        elif provider == "pandas_ta":
            indicator = "sma"
            params = {"length": 20}
        elif provider == "ta":
            indicator = "SMAIndicator"
            params = {"window": 20}
        elif provider == "technical":
            indicator = "ROLLING_MEAN"
            params = {"window": 20}
        elif provider == "techcon":
            indicator = "MACON"
            params = {"window": 20}
        elif provider == "smc":
            indicator = "SWING_HIGHS_LOWS"
            params = {"window": 20}
        else:  # wqa101
            indicator = "1"
            params = {}
            
        print(f"\n1. Testando indicador específico: {indicator}")
        result = indicator_tool._run(
            indicators=f"{provider}:{indicator}",
            data=market_data,
            params=params
            #unpack="frame"  # Forçar saída como DataFrame
        )
        print(result)
        
        # 2. Testar todos os indicadores do provedor
        print(f"\n2. Testando todos os indicadores do {provider}:")
        result = indicator_tool._run(
            indicators=f"{provider}:*",
            data=market_data
        )
        if isinstance(result, pd.DataFrame):
            print(f"\nTotal de indicadores: {len(result.columns)}")
            print("\nPrimeiras linhas dos dados:")
            print(result)

    # Simbolos disponíveis
    print("\nSimbols disponíveis:")
    print(market_data.symbols)
