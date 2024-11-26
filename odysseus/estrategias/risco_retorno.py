import vectorbtpro as vbt
import numpy as np
import pandas as pd
import os

# Configuração temporária para o carregamento de dados
vbt.settings.execution.engine = 'serial'  # Usando SerialEngine para o carregamento de dados

# Carregando os dados de preços usando SerialEngine
DB_PATH = "../forex_market.duckdb"
symbol = "EURUSD"
time_frame = 1
freq = f'{time_frame}h'
data = vbt.DuckDBData.from_duckdb(symbol, start="2013-01-01", connection=DB_PATH)
close_price = data.close.vbt.resample_apply(freq, vbt.nb.last_reduce_nb)

# Reconfigura para Ray após o carregamento dos dados
vbt.settings.execution.engine = 'ray'
vbt.settings.execution.engine_config = {
    'n_workers': os.cpu_count() // 2,
    'show_progress': True,
    'timeout': 300
}

# Configurações válidas de caching e chunking
vbt.settings.caching.update({
    'disable': False,
    'use_cached_accessors': True
})

vbt.settings.execution.update({
    'cache_chunks': True,
    'chunk_cache_dir': "cache_chunks",
    'release_chunk_cache': True
})

@vbt.parameterized(
    merge_func="concat",
    cache_chunks=True,
    chunk_len=100,
    n_chunks="auto",
    execute_kwargs={
        'show_progress': True,
        'clear_cache': True,
        'collect_garbage': True
    }
)
def volatility_strategy(close, window, wtype, alpha, minp, adjust, ddof, bb_thresh_low, bb_thresh_high, bb_thresh_vol_low, bb_thresh_vol_high):
    bb = vbt.BBANDS.run(close, window=window, wtype=wtype, alpha=alpha, minp=minp, adjust=adjust, ddof=ddof)
    bandwidth = bb.bandwidth
    percent_b = bb.percent_b
    
    entries = np.asarray((percent_b < bb_thresh_low) & (bandwidth < bb_thresh_vol_low), dtype=bool)
    exits = np.asarray((percent_b > bb_thresh_high) & (bandwidth > bb_thresh_vol_high), dtype=bool)
    return entries, exits

def calculate_optimal_size(account_balance, risk_per_trade, stop_loss_pips, pip_value):
    risk_amount = account_balance * (risk_per_trade / 100)
    position_size = risk_amount / (stop_loss_pips * pip_value)
    return position_size

if __name__ == "__main__":

    periods = vbt.Param(np.arange(5, 46, 5))
    wtypes = vbt.Param(["simple", "exp"])
    alphas = vbt.Param([1, 2])
    minps = vbt.Param([1, 2])
    adjusts = vbt.Param([True, False])
    ddofs = vbt.Param([0, 1])
    bb_thresh_lows = vbt.Param(np.arange(-1, 2, 0.1), condition="x < bb_thresh_high")
    bb_thresh_highs = vbt.Param(np.arange(-1, 2, 0.1), condition="x > bb_thresh_low")
    bb_thresh_vol_lows = vbt.Param(np.arange(0, 0.032, 0.001), condition="x < bb_thresh_vol_high")
    bb_thresh_vol_highs = vbt.Param(np.arange(0, 0.032, 0.001), condition="x > bb_thresh_vol_low")

    entries, exits = volatility_strategy(
        close=close_price,
        window=periods,
        wtype=wtypes,
        alpha=alphas,
        minp=minps,
        adjust=adjusts,
        ddof=ddofs,
        bb_thresh_low=bb_thresh_lows,
        bb_thresh_high=bb_thresh_highs,
        bb_thresh_vol_low=bb_thresh_vol_lows,
        bb_thresh_vol_high=bb_thresh_vol_highs
    )

    entries = pd.DataFrame(entries, index=close_price.index).astype(bool)
    exits = pd.DataFrame(exits, index=close_price.index).astype(bool)

    account_balance = 25000
    risk_per_trade = 0.2
    stop_loss_pips = 20
    pip_value = 1
    optimal_size = calculate_optimal_size(account_balance, risk_per_trade, stop_loss_pips, pip_value)

    full_lot_fee = 5
    portfolio = vbt.Portfolio.from_signals(
        close=close_price,
        entries=entries,
        exits=exits,
        init_cash=account_balance,
        size=optimal_size,
        fees=lambda size, price: full_lot_fee * abs(size),
        slippage=0.0025
    )

    portfolio_sharpe = portfolio.get_sharpe_ratio(sim_start="2014-01-01", sim_end="2022-12-31", rec_sim_range=True)
    performance = portfolio.get_total_return(sim_start="2014-01-01", sim_end="2022-12-31", rec_sim_range=True)
    
    print("\nSharpe Ratios:\n", portfolio_sharpe)
    print("\nTotal Returns:\n", performance)
    print("\nMax Drawdowns:\n", portfolio.max_drawdown())

    # Exibe gráficos se o ambiente permitir
    fig = portfolio.plot().update_layout(title="Portfolio Performance with Optimized Strategy")
    fig.show()
    performance_df = pd.DataFrame({'Total Return': performance, 'Sharpe Ratio': portfolio_sharpe})
    performance_df.plot(kind='bar', title='Performance Metrics by Parameter Combinations').show()
