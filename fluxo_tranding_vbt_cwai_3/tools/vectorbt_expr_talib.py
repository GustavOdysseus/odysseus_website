from typing import Type, Dict, Any, List, Optional, Union
import vectorbtpro as vbt
import pandas as pd
import numpy as np
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, model_validator


class TALibExpressionSchema(BaseModel):
    """Schema para TALibExpression quando os dados já estão carregados."""
    expression: str = Field(
        ...,
        description="String multi-linha (\"\"\"...\"\"\") contendo a expressão VectorBT completa com: "
                   "1) @settings com factory_kwargs e parâmetros, "
                   "2) cálculo dos indicadores, "
                   "3) definição dos sinais, e "
                   "4) retorno dos sinais na ordem de output_names"
                   "Exemplo de como construir a expressão: "
                   "@settings(dict("
                   "    factory_kwargs=dict("
                   "        class_name='Strategy',"
                   "        input_names=['close'],"
                   "        param_names=['rsi_timeperiod', 'rsi_oversold', 'rsi_overbought', "
                   "                    'bbands_timeperiod', 'bbands_nbdevup', 'bbands_nbdevdn'],"
                   "        output_names=['long_entry', 'long_exit', 'short_entry', 'short_exit']"
                   "    ),"
                   "    rsi_timeperiod = np.arange(7, 30, 7),"
                   "    rsi_oversold = np.arange(20, 36, 5),"
                   "    rsi_overbought = np.arange(65, 81, 5),"
                   "    bbands_timeperiod = np.arange(10, 26, 5),"
                   "    bbands_nbdevup = np.arange(1.5, 3.1, 0.5),"
                   "    bbands_nbdevdn = np.arange(1.5, 3.1, 0.5)"
                   "))"

                   "# Calcular RSI usando talib"
                   "rsi = @talib_RSI(close, timeperiod=rsi_timeperiod)"

                   "# Calcular Bandas de Bollinger usando talib"
                   "bb = @talib_BBANDS("
                   "    close, "
                   "    timeperiod=bbands_timeperiod,"
                   "    nbdevup=bbands_nbdevup,"
                   "    nbdevdn=bbands_nbdevdn"
                   ")"
                   "upperband = bb[0]"
                   "middleband = bb[1]" 
                   "lowerband = bb[2]"

                   "# Gerar sinais"
                   "long_entry = (rsi < rsi_oversold) & (close < lowerband)"
                   "long_exit = (rsi > rsi_overbought) | (close > upperband)"
                   "short_entry = (rsi > rsi_overbought) & (close > upperband)"
                   "short_exit = (rsi < rsi_oversold) | (close < lowerband)"

                   "# IMPORTANTE: Retornar os sinais na ordem definida em output_names"
                   "long_entry, long_exit, short_entry, short_exit",

        examples=[
            """
            @settings(dict(
                factory_kwargs=dict(
                    class_name='Strategy',
                    input_names=['close'],
                    param_names=['rsi_timeperiod', 'rsi_oversold', 'rsi_overbought', 
                                'bbands_timeperiod', 'bbands_nbdevup', 'bbands_nbdevdn'],
                    output_names=['long_entry', 'long_exit', 'short_entry', 'short_exit']
                ),
                rsi_timeperiod = np.arange(7, 30, 7),
                rsi_oversold = np.arange(20, 36, 5),
                rsi_overbought = np.arange(65, 81, 5),
                bbands_timeperiod = np.arange(10, 26, 5),
                bbands_nbdevup = np.arange(1.5, 3.1, 0.5),
                bbands_nbdevdn = np.arange(1.5, 3.1, 0.5)
            ))
            

            # Calcular RSI usando talib
            rsi = @talib_RSI(close, timeperiod=rsi_timeperiod)

            # Calcular Bandas de Bollinger usando talib
            bb = @talib_BBANDS(
                close, 
                timeperiod=bbands_timeperiod,
                nbdevup=bbands_nbdevup,
                nbdevdn=bbands_nbdevdn
            )
            upperband = bb[0]
            middleband = bb[1]
            lowerband = bb[2]

            # Gerar sinais
            long_entry = (rsi < rsi_oversold) & (close < lowerband)
            long_exit = (rsi > rsi_overbought) | (close > upperband)
            short_entry = (rsi > rsi_overbought) & (close > upperband)
            short_exit = (rsi < rsi_oversold) | (close < lowerband)

            long_entry, long_exit, short_entry, short_exit
            """
        ]
    )

class TALibExpression(BaseTool):
    model_config = {
        "arbitrary_types_allowed": True
    }
    name: str = "TALibExpression"
    description: str = (
        "Executa expressões, em formato de string regular (não é um código python), no VectorBT para análise técnica usando indicadores TA-Lib. "
        "As expressões são uma maneira totalmente nova de definir indicadores de qualquer complexidade usando strings regulares. "
        "A principal vantagem das expressões sobre as funções personalizadas e de aplicação é que o vectorbt pode facilmente examinar o código de um indicador e injetar muitas automações úteis. "
        "As expressões são convertidas em indicadores completos por um método híbrido IndicatorFactory.from_expr. "
        "Por que híbrido? É uma classe e um método de instância. "
        "Podemos chamar esse método em uma instância caso queiramos ter controle total sobre a especificação do indicador, e em uma classe caso queiramos que toda a especificação seja analisada para nós."
    )
    args_schema: Type[BaseModel] = TALibExpressionSchema
    data_dict: Optional[Dict[str, pd.Series]] = None
    
    def __init__(
        self, 
        market_data: Optional[Union[Dict[str, pd.Series], vbt.Data]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        if market_data is not None:
            self.add(market_data)
            #self.description = (
            #    f"Dados OHLCV carregados, no formato de objeto vbt.Data. Executa expressões, em formato de string, no VectorBT para criação de estratégias de trading."
            #)
            #self.args_schema = TALibExpressionSchema

    def add(
        self,
        market_data: Union[Dict[str, pd.Series], vbt.Data],
        **kwargs: Any,
    ) -> None:
        """
        Adiciona dados de mercado à ferramenta.
        
        Args:
            market_data: Dados OHLCV no formato Dict[str, pd.Series] ou vbt.Data
        """
        if isinstance(market_data, vbt.Data):
            self.data_dict = {
                'open': market_data.open,
                'high': market_data.high,
                'low': market_data.low,
                'close': market_data.close,
                'volume': market_data.volume
            }
        else:
            self.data_dict = market_data

    def _before_run(
        self,
        expression: str,
        **kwargs: Any,
    ) -> Any:
        """
        Pré-processamento antes de executar a expressão.
        Carrega os dados se fornecidos nos kwargs.
        """
        if "market_data" in kwargs:
            self.add(kwargs["market_data"])

    def _run(
    self,
    expression: str,
    #parameters: Dict[str, Any] = {},
    #settings: Dict[str, Any] = {},
    market_data: Optional[Union[Dict[str, pd.Series], vbt.Data]] = None,
    ) -> Dict[str, Any]:
        """
        Executa uma expressão VectorBT para gerar sinais.

        Args:
            expression: Expressão VectorBT com indicadores
            parameters: Dicionário com parâmetros para otimização
            settings: Configurações do VectorBT
            market_data: Dados OHLCV (opcional, usa os dados já carregados se None)

        Returns:
            Dict[str, Any]: Resultado do processamento contendo os sinais gerados
        """
        try:
            # Usa os dados fornecidos ou os já carregados
            data = self.data_dict if market_data is None else market_data
            if data is None:
                raise ValueError("Nenhum dado de mercado fornecido")
            
            # Cria o indicador customizado
            CustomIndicator = vbt.IF.from_expr(
                expr=expression,
                #**parameters,
                #**settings
                keep_pd=True,
                use_pd_eval=False
            )
            print(CustomIndicator)
            
            # Executa o indicador
            result = CustomIndicator.run(**data)
            
            # Prepara os sinais
            signals = {
                name: getattr(result, name)
                for name in CustomIndicator.output_names
                if name in ['long_entry', 'long_exit', 'short_entry', 'short_exit']
            }
            
            # Configura e executa o portfólio
            portfolio = vbt.Portfolio.from_signals(
                close=data['close'],
                entries=signals.get('long_entry'),
                exits=signals.get('long_exit'),
                short_entries=signals.get('short_entry'),
                short_exits=signals.get('short_exit'),
                freq=data['close'].index.inferred_freq,
                init_cash=100000,
                fees=0.001,
                slippage=0.001
            )
            
            # Prepara o retorno
            return {
                "success": True,
                "signals": signals,
                "portfolio": {
                    "stats": portfolio.stats().to_dict(),
                    "returns_stats": portfolio.returns_stats().to_dict(),
                    "trades": portfolio.trades.records_readable
                },
                "metadata": {
                    "input_names": CustomIndicator.input_names,
                    "param_names": CustomIndicator.param_names,
                    "output_names": CustomIndicator.output_names,
                    "expression": expression
                }
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao executar a expressão e simular o portfólio"
            }


if __name__ == "__main__":
    from tools.fetch_binance_data import FetchBinanceDataTool
    
    # Exemplo de uso
    data_tool = FetchBinanceDataTool()
    market_data = data_tool._run(
        symbols=["BTCUSDT", "ETHUSDT", "BNBUSDT"],
        start="1 month ago",
        timeframe="1h"
    )
    
    # Criando a ferramenta com dados pré-carregados
    expr_tool = TALibExpression(market_data=market_data)

    # Definir a expressão de trading
    trading_signals_expr = """
        @settings(dict(
            factory_kwargs=dict(
                class_name='Strategy',
                input_names=['close'],
                param_names=['rsi_timeperiod', 'rsi_oversold', 'rsi_overbought', 
                            'bbands_timeperiod', 'bbands_nbdevup', 'bbands_nbdevdn'],
                output_names=['long_entry', 'long_exit', 'short_entry', 'short_exit']
            ),
            rsi_timeperiod = np.arange(7, 30, 7),
            rsi_oversold = np.arange(20, 36, 5),
            rsi_overbought = np.arange(65, 81, 5),
            bbands_timeperiod = np.arange(10, 26, 5),
            bbands_nbdevup = np.arange(1.5, 3.1, 0.5),
            bbands_nbdevdn = np.arange(1.5, 3.1, 0.5)
        ))
        

        # Calcular RSI usando talib
        rsi = @talib_RSI(close, timeperiod=rsi_timeperiod)

        # Calcular Bandas de Bollinger usando talib
        bb = @talib_BBANDS(
            close, 
            timeperiod=bbands_timeperiod,
            nbdevup=bbands_nbdevup,
            nbdevdn=bbands_nbdevdn
        )
        upperband = bb[0]
        middleband = bb[1]
        lowerband = bb[2]

        # Gerar sinais
        long_entry = (rsi < rsi_oversold) & (close < lowerband)
        long_exit = (rsi > rsi_overbought) | (close > upperband)
        short_entry = (rsi > rsi_overbought) & (close > upperband)
        short_exit = (rsi < rsi_oversold) | (close < lowerband)

        long_entry, long_exit, short_entry, short_exit
        """

    result = expr_tool._run(
        expression=trading_signals_expr)
    
    # Imprimir resultados
    if result["success"]:
        stats = result["portfolio"]["stats"]
        print(f"Resultados do Backtest:\n")
        print(f"Start Value: {stats['Start Value']}")
        print(f"End Value: {stats['End Value']}")
        print(f"Total Return [%]: {stats['Total Return [%]']:.2f}%")
        print(f"Win Rate [%]: {stats['Win Rate [%]']:.2f}%")
        print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
        print(f"Max Drawdown [%]: {stats['Max Drawdown [%]']:.2f}%")
        print(f"Profit Factor: {stats['Profit Factor']:.2f}")
        
        # Informações sobre trades
        print("\nInformações de Trades:")
        print(f"Total Trades: {stats['Total Trades']}")
        print(f"Avg Winning Trade [%]: {stats['Avg Winning Trade [%]']:.2f}%")
        print(f"Avg Losing Trade [%]: {stats['Avg Losing Trade [%]']:.2f}%")

        print(result)