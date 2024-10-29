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
def pullback_signal_vbt(midpoint, tf_high, tf_low, reversal_signal, low_1m, high_1m):
    """
    Calcula o sinal de pullback para um único candle com sinal de reversão,
    usando apenas os dados de 1 minuto correspondentes ao intervalo do candle maior.

    Parâmetros:
        midpoint: Ponto médio pré-calculado do candle de 6 horas.
        tf_high: Valor máximo do candle de 6 horas.
        tf_low: Valor mínimo do candle de 6 horas.
        reversal_signal: Sinal de reversão (True/False ou valor numérico).
        low_1m: Array com os valores de mínima de 1 minuto dentro do candle de 6 horas.
        high_1m: Array com os valores de máxima de 1 minuto dentro do candle de 6 horas.

    Retorna:
        Sinal de pullback (1 para verdadeiro, np.nan para falso).
    """
    # Verifica se há sinal de reversão
    if np.isnan(reversal_signal):
        return np.nan

    # Passo 1: Verifica a primeira condição (mínima <= midpoint)
    first_condition = low_1m <= midpoint
    if not first_condition.any():
        return np.nan  # Se a primeira condição não é satisfeita, retorna np.nan

    # Obtem o índice do primeiro valor que satisfaz a primeira condição
    first_index = first_condition.argmax()

    # Passo 2: Verifica a segunda condição (máxima >= fechamento do candle anterior de 6 horas)
    second_condition = high_1m[first_index:] >= tf_high
    if not second_condition.any():
        return np.nan  # Se a segunda condição não é satisfeita, retorna np.nan

    # Obtem o índice do primeiro valor que satisfaz a segunda condição
    second_index = first_index + second_condition.argmax()

    # Passo 3: Verifica a terceira condição (mínima <= mínimo do candle de 6 horas anterior)
    third_condition = low_1m[:second_index] <= tf_low
    if third_condition.any():
        return np.nan  # Se a terceira condição é satisfeita, invalida o sinal e retorna np.nan

    # Se todas as condições são satisfeitas na sequência correta, retorna sinal de pullback
    return 1

# Instancia o indicador de pullback com flexibilidade de timeframe, definindo `tf_timedelta` como um param_name
PullbackIndicator = IndicatorFactory(
    class_name="PullbackToMidpoint",
    input_names=['midpoint', 'tf_high', 'tf_low', 'reversal_signal', 'low_1m', 'high_1m'],
    output_names=['pullback_signal'],
    short_name='PBK'
).with_apply_func(pullback_signal_vbt)

if __name__ == "__main__":
    start_time = time.time()
    DB_PATH = "forex_market.duckdb"
    symbol = "AUDCAD"
    data = vbt.DuckDBData.from_duckdb(symbol, connection=DB_PATH)

    last_date = data.index.max()
    one_month_ago = last_date - pd.DateOffset(months=1)
    data = data.loc[one_month_ago:]

    # Definindo a frequência para o resampling de timeframe superior
    freq = '6h'

    # Resampling para um timeframe superior
    data_fm_close = data.close.vbt.resample_apply(freq, vbt.nb.last_reduce_nb)
    data_fm_open = data.open.vbt.resample_apply(freq, vbt.nb.first_reduce_nb)
    data_fm_high = data.high.vbt.resample_apply(freq, vbt.nb.max_reduce_nb)
    data_fm_low = data.low.vbt.resample_apply(freq, vbt.nb.min_reduce_nb)
    print('data_fm_low')
    print(data_fm_low)

    # Aplicar indicador de reversão no timeframe superior
    reversal_ind_tf = ReversalIndicator.run(data_fm_open, data_fm_close)
    reversal_signals_tf = reversal_ind_tf.signal  # Mantem o sinal em 6 horas, sem ffill

    # Extrair o índice de tempo dos dados de 1 minuto
    time_index = data.index

    # Aplicar o indicador de pullback com dados de 6 horas
    pullback_signals = PullbackIndicator.run(
        data.low, data.high, time_index, reversal_signals_tf, data_fm_low, data_fm_high
    ).pullback_signal

    print("Sinais de Recuo com Timeframe de 1 minuto:")
    print(pullback_signals)
    print(pullback_signals.dropna())
    end_time = time.time()
    print(f"Tempo de execução: {end_time - start_time:.2f} segundos")

