import time
import numpy as np
import pandas as pd
start_load_libraries = time.time()
import vectorbtpro as vbt
import timeit
timeit.timeit("import vectorbtpro as vbt", number=1)
from vectorbtpro import IndicatorFactory
end_load_libraries = time.time()
print(f"Tempo de carregamento de bibliotecas: {end_load_libraries - start_load_libraries:.2f} segundos")

# Definir o indicador de reversão
def reversal_pattern_np(open_array, close_array):
    out = np.full_like(close_array, np.nan, dtype=np.float64)
    close_shift_1 = np.roll(close_array, 1)
    open_shift_1 = np.roll(open_array, 1)
    close_shift_2 = np.roll(close_array, 2)
    open_shift_2 = np.roll(open_array, 2)
    
    close_shift_1[:1] = np.nan
    open_shift_1[:1] = np.nan
    close_shift_2[:2] = np.nan
    open_shift_2[:2] = np.nan

    long_cond = (close_shift_2 < open_shift_2) & (close_shift_1 > open_shift_1)
    short_cond = (close_shift_2 > open_shift_2) & (close_shift_1 < open_shift_1)

    out[long_cond] = 1
    out[short_cond] = -1
    return out

ReversalIndicator = IndicatorFactory(
    class_name="ReversalPattern",
    input_names=['open', 'close'],
    output_names=['signal'],
    short_name='RPR'
).with_apply_func(reversal_pattern_np)

# Função de recuo otimizada para implementar as condições hierárquicas com base no timeframe de 6 horas
def pullback_signal_np(low_array, high_array, time_index, reversal_signals, tf_open, tf_close, tf_low, tf_high, tf_timedelta):
    # Calcula o ponto médio e valores anteriores com base no candle anterior de 6 horas
    tf_open_shift_1 = np.roll(tf_open, 1)
    tf_close_shift_1 = np.roll(tf_close, 1)
    tf_prev_low = np.roll(tf_low, 1)
    tf_prev_high = np.roll(tf_high, 1)

    # Alinha os valores anteriores com o timeframe de 1 minuto
    tf_open_shift_1[:1] = np.nan
    tf_close_shift_1[:1] = np.nan
    tf_prev_low[:1] = np.nan
    tf_prev_high[:1] = np.nan
    
    # Calcula o ponto médio e garante que ele seja unidimensional
    midpoint = (tf_open_shift_1 + tf_close_shift_1) / 2

    # Alinha `out` com o timeframe de 1 minuto
    out = np.full_like(low_array, np.nan, dtype=np.float64)

    for i in range(len(reversal_signals)):
        if np.isnan(reversal_signals[i]):
            continue

        # Define o intervalo de 1 minuto correspondente ao sinal de 6 horas usando time_index
        end_time = time_index[i] + tf_timedelta
        mask = (time_index >= time_index[i]) & (time_index < end_time)

        # Passo 1: Verificar a primeira condição (mínima <= ponto médio do candle de 6 horas anterior)
        first_condition = (low_array[mask] <= midpoint[i])

        print('midpoint[i]') if not np.isnan(midpoint[i]) else 'nan'
        print(midpoint[i]) if not np.isnan(midpoint[i]) else 'nan'
        if not first_condition.any():
            continue  # Se não houver primeira condição, passa para o próximo índice

        # Obter o índice do primeiro valor que satisfaz a primeira condição
        first_index = np.where(mask)[0][first_condition.argmax()]
        print('primeira condição')
        print(first_index)
        # Passo 2: Verificar a segunda condição (máxima >= close_shift_1 do candle de 6 horas) após o índice da primeira condição
        second_condition = (high_array[first_index:] >= tf_close_shift_1[i])
        if not second_condition.any():
            continue  # Se não houver segunda condição, passa para o próximo índice
        # Obter o índice do segundo valor que satisfaz a segunda condição
        second_index = first_index + second_condition.argmax()
        print('segunda condição')
        print(second_index)

        # Passo 3: Verificar a terceira condição (mínima <= prev_low do candle de 6 horas) antes do índice da segunda condição
        third_condition = (low_array[i:second_index] <= tf_prev_low[i])
        if third_condition.any():
            continue  # Se a terceira condição for verdadeira, invalida o recuo e passa para o próximo índice
        print('terceira condição')
        print(third_condition)
        # Se todas as condições forem satisfeitas na ordem correta, retorna o sinal de pullback no timeframe de 6 horas
        out[i] = 1

    return out

# Instancia o indicador de pullback com flexibilidade de timeframe, definindo `tf_timedelta` como um param_name
PullbackIndicator = IndicatorFactory(
    class_name="PullbackToMidpoint",
    input_names=['low', 'high', 'time_index', 'reversal_signals', 'tf_open', 'tf_close', 'tf_low', 'tf_high'],
    param_names=['tf_timedelta'],
    output_names=['pullback_signal'],
    short_name='PBK'
).with_apply_func(pullback_signal_np)

if __name__ == "__main__":
    start_time = time.time()
    DB_PATH = "forex_market.duckdb"
    symbol = "AUDCAD"
    data = vbt.DuckDBData.from_duckdb(symbol, connection=DB_PATH)

    last_date = data.index.max()
    one_month_ago = last_date - pd.DateOffset(months=1)
    data = data.loc[one_month_ago:]

    # Definindo a frequência para o resampling de 6 horas
    freq = '6h'

    # Resampling para 6 horas
    data_6h_close = data.close.vbt.resample_apply("6h", vbt.nb.last_reduce_nb)
    data_6h_open = data.open.vbt.resample_apply("6h", vbt.nb.first_reduce_nb)
    data_6h_high = data.high.vbt.resample_apply("6h", vbt.nb.max_reduce_nb)
    data_6h_low = data.low.vbt.resample_apply("6h", vbt.nb.min_reduce_nb)

    # Aplicar indicador de reversão no timeframe superior
    reversal_ind_tf = ReversalIndicator.run(data_6h_open, data_6h_close)
    reversal_signals_tf = reversal_ind_tf.signal  # Mantém o sinal em 6 horas, sem ffill
    print('reversal_signals_tf')
    print(reversal_signals_tf)
    # Extrair o índice de tempo dos dados de 1 minuto
    time_index = data.index

    # Aplicar o indicador de pullback com Timedelta e dados de 6 horas
    tf_timedelta = vbt.timedelta(freq)
    pullback_signals = PullbackIndicator.run(
        data.low, data.high, time_index, reversal_signals_tf, data_6h_open, data_6h_close, data_6h_low, data_6h_high, tf_timedelta=tf_timedelta
    ).pullback_signal

    print("Sinais de Recuo com Timeframe de 1 minuto:")
    print(pullback_signals)
    print(pullback_signals.dropna())
    end_time = time.time()
    print(f"Tempo de execução: {end_time - start_time:.2f} segundos")

