'''
Explicação da Estratégia de Trading

A estratégia de trading aqui descrita busca identificar oportunidades de compra e venda no mercado financeiro, utilizando a análise de candles (barras que representam variações de preços em um determinado período) e aplicando um rigoroso gerenciamento de risco. Ela faz uso de dois timeframes diferentes: um timeframe maior (como 1 hora) para identificar sinais de reversão de tendência e um timeframe menor (como 1 minuto) para executar as operações.
1. Identificação de Sinais de Compra e Venda

A estratégia começa analisando dois candles consecutivos no timeframe maior (ex.: candles de 1 hora). Ela avalia a relação entre o preço de abertura e fechamento de cada candle para determinar se há uma possível reversão de tendência, gerando um sinal de compra (alta) ou venda (baixa):

    Sinal de Compra (alta): É gerado quando o primeiro candle (candle_1) apresenta um fechamento mais baixo que sua abertura (indicando queda), mas o segundo candle (candle_2) fecha acima da abertura do primeiro candle. Isso sugere que o mercado pode estar revertendo de uma tendência de queda para uma de alta.

    Sinal de Venda (baixa): É gerado quando o primeiro candle (candle_1) fecha acima de sua abertura (indicando alta), mas o segundo candle (candle_2) fecha abaixo da abertura do primeiro. Isso indica uma possível reversão de uma tendência de alta para uma de baixa.

Se nenhum desses critérios for atendido, a estratégia não gera sinal e continua aguardando o próximo conjunto de candles.
2. Execução das Operações com Candles de 1 Minuto

Quando a estratégia identifica um sinal de compra ou venda, ela passa a monitorar candles de 1 minuto dentro do intervalo do candle atual de maior timeframe (por exemplo, os candles de 1 minuto durante o candle de 1 hora). Nesse momento, a estratégia busca uma confirmação para abrir uma operação de compra ou venda.
Para Sinais de Compra:

    A estratégia acompanha o movimento dos preços no gráfico de 1 minuto, esperando que o preço retraia, ou seja, caia temporariamente abaixo do ponto médio do candle atual.
    Quando o preço atinge essa retração, a estratégia registra os valores mínimos alcançados e busca um sinal de recuperação. Se o preço, depois de atingir o ponto mínimo, começar a subir e superar o preço de fechamento do candle anterior, a estratégia abre uma posição de compra.
    Neste momento, são definidos automaticamente dois níveis importantes:
        Stop Loss (SL): O ponto mais baixo da retração serve como o limite de perda máxima aceitável. Se o preço cair até esse ponto, a operação será encerrada com uma perda controlada.
        Take Profit (TP): O objetivo de lucro é definido de forma simétrica ao SL, ou seja, a distância entre o preço de entrada e o Stop Loss é replicada para cima. Se o preço atingir o TP, a operação é encerrada com lucro.

Para Sinais de Venda:

    De forma semelhante à operação de compra, a estratégia monitora os preços de 1 minuto para detectar uma retração, mas neste caso, uma alta temporária acima do ponto médio do candle atual.
    A estratégia registra os valores máximos durante essa alta e espera uma reversão para o lado da venda. Se o preço cair abaixo do fechamento do candle anterior, a operação de venda é ativada.
    Assim como na operação de compra, são definidos automaticamente o Stop Loss, que é o valor máximo da retração, e o Take Profit, que é calculado simetricamente para baixo. A operação de venda é encerrada se o preço atingir o SL ou o TP.

3. Condições de Interrupção

Nem todas as análises resultam em operações. Se o preço durante a análise dos candles de 1 minuto se mover contra a expectativa (ou seja, se o preço mínimo de um candle de 1 minuto for menor que o preço mínimo do candle anterior em uma operação de compra, ou se o preço máximo for maior no caso de uma operação de venda), a análise é interrompida sem que a operação seja aberta. Isso evita entrar em operações quando o mercado mostra fraqueza ou força contrária à direção esperada.
4. Gerenciamento de Risco

O gerenciamento de risco é uma parte fundamental dessa estratégia. Cada operação é limitada por um Stop Loss, que garante que as perdas potenciais sejam controladas. Ao mesmo tempo, o Take Profit define o nível em que os lucros são realizados automaticamente. A relação entre SL e TP é simétrica, o que significa que o potencial de lucro é igual ao risco assumido em cada operação.

Além disso, o tamanho de cada operação é proporcional ao saldo disponível, e o nível de risco é ajustado conforme o saldo aumenta ou diminui. Isso ajuda a proteger o capital e garantir que não sejam feitas operações com risco excessivo em relação ao saldo da conta.

Se o saldo da conta cair a zero durante uma operação, a estratégia interrompe o backtesting (simulação) imediatamente, evitando continuar operações que possam gerar mais perdas do que o saldo disponível.
'''

import numpy as np
from numba import njit, int64  # Adicione esta importação no topo do arquivo
import vectorbtpro as vbt
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os
import time
from vectorbtpro.utils.template import Rep
import typing as tp

@njit
def detect_reversal_pattern_nb(open: np.ndarray, close: np.ndarray, high: np.ndarray, low: np.ndarray) -> tuple:
    """
    Detecta padrões de reversão no timeframe maior.
    
    Args:
        open (np.ndarray): Preços de abertura
        close (np.ndarray): Preços de fechamento
        high (np.ndarray): Preços máximos
        low (np.ndarray): Preços mínimos
        
    Returns:
        tuple: (sinais_compra, sinais_venda, ponto_medio, preco_falha)
    """
    n = len(open)
    bullish_signals = np.full(n, False)
    bearish_signals = np.full(n, False)
    midpoints = np.full(n, np.nan)
    fail_prices = np.full(n, np.nan)
    prev_closes = np.full(n, np.nan)
    # Precisamos de pelo menos 2 candles
    for i in range(2, n):
        # Sinal de Compra: candle1 bearish + candle2 fecha acima da abertura do candle1
        if close[i-2] < open[i-2] and close[i-1] > open[i-1]:
            bullish_signals[i] = True
            midpoints[i] = (high[i-1] + low[i-1]) / 2
            fail_prices[i] = low[i-1]
            prev_closes[i] = close[i-1]
            
        # Sinal de Venda: candle1 bullish + candle2 fecha abaixo da abertura do candle1
        if close[i-2] > open[i-2] and close[i-1] < open[i-1]:
            bearish_signals[i] = True
            midpoints[i] = (high[i-1] + low[i-1]) / 2
            fail_prices[i] = high[i-1]
            prev_closes[i] = close[i-1]
    return bullish_signals, bearish_signals, midpoints, fail_prices, prev_closes

@njit
def confirm_entry_nb(open: np.ndarray, high: np.ndarray, low: np.ndarray, close: np.ndarray, 
                    prev_close: np.float64, fail_price: np.float64, midpoint: np.float64,  # Mudar para float64
                    bullish_signal: bool, bearish_signal: bool) -> tuple:
    """
    Confirma entrada após retração no timeframe menor (1min) e após atingir o preço de fechamento do candle anterior de timeframe maior, comparando com as informações do candle anterior de timeframe maior.
    
    Args:
        open (np.ndarray): Preços de abertura
        high (np.ndarray): Preços máximos
        low (np.ndarray): Preços mínimos
        close (np.ndarray): Preços de fechamento
        prev_close (np.float64): Preço de fechamento do candle anterior de timeframe maior
        fail_price (np.float64): Preço de falha. Caso o padrão de reversão seja de compra, o preço de falha será o preço mínimo do candle anterior (x-1) de timeframe maior. Caso o padrão de reversão seja de venda, o preço de falha será o preço máximo do candle anterior (x-1) de timeframe maior.
        midpoint (np.float64): Ponto médio do candle anterior de timeframe maior
        bullish_signal (bool): Sinail de alta
        bearish_signal (bool): Sinail de baixa
        
    Returns:
        tuple: (entradas_confirmadas, stop_loss, take_profit)
    """
    n = len(close)
    entries = np.full(n, False)
    sl_prices = np.full(n, np.nan, dtype=np.float64)  # Especificar dtype
    tp_prices = np.full(n, np.nan, dtype=np.float64)  # Especificar dtype
    stop_price_buy = np.float64(np.inf)   # Converter para float64
    stop_price_sell = np.float64(-np.inf)  # Converter para float64
    
    
    for i in range(1, n):
        if bullish_signal:
            if low[i] <= fail_price:
                break
            
            if low[i] <= midpoint and low[i] < stop_price_buy:
                stop_price_buy = low[i]

            # Para sinais de compra
            if high[i] >= prev_close:
                entries[i] = True
                sl_prices[i] = stop_price_buy  # Stop Loss no mínimo da retração
                tp_prices[i] = close[i] + (close[i] - stop_price_buy)  # Take Profit simétrico
        
        elif bearish_signal:
            if high[i] >= fail_price:
                break

            if high[i] >= midpoint and high[i] > stop_price_sell:
                stop_price_sell = high[i]

            # Para sinais de venda
            if high[i] > midpoint and low[i] <= prev_close:
                entries[i] = True
                sl_prices[i] = stop_price_sell  # Stop Loss no máximo da retração
                tp_prices[i] = close[i] - (stop_price_sell - close[i])  # Take Profit simétrico
            
    return entries, sl_prices, tp_prices

@njit
def validate_continuation_nb(low: np.ndarray, high: np.ndarray, direction: int) -> bool:
    """
    Valida se o movimento continua na direção esperada.
    
    Args:
        low (np.ndarray): Preços mínimos
        high (np.ndarray): Preços máximos
        direction (int): 1 para compra, -1 para venda
        
    Returns:
        bool: True se movimento continua válido
    """
    n = len(low)
    for i in range(1, n):
        if direction == 1:  # Compra
            if low[i] < low[i-1]:
                return False
        else:  # Venda
            if high[i] > high[i-1]:
                return False
    return True

@njit
def get_param_value(param_tuple: tp.Tuple[int, ...], index: int) -> np.int64:
    """Função auxiliar para extrair valor do parâmetro como np.int64"""
    return np.int64(60) if index == 0 else np.int64(1)

@njit
def custom_gotas_nb(input_tuple: tp.Tuple[np.ndarray, ...], 
                    in_output_tuple: tp.Tuple[np.ndarray, ...],
                    param_tuple: tp.Tuple[int, ...],
                    *args) -> tp.Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Função principal da estratégia Gotas.
    """
    # Extrair dados e parâmetros
    data = input_tuple[0]
    # Extrair valores individuais dos parâmetros
    tf_maior = np.int64(param_tuple[0])  # Converter para np.int64
    tf_menor = np.int64(param_tuple[1])  # Converter para np.int64
    
    n_samples = data.shape[0]
    n_params = 1  # Definir como 1 já que estamos usando valores únicos
    
    # Arrays de saída
    entries = np.full((n_samples, n_params), False)
    exits = np.full((n_samples, n_params), False)
    sl_prices = np.full((n_samples, n_params), np.nan, dtype=np.float64)
    tp_prices = np.full((n_samples, n_params), np.nan, dtype=np.float64)
    
    # Dados do timeframe menor (1min)
    open_1m = data[:, 0]
    high_1m = data[:, 1]
    low_1m = data[:, 2]
    close_1m = data[:, 3]
    
    # Dados do timeframe maior
    open_tf = data[:, 4]
    high_tf = data[:, 5]
    low_tf = data[:, 6]
    close_tf = data[:, 7]
    
    # Detectar padrões no timeframe maior
    bullish, bearish, midpoints, fail_prices, prev_closes = detect_reversal_pattern_nb(
        open_tf, high_tf, low_tf, close_tf
    )
    
    # Para cada sinal no timeframe maior
    i = np.int64(0)  # Inicializar como np.int64
    while i < n_samples:
        j = i // tf_maior  # Agora tf_maior é um np.int64
        
        if j < len(bullish) and (bullish[j] or bearish[j]):
            tf_end = min(i + tf_maior, n_samples)
            
            # Confirmar entrada no timeframe menor
            entries_tf, sl_tf, tp_tf = confirm_entry_nb(
                open_1m[i:tf_end],
                high_1m[i:tf_end],
                low_1m[i:tf_end],
                close_1m[i:tf_end],
                prev_closes[j],
                fail_prices[j],
                midpoints[j],
                bullish[j],
                bearish[j]
            )
            
            # Atualizar arrays de saída
            entries[i:tf_end, 0] = entries_tf  # Usar índice 0 para a única coluna
            sl_prices[i:tf_end, 0] = sl_tf     # Usar índice 0 para a única coluna
            tp_prices[i:tf_end, 0] = tp_tf     # Usar índice 0 para a única coluna
            
            # Se houver entrada, definir saída no próximo timeframe maior
            if np.any(entries_tf):
                next_tf_start = tf_end
                next_tf_end = min(next_tf_start + tf_maior, n_samples)
                exits[next_tf_start:next_tf_end, 0] = True  # Usar índice 0 para a única coluna
        
        i += tf_maior
    
    return entries, exits, sl_prices, tp_prices


# Criar o Indicator Factory
GotasStrategy = vbt.IF(
    class_name='GotasStrategy',
    short_name='gotas',
    input_names=['data'],
    param_names=['timeframe_maior', 'timeframe_menor'],
    output_names=['entries', 'exits', 'sl_prices', 'tp_prices']
).with_custom_func(
    custom_gotas_nb,
    require_input_shape=True,
    pass_packed=True,
    param_settings=dict(
        timeframe_maior=dict(dtype=np.int64),
        timeframe_menor=dict(dtype=np.int64)
    )
)

def prepare_data(symbol: str, start_date: str = None, end_date: str = None, 
                base_path: str = r'D:\Caleb\caleb\Python\mercado\mercado\reinaldo\FOREX\simbolos') -> pd.DataFrame:
    """
    Prepara os dados do CSV para o backtesting.
    
    Args:
        symbol (str): Símbolo do par (ex: 'EURUSD')
        start_date (str, optional): Data inicial (formato: 'YYYY-MM-DD')
        end_date (str, optional): Data final (formato: 'YYYY-MM-DD')
        base_path (str): Caminho base para os arquivos CSV
        
    Returns:
        pd.DataFrame: DataFrame com OHLCV em frequência de 1 minuto
    """
    symbol = symbol.lower()
    csv_path = os.path.join(base_path, f"{symbol}_1m.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")
    
    # Carregar dados do CSV
    data = pd.read_csv(csv_path)
    data['datetime'] = pd.to_datetime(data['datetime'])
    data.set_index('datetime', inplace=True)
    
    # Filtrar período se especificado
    if start_date:
        data = data[data.index >= start_date]
    if end_date:
        data = data[data.index <= end_date]
    
    # Remover duplicatas e NaN
    data = data.drop_duplicates()
    data = data.dropna()
    
    return data

def resample_data(data: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """
    Faz o resample dos dados para o timeframe especificado usando o OHLCV accessor do VectorBT.
    
    Args:
        data (pd.DataFrame): DataFrame com dados OHLCV
        timeframe (str): Timeframe desejado (ex: '1min', '60min', '1H')
        
    Returns:
        pd.DataFrame: DataFrame com dados resampleados
    """
    # Usar o accessor OHLCV do VectorBT que já implementa as regras corretas de agregação
    resampled = data.vbt.ohlcv.resample(timeframe)
    return resampled

def run_backtest(data: pd.DataFrame, timeframe_maior: int, timeframe_menor: int = 1, 
                initial_capital: float = 100000.0, risk_per_trade: float = 0.01) -> vbt.Portfolio:
    """
    Executa o backtesting da estratégia.
    """
    # Validações
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data deve ser um pandas DataFrame")
    if not all(col in data.columns for col in ['open', 'high', 'low', 'close']):
        raise ValueError("data deve conter colunas 'open', 'high', 'low', 'close'")
    if timeframe_maior <= 0:
        raise ValueError("timeframe_maior deve ser maior que zero")
    if timeframe_menor <= 0:
        raise ValueError("timeframe_menor deve ser maior que zero")
    if initial_capital <= 0:
        raise ValueError("initial_capital deve ser maior que zero")
    if risk_per_trade <= 0 or risk_per_trade > 1:
        raise ValueError("risk_per_trade deve estar entre 0 e 1")

    # Converter timeframes para np.int64
    tf_maior = np.int64(timeframe_maior)
    tf_menor = np.int64(timeframe_menor)

    # Fazer resample dos dados para timeframe maior
    data_tf_maior = data.vbt.ohlcv.resample(f'{timeframe_maior}min').obj
    
    # Reindexar os dados do timeframe maior para o mesmo índice dos dados originais
    data_tf_maior = data_tf_maior.reindex(data.index, method='ffill')
    
    # Preparar array de entrada
    input_data = np.column_stack((
        data['open'].values,
        data['high'].values,
        data['low'].values,
        data['close'].values,
        data_tf_maior['open'].values,
        data_tf_maior['high'].values,
        data_tf_maior['low'].values,
        data_tf_maior['close'].values
    ))
    
    # Executar a estratégia
    gotas = GotasStrategy.run(
        data=input_data,
        input_shape=(len(data), 8),
        timeframe_maior=np.int64(60),  # Definir valor padrão aqui
        timeframe_menor=np.int64(1)    # Definir valor padrão aqui
    )
    
    # Calcular size baseado no risco por operação
    size = pd.Series(np.nan, index=data.index)
    size[gotas.entries] = initial_capital * risk_per_trade / (
        data['close'] - gotas.sl_prices
    )
    
    # Criar portfolio
    pf = vbt.Portfolio.from_signals(
        close=data['close'],
        entries=gotas.entries,
        exits=gotas.exits,
        sl_stop=gotas.sl_prices,
        tp_stop=gotas.tp_prices,
        size=size,
        init_cash=initial_capital,
        freq='1min'
    )
    
    return pf

# Exemplo de uso atualizado
if __name__ == "__main__":
    try:
        # Parâmetros
        SYMBOL = "AUDUSD"
        START_DATE = "2013-01-01"
        END_DATE = "2022-12-31"
        TIMEFRAME_MAIOR = np.int64(60)  # Converter para np.int64
        INITIAL_CAPITAL = 25000.0
        RISK_PER_TRADE = 0.002

        inicio_tempo = time.time()
        
        # Preparar dados
        data = prepare_data(
            symbol=SYMBOL,
            start_date=START_DATE,
            end_date=END_DATE
        )
        
        # Executar backtest
        portfolio = run_backtest(
            data=data,
            timeframe_maior=TIMEFRAME_MAIOR,
            initial_capital=INITIAL_CAPITAL,
            risk_per_trade=RISK_PER_TRADE
        )
        
        # Marca o fim do tempo de execução
        fim_tempo = time.time()

        # Calcula o tempo total de execução
        tempo_total = fim_tempo - inicio_tempo

        # Exibe o tempo total em segundos
        print(f"Tempo total de execução: {tempo_total:.2f} segundos")
        # Imprimir resultados
        print(f"\nResultados do Backtest para {SYMBOL}:")
        print(f"Total Return: {portfolio.total_return:.2%}")
        print(f"Sharpe Ratio: {portfolio.sharpe_ratio:.2f}")
        print(f"Max Drawdown: {portfolio.max_drawdown:.2%}")
        
        # Métricas de trades
        if len(portfolio.trades.records) > 0:
            print(f"Win Rate: {portfolio.trades.win_rate:.2%}")
            print(f"Número de Trades: {len(portfolio.trades.records)}")
            print(f"Profit Factor: {portfolio.trades.profit_factor:.2f}")
            print(f"Expectativa: {portfolio.trades.expectancy:.2f}")
            print(f"SQN: {portfolio.trades.sqn:.2f}")
        else:
            print("\nNenhum trade realizado!")
            
        # Métricas adicionais
        print(f"\nMétricas Adicionais:")
        print(f"Volatilidade Anual: {portfolio.annualized_volatility:.2%}")
        print(f"Retorno Anualizado: {portfolio.annualized_return:.2%}")
        print(f"Calmar Ratio: {portfolio.calmar_ratio:.2f}")
        print(f"Omega Ratio: {portfolio.omega_ratio:.2f}")

    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
        raise
















