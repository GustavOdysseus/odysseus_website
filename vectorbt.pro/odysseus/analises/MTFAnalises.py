import vectorbtpro as vbt
from screeninfo import get_monitors
import pandas as pd

vbt.settings.set_theme("dark")

if __name__ == "__main__":
    # Obtém as dimensões do monitor principal
    monitor = get_monitors()[0]
    
    # Usa 80% do tamanho do monitor para o gráfico
    width = int(monitor.width * 0.95)
    height = int(monitor.height * 0.95)

    # Carregando os dados de preços usando SerialEngine
    DB_PATH = "../forex_market.duckdb"
    symbol = "EURUSD"
    data = vbt.DuckDBData.from_duckdb(symbol, start="2013-01-01", connection=DB_PATH)

    time_frames = [1, 4, 24]
    freqs = [f'{tf}h' for tf in time_frames]
    h1_data = data.resample("1h")
    h1_close = h1_data.close
    h4_data = data.resample("4h")
    h4_close = h4_data.close
    h24_data = data.resample("24h")
    h24_close = h24_data.close

    h4_close_shifted = h4_close.shift()
    h1_h4_ratio = h1_close / h4_close_shifted

    h4_h1_close = h4_close.shift(1).resample("1h").last().shift(-1).ffill()
    h24_h1_close = h24_close.shift(1).resample("1h").last().shift(-1).ffill()

    # Criação do gráfico base
    fig = h1_close.rename("H1").iloc[-512:].vbt.plot()
    h4_h1_close.rename("H4_H1").iloc[-512:].vbt.plot(fig=fig)
    h24_h1_close.rename("H24_H1").iloc[-512:].vbt.plot(fig=fig)
    
    # Atualiza o layout usando as dimensões do monitor
    fig.update_layout(
        width=width,
        height=height
    )
    
    # Abre o gráfico no navegador padrão
    fig.show()

    h1_h4_ratio = h1_close / h4_h1_close
    h1_h24_ratio = h1_close / h24_h1_close
    fig = h1_h4_ratio.rename("H1_H4").iloc[-512:].vbt.plot()
    h1_h24_ratio.rename("H1_H24").iloc[-512:].vbt.plot(fig=fig)

    fig.update_layout(
        width=width,  
        height=height 
    )
    fig.show()

    h1_sma = vbt.talib("SMA", timeperiod=4).run(h1_close, skipna=True).real
    h4_sma = vbt.talib("SMA", timeperiod=8).run(h4_h1_close, skipna=True).real
    h24_sma = vbt.talib("SMA", timeperiod=16).run(h24_h1_close, skipna=True).real

    h1_sma = h1_sma.ffill()
    h4_sma = h4_sma.ffill()
    h24_sma = h24_sma.ffill()

    print(h1_sma)
    print(h4_sma)
    print(h24_sma)

    fig = h1_sma.rename("h1_sma").iloc[-512:].vbt.plot()
    h4_sma.rename("h4_sma").iloc[-512:].vbt.plot(fig=fig)
    h24_sma.rename("h24_sma").iloc[-512:].vbt.plot(fig=fig)

    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    entries = h1_sma.vbt.crossed_above(h24_sma)
    exits = h1_sma.vbt.crossed_below(h24_sma)

    def plot_date_range(date_range):
        fig = h1_sma[date_range].rename("h1_sma").vbt.plot()
        h4_sma[date_range].rename("h4_sma").vbt.plot(fig=fig)
        entries[date_range].rename("Entry").vbt.signals.plot_as_entries(
            y=h1_sma[date_range], fig=fig)
        exits[date_range].rename("Exit").vbt.signals.plot_as_exits(
            y=h1_sma[date_range], fig=fig)

        # Atualiza o layout usando as dimensões do monitor
        fig.update_layout(
            width=width,    
            height=height   
        )
        return fig

    # Cria e mostra o gráfico
    fig = plot_date_range(slice("2019-02-01", "2023-03-01"))
    fig.show()

    def generate_bandwidths(freqs):
        bandwidths = []
        for freq in freqs:
            close = h1_data.resample(freq).get("Close")
            bbands = vbt.talib("BBANDS").run(close, skipna=True)
            upperband = bbands.upperband.ffill()
            middleband = bbands.middleband.ffill()
            lowerband = bbands.lowerband.ffill()
            bandwidth = (upperband - lowerband) / middleband
            bandwidths.append(bandwidth.vbt.realign_closing("1h"))
        df = pd.concat(bandwidths, axis=1, keys=pd.Index(freqs, name="timeframe"))
        return df.ffill()

    bandwidths = generate_bandwidths(["1h", "4h", "1d"])
    print(bandwidths)

    fig = bandwidths.iloc[-1024:, ::-1].vbt.ts_heatmap()
    
    # Atualiza o layout usando as dimensões do monitor
    fig.update_layout(
        width=width,    
        height=height   
    )
    
    # Abre o gráfico no navegador padrão
    fig.show()

    bbands = vbt.talib("BBANDS").run(
        h1_data.close, 
        skipna=True, 
        timeframe=["1h", "4h", "1d"],
        broadcast_kwargs=dict(wrapper_kwargs=dict(freq="1h"))
    )
    bandwidth = (bbands.upperband - bbands.lowerband) / bbands.middleband
    print(bandwidth)

    def generate_signals(data, freq, fast_window, slow_window):
        open_price = h1_data.get("Open").resample(freq).first()
        fast_sma = vbt.talib("SMA")\
            .run(
                open_price, 
                fast_window, 
                skipna=True, 
                short_name="fast_sma"
            )\
            .real.ffill()\
            .vbt.realign(data.wrapper.index)
        slow_sma = vbt.talib("SMA")\
            .run(
                open_price, 
                slow_window, 
                skipna=True, 
                short_name="slow_sma"
            )\
            .real.ffill()\
            .vbt.realign(data.wrapper.index)
        entries = fast_sma.vbt.crossed_above(slow_sma)
        exits = fast_sma.vbt.crossed_below(slow_sma)
        return entries, exits

    fast_window = [10, 20]
    slow_window = [20, 30]
    h1_entries, h1_exits = generate_signals(h1_data, "1h", fast_window, slow_window)
    h4_entries, h4_exits = generate_signals(h1_data, "4h", fast_window, slow_window)
    d1_entries, d1_exits = generate_signals(h1_data, "1d", fast_window, slow_window)

    entries = pd.concat(
        (h1_entries, h4_entries, d1_entries), 
        axis=1, 
        keys=pd.Index(["1h", "4h", "1d"], name="timeframe")
    )
    exits = pd.concat(
        (h1_exits, h4_exits, d1_exits), 
        axis=1,
        keys=pd.Index(["1h", "4h", "1d"], name="timeframe")
    )

    fig = (entries.astype(int) - exits.astype(int))\
        .resample("1d").sum()\
        .vbt.ts_heatmap(
            trace_kwargs=dict(
                colorscale=["#ef553b", "rgba(0, 0, 0, 0)", "#17becf"],
                colorbar=dict(
                    tickvals=[-1, 0, 1],
                    ticktext=["Exit", "", "Entry"]
                )
            )
        )
    
    # Atualiza o layout usando as dimensões do monitor
    fig.update_layout(
        width=width,    
        height=height   
    )
    
    # Abre o gráfico no navegador padrão
    fig.show()

    pf = vbt.Portfolio.from_signals(
        h1_data,
        entries,
        exits,
        sl_stop=0.1,
        freq="1h"
    )

    print(pf.orders.count())
    print(pf.cumulative_returns)
    print(pf.drawdown)
    print(pf.max_drawdown)
    print(pf.omega_ratio)
    print(pf.value_at_risk)
    print(pf.cond_value_at_risk)
    print(pf.total_profit)
    print(pf.total_return)


    fast_sma = vbt.talib("SMA").run(h1_close, timeperiod=vbt.Default(4))
    slow_sma = vbt.talib("SMA").run(h24_h1_close, timeperiod=vbt.Default(4))
    entries = fast_sma.real_crossed_above(slow_sma.real)
    exits = fast_sma.real_crossed_below(slow_sma.real)

    pf = vbt.Portfolio.from_signals(h1_close, entries, exits)

    # Cria o gráfico do portfolio
    fig = pf.plot()
    
    # Atualiza o layout usando as dimensões do monitor
    fig.update_layout(
        width=width,    
        height=height
    )
    
    # Abre o gráfico no navegador padrão
    fig.show()
    
    print("Número de ordens:")
    print(pf.orders.count())
    print("Retorno cumulativo:")
    print(pf.cumulative_returns)
    print("Drawdown:")
    print(pf.drawdown)
    print("Máximo drawdown:")
    print(pf.max_drawdown)
    print("Omega ratio:")
    print(pf.omega_ratio)
    print("Value at risk:")
    print(pf.cond_value_at_risk)
    print("Profit total:")
    print(pf.total_profit)
    print("Retorno total:")
    print(pf.total_return)

    ms_pf = pf.resample("M")
    fig = ms_pf.plot()
    fig.update_layout(
        width=width,    
        height=height
    )
    fig.show()

    print(ms_pf.trades.pnl.to_pd(reduce_func_nb="sum"))