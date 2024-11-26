# tendencia.py

import numpy as np
import pandas as pd
from numba import njit
import vectorbtpro as vbt
import talib
from typing import NamedTuple as tp_NamedTuple
import typing as tp

class SuperTrend:
    def __init__(self, timeframe='1h'):
        """
        Args:
            timeframe (str): Timeframe para análise (ex: '1m', '5m', '1h', '4h', '1d')
        """
        vbt.settings.set_theme('dark')
        self.timeframe = timeframe
        
    def load_data(self, symbols=['EURUSD', 'AUDUSD'], start='2023-03-01', end='2023-05-01', path='../forex_market.duckdb'):
        """Carrega ou baixa dados históricos"""
        self.data = vbt.DuckDBData.from_duckdb(
            symbols,
            start=start,
            end=end,
            connection=path
        )
        
        # Usa o timeframe definido na instância
        self.data = self.data.resample(self.timeframe)
            
        self.high = self.data.get('High')
        self.low = self.data.get('Low') 
        self.close = self.data.get('Close')

    @staticmethod
    def get_med_price(high, low):
        """Calcula preço médio usando TA-Lib"""
        return talib.MEDPRICE(high, low)

    @staticmethod
    @njit
    def get_final_bands_nb(close, upper, lower):
        """Versão Numba otimizada para cálculo das bandas finais"""
        trend = np.full(close.shape, np.nan)
        dir_ = np.full(close.shape, 1)
        long = np.full(close.shape, np.nan)
        short = np.full(close.shape, np.nan)

        for i in range(1, close.shape[0]):
            if close[i] > upper[i - 1]:
                dir_[i] = 1
            elif close[i] < lower[i - 1]:
                dir_[i] = -1
            else:
                dir_[i] = dir_[i - 1]
                if dir_[i] > 0 and lower[i] < lower[i - 1]:
                    lower[i] = lower[i - 1]
                if dir_[i] < 0 and upper[i] > upper[i - 1]:
                    upper[i] = upper[i - 1]

            if dir_[i] > 0:
                trend[i] = long[i] = lower[i]
            else:
                trend[i] = short[i] = upper[i]

        return trend, dir_, long, short

    def supertrend(self, high, low, close, period=7, multiplier=3):
        """Implementação otimizada do SuperTrend usando TA-Lib"""
        avg_price = talib.MEDPRICE(high, low)
        atr = talib.ATR(high, low, close, period)

        # Calcula bandas básicas
        matr = multiplier * atr
        upper = avg_price + matr
        lower = avg_price - matr

        return self.get_final_bands_nb(close, upper, lower)

    def backtest(self, symbol='BTCUSDT', period=7, multiplier=3):
        """Executa backtest da estratégia"""
        supert, superd, superl, supers = self.supertrend(
            self.high[symbol].values,
            self.low[symbol].values,
            self.close[symbol].values,
            period,
            multiplier
        )

        # Gera sinais
        entries = (~pd.Series(superl, index=self.close.index).isnull()).vbt.signals.fshift()
        exits = (~pd.Series(supers, index=self.close.index).isnull()).vbt.signals.fshift()
        print('entries')
        print(entries)
        print('entradas True')
        print(entries.sum())
        print('entradas False')
        print(entries.sum() - entries.size)
        print('-'*10)
        print('exits')
        print(exits)
        print('exits True')
        print(exits.sum())
        print('exits False')
        print(exits.sum() - exits.size)
        # Cria portfólio
        pf = vbt.Portfolio.from_signals(
            close=self.close[symbol],
            entries=entries,
            exits=exits,
            fees=0.001,
            freq=self.timeframe
        )

        return pf

    def optimize(self, symbol='BTCUSDT', periods=range(4,8), multipliers=np.arange(20,26)/10):
        """Otimiza parâmetros"""
        period_product, multiplier_product = vbt.generate_param_combs(
            (vbt.product, periods, multipliers)
        )
        
        st = vbt.IF(
            class_name='SuperTrend',
            short_name='st',
            input_names=['high', 'low', 'close'],
            param_names=['period', 'multiplier'],
            output_names=['supert', 'superd', 'superl', 'supers']
        ).with_apply_func(
            self.supertrend,
            takes_1d=True
        )

        results = st.run(
            self.high[symbol],
            self.low[symbol],
            self.close[symbol],
            period=period_product,
            multiplier=multiplier_product,
            param_product=True
        )

        return results

    def plot(self, symbol='BTCUSDT', date_range=slice('2023-03-01', '2023-04-01')):
        """Plota resultados"""
        supert, superd, superl, supers = self.supertrend(
            self.high[symbol].values,
            self.low[symbol].values,
            self.close[symbol].values
        )
        
        fig = self.close.loc[date_range, symbol].rename('Close').vbt.plot()
        pd.Series(supers, index=self.close.index).loc[date_range].rename('Short').vbt.plot(fig=fig)
        pd.Series(superl, index=self.close.index).loc[date_range].rename('Long').vbt.plot(fig=fig)
        
        return fig

if __name__ == '__main__':
    # Exemplo de uso com timeframe personalizado
    timeframe = '1h'
    symbols = ['EURUSD', 'AUDUSD']
    start = '2021-01-01'
    end = '2023-01-01'
    path = '../forex_market.duckdb'

    st = SuperTrend(timeframe=timeframe)  # ou qualquer outro timeframe
    st.load_data(symbols, start, end, path)
    
    # Backtest básico
    pf = st.backtest(symbols[0])
    print(pf.stats())

    periodos = np.logspace(1, 5, num=4, base=2, dtype=int) #range(4, 55, 10)
    multiplicadores = np.arange(10, 41, 10) / 10

    # Otimização
    results = st.optimize(symbols[0], periodos, multiplicadores)
    print(results.stats())

    date_range = slice(start, end)
    # Plot
    fig = st.plot(symbols[0], date_range)
    fig.show()
