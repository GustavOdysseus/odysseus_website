from typing import Type, Dict, Any, List, Optional, Union
import vectorbtpro as vbt
import pandas as pd
import numpy as np
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, model_validator
import os
from datetime import datetime
import json

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
        "Leia com cuidado a descrição do input que a ferramenta espera, para construir a expressão corretamente."
        "A expressão deve sempre retornar os sinais de long_entry, long_exit, short_entry, short_exit na última linha."
        "A ferramenta irá retornar o desempenho no backtesting da estratégia conforme a expressão fornecida."
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
            
            # Executa o indicador
            result = CustomIndicator.run(**data)
            # Obtém o nome da estratégia (pode ser customizado conforme necessário)
            strategy_name = result.__class__.__name__
            
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
                init_cash=100000,
                fees=0.001,
                slippage=0.001,
                save_returns=True,
                size=10,
                size_type="valuepercent100",
                group_by=True,  
                cash_sharing=True,
                call_seq="auto"
            )

            def save_plot(fig, filename, strategy_name, base_dir="Estrategias"):
                strategy_dir = os.path.join(base_dir, strategy_name, "plots")
                os.makedirs(strategy_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                full_path = os.path.join(strategy_dir, f"{filename}_{timestamp}.html")
                
                # Salva o gráfico em HTML
                fig.write_html(full_path)
                return full_path

            # Lista para armazenar os caminhos dos plots
            plots_info = []

            # Salvando os gráficos
            plots = {
                "cumulative_returns": portfolio.plot_cumulative_returns(),
                "allocations": portfolio.plot_allocations(),
                "cash_flow": portfolio.plot_cash_flow(),
                "cash": portfolio.plot_cash(),
                "asset_value": portfolio.plot_asset_value(),
                "value": portfolio.plot_value(),
                "drawdowns": portfolio.plot_drawdowns(),
                "underwater": portfolio.plot_underwater(),
                "gross_exposure": portfolio.plot_gross_exposure()
            }

            # Salva cada plot
            for name, plot in plots.items():
                plots_info.append(save_plot(plot, name, strategy_name))

            def save_results(results, strategy_name, base_dir="Estrategias"):
                strategy_dir = os.path.join(base_dir, strategy_name)
                data_dir = os.path.join(strategy_dir, "data")
                os.makedirs(data_dir, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Função auxiliar para salvar DataFrames
                def save_dataframe(df, name):
                    file_path = os.path.join(data_dir, f"{name}_{timestamp}.csv")
                    df.to_csv(file_path, index=True)
                
                # Salva os DataFrames em CSV
                stats_df = pd.DataFrame([results['portfolio']['stats']])
                save_dataframe(stats_df, "stats")
                
                returns_stats_df = pd.DataFrame([results['portfolio']['returns_stats']])
                save_dataframe(returns_stats_df, "returns_stats")
                
                trades_df = pd.DataFrame(results['portfolio']['trades'])
                save_dataframe(trades_df, "trades")
                
                # Salva os sinais em CSV
                for k, v in results['signals'].items():
                    if isinstance(v, pd.DataFrame):
                        save_dataframe(v, f"signal_{k}")
                
                # Prepara dados não-DataFrame para JSON
                json_results = {
                    "success": results["success"],
                    "metadata": results["metadata"],
                    "portfolio": {
                        "plots": results["portfolio"]["plots"]
                    }
                }
                
                # Salva o JSON
                json_path = os.path.join(strategy_dir, f"results_{timestamp}.json")
                with open(json_path, 'w', encoding='utf-8') as f:
                    json_str = json.dumps(json_results, indent=4, ensure_ascii=False)
                    f.write(json_str)
            
            results = {
                "success": True,
                "signals": signals,
                "portfolio": {
                    "stats": portfolio.stats(),
                    "returns_stats": portfolio.returns_stats(),
                    "trades": portfolio.trades.records_readable,
                    "plots": plots_info
                },
                "metadata": {
                    "input_names": CustomIndicator.input_names,
                    "param_names": CustomIndicator.param_names,
                    "output_names": CustomIndicator.output_names,
                    "expression": expression,
                    "strategy_name": strategy_name
                }
            }

            # Salva os resultados
            save_results(results, strategy_name)

            return results
                
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
        print("result['portfolio']")
        print(result['portfolio'])





        '''
        strategy_config = {
        'class_name': 'EstrategiaRsiEmaSimples',
        'input_names': "['close', 'high', 'low']",
        'param_names': """[
            'rsi_curto_periodo', 'ema_medio_periodo',
            'rsi_curto_limite_baixo', 'rsi_curto_limite_alto',
            'ema_medio_limite_baixo', 'ema_medio_limite_alto',
            'sl_mult', 'atr_timeperiod', 'tp_mult', 'tsl_mult', 
            'volatilidade_ajuste', 'alavancagem_base', 'alavancagem_max',
            'position_size', 'risco_por_trade'
        ]""",
        'output_names': """[
            'long_entries', 'long_exits', 'short_entries', 'short_exits',
            'sl_stop', 'tp_stop', 'tsl_stop', 'leverage', 'size'
        ]""",
        'params': """
        rsi_curto_periodo = np.arange(7, 36, 7),          
        ema_medio_periodo = np.arange(30, 91, 15),        
        rsi_curto_limite_baixo = np.arange(20, 41, 5),    
        rsi_curto_limite_alto = np.arange(65, 86, 5),     
        ema_medio_limite_baixo = np.arange(30, 51, 5),    
        ema_medio_limite_alto = np.arange(55, 76, 5),
        sl_mult = np.arange(0.01, 0.06, 0.01),
        atr_timeperiod = np.arange(7, 36, 7),
        tp_mult = np.arange(0.01, 0.06, 0.01),
        tsl_mult = np.arange(0.01, 0.06, 0.01),
        volatilidade_ajuste = np.arange(1, 6, 1),
        alavancagem_base = np.arange(5, 10, 1),
        alavancagem_max = np.arange(21, 26, 1),
        position_size = np.arange(0.01, 0.06, 0.01),
        risco_por_trade = np.arange(0.01, 0.06, 0.01)""",
        'indicators': """
        temp_rsi_curto = @talib_RSI(@in_close, timeperiod=@p_rsi_curto_periodo)
        temp_ema_medio = @talib_EMA(@in_close, timeperiod=@p_ema_medio_periodo)
        temp_volatilidade = @talib_ATR(@in_high, @in_low, @in_close, timeperiod=@p_atr_timeperiod)""",
        'relaxamento': """
        relaxar_parametros_maiores = 1
        relaxar_parametros_menores = 1""",
        'signals': """
        @out_long_entries = (temp_rsi_curto < (@p_rsi_curto_limite_baixo * relaxar_parametros_menores)) & (@in_close > (temp_ema_medio * relaxar_parametros_maiores))
        @out_long_exits = (temp_rsi_curto > (@p_rsi_curto_limite_alto)) | (@in_close < (temp_ema_medio))
        @out_short_entries = (temp_rsi_curto > (@p_rsi_curto_limite_alto * relaxar_parametros_maiores)) & (@in_close < (temp_ema_medio * relaxar_parametros_menores))
        @out_short_exits = (temp_rsi_curto < (@p_rsi_curto_limite_baixo)) | (@in_close > (temp_ema_medio))""",
        'risk_levels': """
        @out_sl_stop = (@p_sl_mult * temp_volatilidade) / @in_close
        @out_tp_stop = @p_tp_mult * temp_volatilidade / @in_close
        @out_tsl_stop = @p_tsl_mult * temp_volatilidade / @in_close""",
        'leverage': """
        temp_ajuste_volatilidade = np.clip(1 / (temp_volatilidade / np.mean(temp_volatilidade)) * @p_volatilidade_ajuste, 1, @p_alavancagem_max)
        temp_confirmacao_tendencia = (temp_rsi_curto < @p_rsi_curto_limite_baixo) | (temp_rsi_curto > @p_rsi_curto_limite_alto) & (@in_close > temp_ema_medio)
        @out_leverage = np.where(temp_confirmacao_tendencia, np.minimum(@p_alavancagem_base * temp_ajuste_volatilidade, @p_alavancagem_max), 1)""",
        'position_sizing': """
        @out_size = np.minimum(@p_position_size, (@p_risco_por_trade / (@out_sl_stop * @in_close)) * @out_leverage)""",
        'outputs': """
        @out_long_entries, @out_long_exits, @out_short_entries, @out_short_exits, @out_sl_stop, @out_tp_stop, @out_tsl_stop, @out_leverage, @out_size"""
    }
    '''