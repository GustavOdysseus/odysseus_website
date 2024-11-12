import time
import numpy as np
import pandas as pd
start_load_libraries = time.time()
import vectorbtpro as vbt
import timeit
from numba import njit
timeit.timeit("import vectorbtpro as vbt", number=1)
from vectorbtpro import IndicatorFactory
end_load_libraries = time.time()
print(f"Tempo de carregamento de bibliotecas: {end_load_libraries - start_load_libraries:.2f} segundos")

# Definir o sinal de reversão
@njit
def reversal_pattern_np(open_array, close_array):
    out = np.full_like(close_array, np.nan, dtype=np.float64)
    close_shift_1 = np.roll(close_array, 1)
    open_shift_1 = np.roll(open_array, 1)
    close_shift_2 = np.roll(close_array, 2)
    open_shift_2 = np.roll(open_array, 2)

    long_cond = (close_shift_2 < open_shift_2) & (close_shift_1 > open_shift_1)
    short_cond = (close_shift_2 > open_shift_2) & (close_shift_1 < open_shift_1)

    # Usando um loop para atribuir os valores
    for i in range(len(out)):
        if long_cond[i]:
            out[i] = 1  # Sinal de reversão de alta
        elif short_cond[i]:
            out[i] = -1  # Sinal de reversão de baixa
            
    return out

ReversalSignal = vbt.IndicatorFactory(
    class_name="ReversalPatternSignal",
    input_names=['open', 'close'],
    output_names=['signal']
).with_apply_func(reversal_pattern_np)

# Função de recuo otimizada para implementar as condições hierárquicas com base no timeframe de 6 horas
@njit
def pullback_custom_func(midpoint, tf_high, tf_low, tf_close, reversal_signal, low_1m, high_1m, close_1m):
    # Verifica se há sinal de reversão
    if np.isnan(reversal_signal):
        return np.nan, np.nan, np.nan, np.nan

    if reversal_signal == 1:
        # Passo 1: Verifica a primeira condição (mínima <= midpoint)
        first_condition = low_1m <= midpoint
        if not first_condition.any():
            return np.nan, np.nan, np.nan, np.nan

        # Índice do primeiro valor que satisfaz a primeira condição
        first_index = first_condition.argmax()

        # Passo 2: Verifica a segunda condição (máxima >= fechamento do candle anterior de 6 horas)
        second_condition = high_1m[first_index:] >= tf_close
        if not second_condition.any():
            return np.nan, np.nan, np.nan, np.nan

        # Índice do primeiro valor que satisfaz a segunda condição
        second_index = first_index + second_condition.argmax()

        # Determina o preço de entrada, stop e take profit
        entry_price = close_1m[second_index]
        if second_index == 0:
            stop_price = low_1m[0]
        else:
            stop_price = low_1m[:second_index].min()
        take_profit_price = entry_price + (entry_price - stop_price)

        # Passo 3: Verifica a terceira condição (mínima <= mínimo do candle de 6 horas anterior)
        third_condition = low_1m[:second_index] <= tf_low
        if third_condition.any():
            return np.nan, np.nan, np.nan, np.nan

    elif reversal_signal == -1:
        # Passo 1: Verifica a primeira condição (máxima >= midpoint)
        first_condition = high_1m >= midpoint
        if not first_condition.any():
            return np.nan, np.nan, np.nan, np.nan
        
        # Índice do primeiro valor que satisfaz a primeira condição
        first_index = first_condition.argmax()

        # Passo 2: Verifica a segunda condição (mínima <= fechamento do candle anterior de 6 horas)
        second_condition = low_1m[first_index:] <= tf_close
        if not second_condition.any():
            return np.nan, np.nan, np.nan, np.nan
        
        # Índice do primeiro valor que satisfaz a segunda condição
        second_index = first_index + second_condition.argmax()

        # Determina o preço de entrada, stop e take profit
        entry_price = close_1m[second_index]
        if second_index == 0:
            stop_price = high_1m[0]
        else:
            stop_price = high_1m[:second_index].max()
        take_profit_price = entry_price - (stop_price - entry_price)

        # Passo 3: Verifica a terceira condição (máxima >= máximo do candle de 6 horas anterior)
        third_condition = high_1m[:second_index] >= tf_high
        if third_condition.any():
            return np.nan, np.nan, np.nan, np.nan

    return 1, entry_price, stop_price, take_profit_price

PullbackIndicator = IndicatorFactory(
    class_name="PullbackWithTargets",
    input_names=['low_1m', 'high_1m', 'close_1m'],
    param_names=['midpoint', 'tf_high', 'tf_low', 'tf_close', 'reversal_signal'],
    output_names=['pullback_signal', 'entry_price', 'stop_price', 'take_profit_price']
).with_custom_func(pullback_custom_func)

# Definindo a função de ordem customizada com expiração
@njit
def order_func_nb(c, position_size, pullback_signal, entry_price, stop_price, take_profit_price, expiration_time):
    # Verifica se os preços são válidos
    if np.isnan(pullback_signal[c.i]) or np.isnan(entry_price[c.i]) or np.isnan(stop_price[c.i]) or np.isnan(take_profit_price[c.i]):
        return vbt.pf_enums.NoOrder

    # Verifica se os preços são positivos
    if entry_price[c.i] <= 0 or stop_price[c.i] <= 0 or take_profit_price[c.i] <= 0:
        return vbt.pf_enums.NoOrder

    # Confere a condição para abrir uma posição de compra (long)
    if pullback_signal[c.i] == 1:
        if c.close[c.i, c.col] >= entry_price[c.i]:  # Confirmar a entrada
            return vbt.pf_nb.order_nb(
                size=position_size,
                price=entry_price[c.i],
                direction=vbt.pf_enums.Direction.LongOnly
            )

    # Confere a condição para abrir uma posição de venda (short)
    elif pullback_signal[c.i] == -1:
        if c.close[c.i, c.col] <= entry_price[c.i]:  # Confirmar a entrada
            return vbt.pf_nb.order_nb(
                size=-position_size,
                price=entry_price[c.i],
                direction=vbt.pf_enums.Direction.ShortOnly
            )

    # Condição de stop e take-profit para posições abertas
    if c.position_now > 0:  # Posição de compra aberta
        if c.close[c.i, c.col] <= stop_price[c.i]:  # Stop Loss
            return vbt.pf_nb.close_position_nb(
                price=stop_price[c.i]
            )
        elif c.close[c.i, c.col] >= take_profit_price[c.i]:  # Take Profit
            return vbt.pf_nb.close_position_nb(
                price=take_profit_price[c.i]
            )

    elif c.position_now < 0:  # Posição de venda aberta
        if c.close[c.i, c.col] >= stop_price[c.i]:  # Stop Loss para short
            return vbt.pf_nb.close_position_nb(
                price=stop_price[c.i]
            )
        elif c.close[c.i, c.col] <= take_profit_price[c.i]:  # Take Profit para short
            return vbt.pf_nb.close_position_nb(
                price=take_profit_price[c.i]
            )

    return vbt.pf_enums.NoOrder



if __name__ == "__main__":
    start_time = time.time()
    DB_PATH = "forex_market.duckdb"
    symbol = "AUDCAD"
    data = vbt.DuckDBData.from_duckdb(symbol, connection=DB_PATH)

    last_date = data.index.max()
    one_month_ago = last_date - pd.DateOffset(months=1)
    data = data.loc[one_month_ago:]

    # Definindo a frequência para o resampling de timeframe superior
    time_frame = 6
    freq = f'{time_frame}h'
    timeframe_minutes = time_frame * 60
    # Parâmetros do backtesting
    initial_capital = 25000
    position_size = 0.02  # Porcentagem do capital para cada trade

    # Resampling para um timeframe superior
    data_fm_close = data.close.vbt.resample_apply(freq, vbt.nb.last_reduce_nb)
    data_fm_open = data.open.vbt.resample_apply(freq, vbt.nb.first_reduce_nb)
    data_fm_high = data.high.vbt.resample_apply(freq, vbt.nb.max_reduce_nb)
    data_fm_low = data.low.vbt.resample_apply(freq, vbt.nb.min_reduce_nb)
    midpoints = (data_fm_close + data_fm_open) / 2
    print('midpoints')
    print(len(midpoints))

    # Geração dos sinais de reversão
    reversal_signals = ReversalSignal.run(open=data_fm_open, close=data_fm_close).signal
    print('reversal_signals')
    print(reversal_signals)
     # Aplicação do PullbackIndicator com intervalos segmentados
    results = []
    for i in range(1, len(midpoints)):
        # Obter os valores únicos para o timeframe maior
        midpoint = midpoints.iloc[i-1]
        tf_high = data_fm_high.iloc[i-1]
        tf_low = data_fm_low.iloc[i-1]
        tf_close = data_fm_close.iloc[i-1]
        reversal_signal = reversal_signals[reversal_signals.index == midpoints.index[i]].values[0]

        # Selecionar dados de 1 minuto dentro do intervalo do candle de 6 horas
        interval_start = midpoints.index[i]
        interval_end = interval_start + pd.Timedelta(minutes=timeframe_minutes-1)
        low_1m = data.low.loc[interval_start:interval_end].values
        high_1m = data.high.loc[interval_start:interval_end].values
        close_1m = data.close.loc[interval_start:interval_end].values

        # Executar PullbackIndicator para o intervalo específico
        pullback_result = pullback_custom_func(midpoint, tf_high, tf_low, tf_close, reversal_signal, low_1m, high_1m, close_1m)
        results.append(pullback_result)

    # Convertendo resultados para DataFrame para visualização
    pullback_df = pd.DataFrame(results, columns=['pullback_signal', 'entry_price', 'stop_price', 'take_profit_price'], index=midpoints.index[1:])
    pullback_df['entry_price'] = pullback_df['entry_price'].ffill()
    pullback_df['stop_price'] = pullback_df['stop_price'].ffill()
    pullback_df['take_profit_price'] = pullback_df['take_profit_price'].ffill()
    pullback_df['pullback_signal'] = pullback_df['pullback_signal'].ffill()

    # Exibir os resultados
    print("Sinais de Pullback:\n", pullback_df['pullback_signal'])
    print("\nPreços de Entrada:\n", pullback_df['entry_price'])
    print("\nPreços de Stop:\n", pullback_df['stop_price'])
    print("\nPreços de Take Profit:\n", pullback_df['take_profit_price'])

    # Configurar o portfólio utilizando a função de ordem customizada
    portfolio = vbt.Portfolio.from_order_func(
    close=data.close,
    order_func_nb=order_func_nb,
    order_args=(
        position_size,
        pullback_df['pullback_signal'].values,
        pullback_df['entry_price'].values,
        pullback_df['stop_price'].values,
        pullback_df['take_profit_price'].values,
        timeframe_minutes
    ),
    init_cash=initial_capital,
    cash_sharing=True
    )

    # Estatísticas de desempenho do portfólio
    portfolio_stats = portfolio.stats()
    print(portfolio_stats)
    
    #portfolio = portfolio.value()
    # Valor do portfólio ao longo do tempo
    portfolio.vbt.plot().show()

    # Detalhes dos trades
    trades = portfolio.trades.records_readable
    print(trades)

    
