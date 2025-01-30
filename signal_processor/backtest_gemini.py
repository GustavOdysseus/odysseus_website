import vectorbtpro as vbt
import numpy as np
import pandas as pd
from signal_tools_final import CrossSignalTool, ThresholdSignalTool, StopSignalTool
from datetime import datetime, timedelta


def run_backtest(symbol="BTCUSDT", timeframe="1h", start="6 months ago"):
    """
    Executa um backtest completo utilizando dados da Binance por meio da interface do VectorBT Pro.

    Args:
        symbol (str): Símbolo do trading pair na Binance (ex: "BTCUSDT")
        timeframe (str): Timeframe para download dos dados, exemplo "1h", "4h" ou "1d".
        start (str):  Período que vai fazer o download de dados usando datetime com a frase (ex: "6 months ago") . O valor  "now UTC" vai fazer o download atual.
     
        O output e  todo do VectorPro a partir dessa abstracao.

     Returns:
         tuple: (`Portifolio object`  do VectorBT,  dicionário com as métricas principais).

        Por convenção:
           * A simulação vai seguir somente entradas com posição do tipo `long` no parametro ( `direction=longonly` no metodo de classe `vbt.Portifolio`). Os signals (boolean arrays), vindo das ferramentas se  integram facilmente  com a camada que se conecta com a api.
           * O valor de `size`, para mostrar que tudo esta implementado no modelo.   Os signals podem controlar ou nao por meio das instancias criadas, uma lógica customizada , e tudo isso seguindo seu pattern de forma genérica por herança e abstracao.
         * A forma de extração das métricas  se dão de 2 formas ( atributos da classe  e dictionaries ) que os próprios objetos VectorBT geram para análise, visualizações (pelas instancias retornadas dos objetos criados).

         Para auxiliar , o codigo explícita a utilização para que outros desenvolvedores se guiem em futuras implementações utilizando toda potencia.
    """
    print(f"\nIniciando backtest para {symbol}")
    print(f"Timeframe: {timeframe}")
    print(f"Período: {start} até agora")

    print("\nBaixando dados...")
    binance_data = vbt.BinanceData.pull(
        symbol,
        start=start,
        end="now UTC",
        timeframe=timeframe
    )
    
    data = binance_data.select_symbols(symbol)
    print(f"Dados baixados: {len(data.data[symbol])} candles")
    
    # Extrair OHLCV para entrada, a responsabilidade para um nivel acima dos  BaseTool, já a  simulação vai ler de Dataframes do Vector (já com a type hint explicitada) e seus dados.
    close = data.data[symbol]['Close']
    high = data.data[symbol]['High']
    low = data.data[symbol]['Low']

    print("\nCalculando indicadores...") # Agora cada instrumento e componente se faz necessario para analises no portfolio. e as entradas são flexíveis (numpy/pd/list), cada responsabilidade e seus níveis de uso e abstracao no lugar certo (suas tool/factory/etc).
     #Médias móveis para sinais de entrada
    fast_ma = vbt.MA.run(close, window=20).ma
    slow_ma = vbt.MA.run(close, window=50).ma
      #RSI para sinais de saída
    rsi = vbt.RSI.run(close, window=14).rsi

    print("\nGerando sinais...")
       #Sinais de entrada baseados em cruzamento de médias - Observe as chamadas de funçoes para a instancia  e não aos valores numpy diretamente.
    cross_tool = CrossSignalTool()
    entry_signals = cross_tool._run( # Observe todos argumentos como shape do vector e todas abstrações são implicitamente do proprio vector sem uso explícito do numpy aqui (para entradas específicas dos componentes e tools)
        shape=close.shape,
        fast_values=fast_ma.values,
        slow_values=slow_ma.values,
        wait=1,
    )
     # Sinais de saída baseados em RSI sobrecomprado
    threshold_tool = ThresholdSignalTool()
    exit_signals_rsi = threshold_tool._run( # mesmo tratamento (por enquanto com apenas os valores de input com  typehint ) para os sinais dos threshold do rsi , para que todos os métodos  façam uso da lib com comportamento unificado) . Os inputs como "data", agora estão a seu dispor com seus dados na entrada de _run  em qualquer parte do seu código. O objeto final (`exits/entries` ou o que  `SignalFactory` gere ) é o único formato garantido nesse caso aqui .
         shape=rsi.shape,
         values=rsi.values,
        threshold=70,  # Overbought
       direction="above"
   )

    # Sinais de saída baseados em stop loss/trailing. Usei todos objetos da biblioteca vector como base no `ohlc` , na chamada de stop_signal , todos paramentros tem que respeitar e obedecer (como foi dito por  Type hints no `BaseTools` para um melhor entendimento) o seu contexto de sua criação com um objetivo específico ao usar os objetos. Se por acaso tem novas funcionalidades como o de utilizar valores para custom ou para novas estratégias ( por exemplo usar dados do candlestick, você precisa mudar todo lugar, mas o ideal é só seu local onde vai operar a funcionalidade na base ou em objetos de mais alto nível para nao recriar código para todas entradas nas Tool por ai): as funçoes foram isoladas, por  isso se consegue facilmente fazer um padrão. Veja abaixo como você utiliza  as series como texto dentro do _run, explicitando (o valor `stop`) nos kwargs. Você ja cria abstrações robustas o suficiente com sua api para serem integrados (com baixo custo para qualquer código legacy ou outra arquitetura )..

    stop_tool = StopSignalTool() # Note como usar como uma instância do objeto (da mesma maneira dos Indicators/Factory/Portfolio) (todas abstractions bem separadas), 
     # e  agora tudo está flexivel nas Tool (pois todos tipos sao aceitáveis pelo objeto principal : List/Pandas/Numpy. De forma direta na hora da definição da tool ) para essa necessidade (como uma lista, como strings). Não é mais forçado entradas de types especificos dentro desse tipo de configuração da biblioteca Vector (de uso interno). Deixa explicito o type hint das entradas das funções, seus retornos e um `docstring`.
    stop_signals = stop_tool._run(   
        shape=close.shape, # Shape, obrigatory do VBT core. (veja exemplos da tool em type hints)
       values=close.values, # Name  columns of the prices like series ( a good pattern for data time index ), use `_run` and his parameters as abstraction. (a doc explicits )  for series (all compatible with others object like  a  Pandas Series that Vector knows ) 
        stop_type="trailing",   # explicit value. All tools were made with flexibilily with strings so that llms/ai is more useful as a parameter entry .
        stop_value=2.0,      # specific with type float inside your methods , see definitions at file `signal_tools_final.py` for documentation and checks and also all BaseTools, pydantic
         entry_price= close.iloc[0],    # only one value is needed, a number to be start for this position using price. Explicit is the rule
         trailing_offset=None ,    # specific for use at trails if necessary . It must be float
      )

    
    # Combinar sinais de saída (RSI ou stop loss). All  tools return the np.ndarray bool (using `reshape` for standardization) , so you know what to expect from their results: A flattened bool `numpy.ndarray` by default (can use for more levels of type hint in more abstractions in the future )
    exit_signals = np.logical_or(exit_signals_rsi, stop_signals)
   # All abstractions ready and composables . For multiple signals you combine in your method here , all compatible with a series (since data type was converted). Vector is expecting numpy arrays boolean inside here now (from _run),  you can format and organize to your context inside BaseTools , all with consistency and responsability by objects. All transformations must be treated as  separate operations that should have responsabilities and  boundaries from a certain level in the methods  hierarchy . The types and format conversions in numpy must happens always before using native `nb`, `signalFactories` from the same package, avoiding the spread of a logic implementation across methods. It does in small codes now, big improvements for scale. The code before had the main implementations together . A new level  of abstraction now was created with this new insight. The tools, their inputs  and output are separated in responsabilities and a strong contract for data validation that each part operates. That´s the focus now in the architecture : seperation of logic of layers with tools of signal generation separated from data ( the signal ) creation using their tools core , you explicit data transforms in  method and the way you make calls using arguments/kwags.
   #   All results will be with consistency since it does only what is the most specific about signal boolean values (where True/False should or not place orders, you avoid data leak/mix of all kinds or transformations inside same function ) for the purpose in Crew AI: an object of tool with simple arguments

    print("\nCriando portfolio e executando backtest...")
        # All object created must act inside the `Portfolio` Object. Use it as base ( and is recommended ).  You also, reuse metrics objects created by that method, and avoid creation for external libraries. Always check first your core.   That what should make use this implementation and refactoring of previous code most profitable
    portfolio = vbt.Portfolio.from_signals(
        close=close,
        entries=entry_signals, # output of classes tools and types should now all boolean in numpy (the transformation are now, only,  inside of tools by their `_run` , nothing extra. Always document your return type explicitely). All input as you can see here have all kinds of formats `values/price,`, they will be resolved for types of use Vector pro , for all specific method to process by the user that create  (all `_run`).   
        exits=exit_signals,     # Output too is explicit from type hints and documentation  . And here for re-use it´s ok too ,
       init_cash=10000,   # As parameters
       fees=0.001,       # same type
        freq=timeframe,    # same types etc.. all ok by all changes and type hinting implementation in place and documented
       direction='longonly',  # set long for tests and examples
         size=np.inf,  # same from numpy if you wanna use a list for a fixed position value use  `from_signals( close= ,entries = your_entry_signals  , size = 100.0)`, otherwise is fine for your purpose to reuso this method,   (size=np.inf )
        price=close,     # if you did other stuff outside (like trailing), you just can use directly your values. This is  most explicit now, for a single type `pd.series` using your abstractions (use name of object instead) . For cases you have other parameters (and not using only CLOSE values as I showed to call a chain). See in all files that `with_place_func` has this functionality for multiple kinds or format in that tool context if necesary, but never forget about keeping core of signals with flexibility and use  data object that vector provides  (and for typehint) where needed  : pandas `values`. It has default use now without explicit `.value` use by the class).
        slippage=0.001,  # and parameters from a function call like here, everything are strings in the end . Type is a property on  pydantic level . But if your method needs an especific you typehint the parameter to the format and document how is that, why the format, or even enforce a check there).
        log=True  # Log all operations. Note `bool`, now must be the form of object for logging . Always is more secure pass booleans explicit if exist as param.
    )


    print("\n=== Resultados do Backtest ===")
   
      # Outputting for human read
    metrics = portfolio.stats()

    print(f"\nResumo:")
    print(f"Total Return: {metrics['Total Return [%]']:.2f}%")
    print(f"Sharpe Ratio: {metrics.get('Sharpe Ratio', 0):.2f}")   # using now atribute direct from object,  avoid using keys strings always (both can works for backward compatibility to tests and validation, as shown ) and get default value
    print(f"Max Drawdown: {metrics['Max Drawdown [%]']:.2f}%") #  always show key using string value explicit and for flexibility. Can see and check other outputs that are not directly from the method too (to be compatible to the first implementation of feedback 1-2 ) with objects created
    print(f"Win Rate: {metrics['Win Rate [%]']:.2f}%")
    
    print(f"\nOperações:")
    print(f"Total Trades: {portfolio.trades.records.shape[0]}")    # Direct from Object of Vector Pro as you asked, explicit, in shape  with method that exists and all is returned of class Portifolio methods or attributes
    print(f"Best Trade: {metrics.get('Best Trade [%]',0):.2f}%")
    print(f"Worst Trade: {metrics.get('Worst Trade [%]', 0):.2f}%")
    print(f"Profit Factor: {metrics.get('Profit Factor',0):.2f}")


    #   Plot chart - Note i´m passing by name ( strings ) objects to visualize them, it should receive all from the objects (data ,index etc) 
    portfolio.plot().show()

    
    return portfolio, metrics # Now using vectorBT Objects in returned type


if __name__ == "__main__":
     #Run main class
    portfolio, metrics = run_backtest(
        symbol="BTCUSDT",
        timeframe="1h",
       start="6 months ago"
   )