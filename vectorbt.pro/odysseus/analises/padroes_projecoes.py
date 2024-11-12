import vectorbtpro as vbt
from screeninfo import get_monitors
import numpy as np
import pandas as pd
import timeit
from functools import partial
from itertools import combinations

if __name__ == "__main__":
    vbt.settings.set_theme("dark")
    # Obtém as dimensões do monitor principal
    monitor = get_monitors()[0]
    
    # Usa 80% do tamanho do monitor para o gráfico
    width = int(monitor.width * 1)
    height = int(monitor.height * 1)

    # Carregando os dados de preços usando SerialEngine
    DB_PATH = "../forex_market.duckdb"
    symbol = "EURUSD"
    data_original = vbt.DuckDBData.from_duckdb(symbol, start="2023-01-01", connection=DB_PATH)
    data = data_original.loc["2023-11-13":"2023-11-17"] #.resample("1h")
    next_data = data_original.loc["2023-11-20":"2023-11-25"]
    next_data_close = next_data.close
    print("nexta_data_close")
    print(next_data_close)
    h1_data = data #.loc["2023-11-13":"2023-11-17"].resample("1h")
    n = 10


    fig = h1_data.loc["2022-11-13":"2023-11-17"].plot()
    fig.update_layout(
        width=width,    
        height=height
    )
    fig.show()

    janela_dados = h1_data #.loc["2023-11-13":"2023-11-17"]
    preco_janela = janela_dados.hlc3


    fig = preco_janela.vbt.plot()
    fig.update_layout(
        width=width,    
        height=height
    )
    fig.show()

    pattern = np.array([1, 2, 3, 2, 3, 2])


    fig = pd.Series(pattern).vbt.plot()
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    resized_pattern = vbt.nb.interp_resize_1d_nb(
        pattern, n, vbt.enums.InterpMode.Linear
    )


    def plot_linear(n):
        resized_pattern = vbt.nb.interp_resize_1d_nb(
            pattern, n, vbt.enums.InterpMode.Linear
        )
        return pd.Series(resized_pattern).vbt.plot()
    
    fig = plot_linear(n)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    resized_pattern = vbt.nb.interp_resize_1d_nb(
        pattern, n, vbt.enums.InterpMode.Linear
    )
    ratio = (len(pattern) - 1) / (len(resized_pattern) - 1)
    new_points = np.arange(len(resized_pattern)) * ratio

    fig = pd.Series(pattern).vbt.plot()
    pd.Series(resized_pattern, index=new_points).vbt.scatterplot(fig=fig)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    resized_pattern = vbt.nb.interp_resize_1d_nb(
            pattern, n, vbt.enums.InterpMode.Nearest
    )

    def plot_nearest(n):
        resized_pattern = vbt.nb.interp_resize_1d_nb(
            pattern, n, vbt.enums.InterpMode.Nearest
        )
        return pd.Series(resized_pattern).vbt.plot()
    
    fig = plot_nearest(n)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    resized_pattern = vbt.nb.interp_resize_1d_nb(
        pattern, n, vbt.enums.InterpMode.Discrete
    )


    def plot_discrete(n):
        resized_pattern = vbt.nb.interp_resize_1d_nb(
            pattern, n, vbt.enums.InterpMode.Discrete
        )
        return pd.Series(resized_pattern).vbt.plot(
            trace_kwargs=dict(
                line=dict(dash="dot"), 
                connectgaps=True
            )
        )
    
    fig = plot_discrete(n)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    resized_pattern = vbt.nb.interp_resize_1d_nb(
        pattern, n, vbt.enums.InterpMode.Mixed
    )


    def plot_mixed(n):
        lin_resized_pattern = vbt.nb.interp_resize_1d_nb(
            pattern, n, vbt.enums.InterpMode.Linear
        )
        mix_resized_pattern = vbt.nb.interp_resize_1d_nb(
            pattern, n, vbt.enums.InterpMode.Mixed
        )
        fig = pd.Series(lin_resized_pattern, name="Linear").vbt.plot()
        return pd.Series(mix_resized_pattern, name="Mixed").vbt.plot(fig=fig)
    
    fig = plot_mixed(n)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    resized_pattern = vbt.nb.interp_resize_1d_nb(
        pattern, len(preco_janela), vbt.enums.InterpMode.Mixed
    )

    pattern_scale = (resized_pattern.min(), resized_pattern.max())
    price_window_scale = (preco_janela.min(), preco_janela.max())
    rescaled_pattern = vbt.utils.array_.rescale_nb(
        resized_pattern, pattern_scale, price_window_scale
    )
    rescaled_pattern = pd.Series(rescaled_pattern, index=preco_janela.index)


    fig = preco_janela.vbt.plot()
    rescaled_pattern.vbt.plot(
        trace_kwargs=dict(
            fill="tonexty", 
            fillcolor="rgba(255, 100, 0, 0.25)"
        ), 
        fig=fig
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    pct_pattern = np.array([1, 1.3, 1.6, 1.3, 1.6, 1.3])
    resized_pct_pattern = vbt.nb.interp_resize_1d_nb(
        pct_pattern, len(preco_janela), vbt.enums.InterpMode.Mixed
    )
    rebased_pattern = resized_pct_pattern / resized_pct_pattern[0]
    rebased_pattern *= preco_janela.values[0]
    rebased_pattern = pd.Series(rebased_pattern, index=preco_janela.index)


    fig = preco_janela.vbt.plot()
    rebased_pattern.vbt.plot(
        trace_kwargs=dict(
            fill="tonexty", 
            fillcolor="rgba(255, 100, 0, 0.25)"
        ), 
        fig=fig
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    abs_distances = np.abs(rescaled_pattern - preco_janela.values)
    mae = abs_distances.sum()
    max_abs_distances = np.column_stack((
        (preco_janela.max() - rescaled_pattern), 
        (rescaled_pattern - preco_janela.min())
    )).max(axis=1)
    max_mae = max_abs_distances.sum()
    similarity = 1 - mae / max_mae
    print(similarity)

    quad_distances = (rescaled_pattern - preco_janela.values) ** 2
    rmse = np.sqrt(quad_distances.sum())
    max_quad_distances = np.column_stack((
        (preco_janela.max() - rescaled_pattern), 
        (rescaled_pattern - preco_janela.min())
    )).max(axis=1) ** 2
    max_rmse = np.sqrt(max_quad_distances.sum())
    similarity = 1 - rmse / max_rmse
    print(similarity)

    quad_distances = (rescaled_pattern - preco_janela.values) ** 2
    mse = quad_distances.sum()
    max_quad_distances = np.column_stack((
        (preco_janela.max() - rescaled_pattern), 
        (rescaled_pattern - preco_janela.min())
    )).max(axis=1) ** 2
    max_mse = max_quad_distances.sum()
    similarity = 1 - mse / max_mse
    print(similarity)

    print(vbt.nb.pattern_similarity_nb(preco_janela.values, pattern))

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pct_pattern, 
        rescale_mode=vbt.enums.RescaleMode.Rebase
    ))

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pct_pattern, 
        interp_mode=vbt.enums.InterpMode.Nearest,
        rescale_mode=vbt.enums.RescaleMode.Rebase,
        distance_measure=vbt.enums.DistanceMeasure.RMSE
    ))

    fig = preco_janela.vbt.plot_pattern(
        pct_pattern, 
        interp_mode="nearest",
        rescale_mode="rebase",
        fill_distance=True
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    adj_pct_pattern = np.array([1, 1.3, 1.6, 1.45, 1.6, 1.3])
    
    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        adj_pct_pattern, 
        interp_mode=vbt.enums.InterpMode.Nearest,
        rescale_mode=vbt.enums.RescaleMode.Rebase,
        distance_measure=vbt.enums.DistanceMeasure.RMSE
    ))

    fig = preco_janela.vbt.plot_pattern(
        adj_pct_pattern, 
        interp_mode="discrete",
        rescale_mode="rebase",
    )
    fig.update_layout(
        width=width,
        height=height
    )

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        adj_pct_pattern, 
        interp_mode=vbt.enums.InterpMode.Discrete,
        rescale_mode=vbt.enums.RescaleMode.Rebase,
        distance_measure=vbt.enums.DistanceMeasure.RMSE
    ))

    abs_pct_distances = abs_distances / rescaled_pattern
    pct_mae = abs_pct_distances.sum()
    max_abs_pct_distances = max_abs_distances / rescaled_pattern
    max_pct_mae = max_abs_pct_distances.sum()
    similarity = 1 - pct_mae / max_pct_mae
    print(similarity)

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pct_pattern, 
        error_type=vbt.enums.ErrorType.Relative
    ))

    print(vbt.nb.pattern_similarity_nb(
        np.array([10, 30, 100]),
        np.array([1, 2, 3]),
        error_type=vbt.enums.ErrorType.Absolute
    ))

    print(vbt.nb.pattern_similarity_nb(
        np.array([10, 30, 100]),
        np.array([1, 2, 3]),
        error_type=vbt.enums.ErrorType.Relative
    ))

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pattern, 
        invert=True
    ))

    fig = preco_janela.vbt.plot_pattern(pattern, invert=True)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    print(pattern.max() + pattern.min() - pattern)

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pattern,
        invert=True
    ))

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pattern, 
        max_error=np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5]),
    ))

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pattern, 
        max_error=np.array([0.5]),
    ))

    fig = preco_janela.vbt.plot_pattern(
        pattern, 
        max_error=0.5
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pattern, 
        max_error=np.array([0.5]),
        max_error_strict=True
    ))

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        adj_pct_pattern, 
        rescale_mode=vbt.enums.RescaleMode.Rebase,
        max_error=np.array([0.2, 0.1, 0.05, 0.1, 0.05, 0.1]),
        max_error_strict=True
    ))

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pattern, 
        max_error=np.array([0.1]),
        error_type=vbt.enums.ErrorType.Relative
    ))

    fig = preco_janela.vbt.plot_pattern(
        pattern, 
        max_error=0.01,
        error_type="relative"
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()
    
    fig = preco_janela.vbt.plot_pattern(
        adj_pct_pattern, 
        rescale_mode="rebase",
        max_error=np.array([0.02, 0.01, 0.005, 0.01, 0.005, 0.01])
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        adj_pct_pattern, 
        rescale_mode=vbt.enums.RescaleMode.Rebase,
        max_error=np.array([0.2, 0.1, 0.05, 0.1, 0.05, 0.1]) + 0.05,
        max_error_strict=True
    ))

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        adj_pct_pattern, 
        rescale_mode=vbt.enums.RescaleMode.Rebase,
        max_error=np.array([np.nan, np.nan, 0.1, np.nan, 0.1, np.nan]),
        max_error_interp_mode=vbt.enums.InterpMode.Discrete,
        max_error_strict=True
    ))

    fig = preco_janela.vbt.plot_pattern(
        adj_pct_pattern, 
        rescale_mode="rebase",
        max_error=np.array([np.nan, np.nan, 0.01, np.nan, 0.01, np.nan]),
        max_error_interp_mode="discrete"
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pattern, 
        max_error=np.array([np.nan, np.nan, 0.1, np.nan, 0.1, np.nan]),
        max_error_interp_mode=vbt.enums.InterpMode.Discrete,
        max_error_strict=True
    ))

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pattern, 
        max_error=np.array([0.5]),
        max_error_as_maxdist=True
    ))

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pattern, 
        max_pct_change=0.3
    ))

    print(vbt.nb.pattern_similarity_nb(
        preco_janela.values, 
        pattern, 
        min_similarity=0.9
    ))

    price = h1_data.hlc3

    similarity = price.vbt.rolling_pattern_similarity(
        pattern, 
        window=30,
        error_type="relative",
        max_error=0.05,
        max_error_interp_mode="discrete"
    )
    print(similarity.describe())


    end_row = similarity.argmax() + 1
    start_row = end_row - 30
    fig = h1_data.iloc[start_row:end_row].plot(plot_volume=False)
    price.iloc[start_row:end_row].vbt.plot_pattern(
        pattern, 
        error_type="relative",
        max_error=0.05,
        max_error_interp_mode="discrete",
        plot_obj=False, 
        fig=fig
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    end_row = similarity.argmin() + 1
    start_row = end_row - 30
    fig = h1_data.iloc[start_row:end_row].plot(plot_volume=False)
    price.iloc[start_row:end_row].vbt.plot_pattern(
        pattern, 
        invert=True,
        error_type="relative",
        max_error=0.05,
        max_error_interp_mode="discrete",
        plot_obj=False, 
        fig=fig
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    inv_similarity = price.vbt.rolling_pattern_similarity(
        pattern, 
        window=30,
        invert=True,
        error_type="relative",
        max_error=0.05,
        max_error_interp_mode="discrete"
    )
    print(inv_similarity.describe())

    end_row = inv_similarity.argmax() + 1
    start_row = end_row - 30
    fig = h1_data.iloc[start_row:end_row].plot(plot_volume=False)
    price.iloc[start_row:end_row].vbt.plot_pattern(
        pattern, 
        invert=True,
        error_type="relative",
        max_error=0.05,
        max_error_interp_mode="discrete",
        plot_obj=False, 
        fig=fig
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    patsim = vbt.PATSIM.run(
        price, 
        vbt.Default(pattern),
        error_type=vbt.Default("relative"),
        max_error=vbt.Default(0.05),
        max_error_interp_mode=vbt.Default("discrete"),
        window=[30, 45, 60, 75, 90]
    )

    print(patsim.wrapper.columns)

    fig = patsim.plot(column=60)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    fig = patsim.overlay_with_heatmap(column=60)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    exits = patsim.similarity >= 0.8
    print(exits.sum())

    patsim = vbt.PATSIM.run(
        price, 
        vbt.Default(pattern),
        error_type=vbt.Default("relative"),
        max_error=vbt.Default(0.05),
        max_error_interp_mode=vbt.Default("discrete"),
        window=[30, 45, 60, 75, 90],
        invert=[False, True],
        min_similarity=[0.7, 0.8],
        param_product=True
    )
    exits = ~patsim.similarity.isnull()
    print(exits.sum())

    groupby = [
        name for name in patsim.wrapper.columns.names 
        if name != "patsim_window"
    ]
    max_sim = patsim.similarity.T.groupby(groupby).max().T
    entries = ~max_sim.xs(True, level="patsim_invert", axis=1).isnull()
    exits = ~max_sim.xs(False, level="patsim_invert", axis=1).isnull()

    fig = h1_data.plot(ohlc_trace_kwargs=dict(opacity=0.5))
    entries[0.8].vbt.signals.plot_as_entries(price, fig=fig)
    exits[0.8].vbt.signals.plot_as_exits(price, fig=fig)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    pattern_range_records = vbt.nb.find_pattern_1d_nb(
        price.values,
        pattern,
        window=30,
        max_window=90,
        error_type=vbt.enums.ErrorType.Relative,
        max_error=np.array([0.05]),
        max_error_interp_mode=vbt.enums.InterpMode.Discrete,
        min_similarity=0.85
    )
    print(pattern_range_records)

    start_row = pattern_range_records[1]["start_idx"]
    end_row = pattern_range_records[1]["end_idx"]
    fig = h1_data.iloc[start_row:end_row + 30].plot(plot_volume=False)
    price.iloc[start_row:end_row].vbt.plot_pattern(
        pattern, 
        error_type="relative",
        max_error=0.05,
        max_error_interp_mode="discrete",
        plot_obj=False, 
        fig=fig
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    pattern_ranges = vbt.PatternRanges.from_pattern_search(
        price,
        pattern,
        window=30,
        max_window=120,
        error_type="relative",
        max_error=0.05,
        max_error_interp_mode="discrete",
        min_similarity=0.85
    )


    pattern_ranges = price.vbt.find_pattern(
        pattern,
        window=30,
        max_window=90,
        error_type="relative",
        max_error=0.05,
        max_error_interp_mode="discrete",
        min_similarity=0.85
    )

    print(pattern_ranges.records_readable)
    print(pattern_ranges.wrapper.columns)
    print(pattern_ranges.search_configs)

    fig = pattern_ranges.plot()
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    print(pattern_ranges.stats())

    pattern_ranges = price.vbt.find_pattern(
        pattern,
        window=30,
        max_window=120,
        error_type="relative",
        max_error=0.05,
        max_error_interp_mode="discrete",
        min_similarity=0.85,
        overlap_mode="allow"
    )

    print(pattern_ranges.count())
    print(pattern_ranges.overlap_coverage)

    fig = pattern_ranges.plot(plot_zones=False, plot_patterns=False)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    def run_prob_search(row_select_prob, window_select_prob):
        return price.vbt.find_pattern(
            pattern,
            window=30,
            max_window=120,
            row_select_prob=row_select_prob,
            window_select_prob=window_select_prob,
            error_type="relative",
            max_error=0.05,
            max_error_interp_mode="discrete",
            min_similarity=0.8,
        )
    
    tempo = timeit.timeit(lambda: run_prob_search(1.0, 1.0), number=1)
    print(f"Tempo de execução: {tempo:.4f} segundos")
    tempo = timeit.timeit(lambda: run_prob_search(0.5, 0.25), number=1)
    print(f"Tempo de execução: {tempo:.4f} segundos")

    print(run_prob_search(1.0, 1.0).count())
    print(run_prob_search(0.5, 0.25).count())

    pd.Series([
        run_prob_search(0.5, 0.25).count() 
        for i in range(100)
    ]).vbt.plot()
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    pattern_ranges = price.vbt.find_pattern(
        vbt.Param([
            [1, 2, 1],
            [2, 1, 2],
            [1, 2, 3],
            [3, 2, 1]
        ]),
        window=30,
        max_window=120,
    )

    print(pattern_ranges.count())

    pattern_ranges = price.vbt.find_pattern(
        vbt.Param([
            [1, 2, 1],
            [2, 1, 2],
            [1, 2, 3],
            [3, 2, 1]
        ], keys=["v-top", "v-bottom", "rising", "falling"]),
        window=30,
        max_window=120,
    )
    print(pattern_ranges.count())

    fig = pattern_ranges.plot(column="falling")
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    pattern_ranges = price.vbt.find_pattern(
        vbt.Param([
            [1, 2, 1],
            [2, 1, 2],
            [1, 2, 3],
            [3, 2, 1]
        ], keys=["v-top", "v-bottom", "rising", "falling"]),
        window=30,
        max_window=120,
        min_similarity=vbt.Param([0.8, 0.85])
    )
    print(pattern_ranges.count())

    fig = pattern_ranges.plot(column=("v-bottom", 0.8))
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    pattern_ranges = price.vbt.find_pattern(
        vbt.Param([
            [1, 2, 1],
            [2, 1, 2],
            [1, 2, 3],
            [3, 2, 1]
        ], keys=["v-top", "v-bottom", "rising", "falling"], level=0),
        window=vbt.Param([30, 30, 7, 7], level=0),
        max_window=vbt.Param([120, 120, 30, 30], level=0),
        min_similarity=vbt.Param([0.8, 0.85], level=1)
    )
    print(pattern_ranges.count())

    mult_data = vbt.DuckDBData.from_duckdb(
        ['EURUSD', 'GBPUSD'], 
        start="2023-01-01", 
        connection=DB_PATH
    )
    mult_data = mult_data.loc["2023-11-13":"2023-11-17"]
    mult_price = mult_data.hlc3

    pattern_ranges = mult_price.vbt.find_pattern(
        search_configs=[
            vbt.PSC(pattern=[1, 2, 3, 2, 3, 2], window=30),
            [
                vbt.PSC(pattern=mult_price.iloc[-30:, 0]),
                vbt.PSC(pattern=mult_price.iloc[-30:, 1]),
            ]
        ],
        min_similarity=0.85
    )
    print(pattern_ranges.count())

    pattern_ranges = mult_price.vbt.find_pattern(
        search_configs=[
            vbt.PSC(pattern=[1, 2, 3, 2, 3, 2], window=30, name="double_top"),
            [
                vbt.PSC(pattern=mult_price.iloc[-30:, 0], name="last"),
                vbt.PSC(pattern=mult_price.iloc[-30:, 1], name="last"),
            ]
        ],
        min_similarity=0.85
    )
    print(pattern_ranges.count())

    pattern_ranges = mult_price.vbt.find_pattern(
        search_configs=[
            vbt.PSC(pattern=[1, 2, 3, 2, 3, 2], window=30, name="double_top"),
            [
                vbt.PSC(pattern=mult_price.iloc[-30:, 0], name="last"),
                vbt.PSC(pattern=mult_price.iloc[-30:, 1], name="last"),
            ]
        ],
        rescale_mode=vbt.Param(["minmax", "rebase"]),
        min_similarity=0.8,
        open=mult_data.open,
        high=mult_data.high,
        low=mult_data.low,
        close=mult_data.close,
    )
    print(pattern_ranges.count())

    fig = pattern_ranges.plot(column=("rebase", "last", "GBPUSD"))
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    mask = pattern_ranges.last_pd_mask
    print(mask.sum())

    pattern_ranges = price.vbt.find_pattern(
        pattern,
        window=30,
        max_window=120,
        row_select_prob=0.5,
        window_select_prob=0.5,
        overlap_mode="allow",
        seed=42
    )
    pr_mask = pattern_ranges.map_field(
        "similarity", 
        idx_arr=pattern_ranges.last_idx.values
    ).to_pd()
    print(pr_mask[~pr_mask.isnull()].sum())

    patsim = vbt.PATSIM.run(
        h1_data.high,
        vbt.Default(pattern),
        window=vbt.Default(30),
        max_window=vbt.Default(120),
        row_select_prob=vbt.Default(0.5),
        window_select_prob=vbt.Default(0.5),
        min_similarity=0.75,
        seed=42
    )
    ind_mask = patsim.similarity
    print(ind_mask[~ind_mask.isnull()].sum())

    price_highs = vbt.PATSIM.run(
        h1_data.high, 
        pattern=np.array([1, 3, 2, 4]), 
        window=40,
        max_window=50
    )
    macd = h1_data.run("talib_macd").macd
    macd_lows = vbt.PATSIM.run(
        macd, 
        pattern=np.array([4, 2, 3, 1]), 
        window=40,
        max_window=50
    )

    fig = vbt.make_subplots(
        rows=3, 
        cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.02
    )
    fig.update_layout(height=500)
    h1_data.high.rename("Price").vbt.plot(
        add_trace_kwargs=dict(row=1, col=1), 
        fig=fig
    )
    macd.rename("MACD").vbt.plot(
        add_trace_kwargs=dict(row=2, col=1), 
        fig=fig
    )
    price_highs.similarity.rename("Price Sim").vbt.plot(
        add_trace_kwargs=dict(row=3, col=1), 
        fig=fig
    )
    macd_lows.similarity.rename("MACD Sim").vbt.plot(
        add_trace_kwargs=dict(row=3, col=1), 
        fig=fig
    )
    fig.show()

    cond1 = (price_highs.similarity >= 0.8).vbt.rolling_any(10)
    cond2 = (macd_lows.similarity >= 0.8).vbt.rolling_any(10)
    exits = cond1 & cond2
    fig = h1_data.plot(ohlc_trace_kwargs=dict(opacity=0.5))
    exits.vbt.signals.plot_as_exits(h1_data.close, fig=fig)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    pattern_ranges = price.vbt.find_pattern(
        [1, 1.0005], 
        window=7, 
        rescale_mode="rebase", 
        max_error=0.01,
        max_error_interp_mode="discrete",
        max_error_strict=True
    )
    print("Número de padrões encontrados:")
    print(pattern_ranges.count())

    range_idxs, raw_projections = vbt.nb.map_ranges_to_projections_nb(
        vbt.to_2d_array(price),
        pattern_ranges.get_field_arr("col"),
        pattern_ranges.get_field_arr("start_idx"),
        pattern_ranges.get_field_arr("end_idx"),
        pattern_ranges.get_field_arr("status")
    )
    print("Índices de intervalo:")
    print(range_idxs)
    print("Projeções brutas:")
    print(raw_projections)

    projections = pattern_ranges.get_projections()
    print("Projeções:")
    print(projections)

    print("Duração:")
    print(pattern_ranges.duration.values)

    projections = pattern_ranges.get_projections(incl_end_idx=False)
    print("Projeções sem índice final:")
    print(projections)

    print("Retorno:")
    print((projections.iloc[-1] / projections.iloc[0] - 1) * 100)

    fig = projections.vbt.plot()
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    delta_ranges = pattern_ranges.with_delta(4)

    fig = pattern_ranges.plot()
    delta_ranges.plot(
        plot_ohlc=False,
        plot_close=False,
        plot_markers=False,
        closed_shape_kwargs=dict(fillcolor="DeepSkyBlue"),
        fig=fig
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    projections = delta_ranges.get_projections()
    print(projections)
    print(np.mean((projections.iloc[-1] / projections.iloc[0] - 1)))

    pattern_ranges = mult_price.vbt.find_pattern(
        [1, 1.0005], 
        window=7, 
        max_window=30,
        rescale_mode="rebase",
        max_error=0.01,
        max_error_interp_mode="discrete",
        max_error_strict=True,
        overlap_mode="allow"
    )

    delta_ranges = pattern_ranges.with_delta(4)
    projections = delta_ranges.get_projections()
    print((projections.iloc[-1] / projections.iloc[0] - 1).describe())

    projections = delta_ranges.get_projections(id_level="end_idx")
    print(projections.columns)


    eurusd_projections = projections.xs("EURUSD", level="symbol", axis=1)
    total_proj_return = (eurusd_projections.iloc[-1] / eurusd_projections.iloc[0]) - 1
    fig = total_proj_return.vbt.scatterplot(
        trace_kwargs=dict(
            marker=dict(
                color=total_proj_return.values,
                colorscale="Temps_r",
                cmid=0
            )
        )
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    eurusd_projections.vbt.plot_projections(plot_bands=False)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    eurusd_projections.vbt.plot_projections(
        plot_bands=False, 
        colorize=np.std
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    projections.xs("GBPUSD", level="symbol", axis=1).median(axis=1)
    print(projections.xs("GBPUSD", level="symbol", axis=1).median(axis=1))
    print(projections.groupby("symbol", axis=1).median())
    print(projections.median(axis=1))

    eurusd_projections.vbt.plot_projections()
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    print(eurusd_projections.iloc[-1].quantile(0.2))
    print(eurusd_projections.iloc[-1].quantile(0.8))

    fig = eurusd_projections.vbt.plot_projections(
        plot_lower=False,
        plot_middle="30%", 
        plot_upper=False, 
        plot_aux_middle=False, 
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    fig = eurusd_projections.iloc[-1].vbt.qqplot()
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    fig = eurusd_projections.vbt.plot_projections(
        plot_lower="P=20%",
        plot_middle="mean", 
        plot_upper="P=80%", 
        plot_aux_middle=False, 
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    def finishes_at_quantile(df, q):
        nth_element = int(np.ceil(q * (df.shape[1] - 1)))
        nth_index = np.argsort(df.iloc[-1].values)[nth_element]
        return df.iloc[:, nth_index]

    fig = eurusd_projections.vbt.plot_projections(
        plot_lower=partial(finishes_at_quantile, q=0.2),
        plot_middle=False, 
        plot_upper=partial(finishes_at_quantile, q=0.8), 
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    crossed_mask = projections.expanding().max().iloc[1] >= 1.05
    filt_projections = projections.loc[:, crossed_mask]
    print(filt_projections.iloc[-1].describe())

    fig = filt_projections.vbt.plot_projections()
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    pattern_ranges = price.vbt.find_pattern(
        pattern=price.iloc[-7:],
        rescale_mode="rebase",
        overlap_mode="allow"
    )
    print(pattern_ranges.count())

    pattern_ranges = pattern_ranges.status_closed
    print(pattern_ranges.count())

    projections = pattern_ranges.get_projections()
    fig = projections.vbt.plot_projections(plot_bands=False)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    delta_ranges = pattern_ranges.with_delta(7)
    projections = delta_ranges.get_projections(start_value=-1)
    fig = h1_data.iloc[-7:].plot(plot_volume=False)
    projections.vbt.plot_projections(fig=fig)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    print(projections.mean(axis=1))

    fig = delta_ranges.plot_projections()
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    windows = np.arange(10, 31)
    window_tuples = combinations(windows, 2)
    window_tuples = filter(lambda x: abs(x[0] - x[1]) >= 5, window_tuples)
    fast_windows, slow_windows = zip(*window_tuples)
    fast_sma = data.run("sma", fast_windows, short_name="fast_sma")
    slow_sma = data.run("sma", slow_windows, short_name="slow_sma")
    entries = fast_sma.real_crossed_above(slow_sma.real)
    exits = fast_sma.real_crossed_below(slow_sma.real)

    print(entries.shape)
    print(exits.shape)

    entry_ranges = entries.vbt.signals.delta_ranges(30, close=data.close)
    entry_ranges = entry_ranges.status_closed
    print(entry_ranges.count().sum())

    exit_ranges = exits.vbt.signals.delta_ranges(30, close=data.close)
    exit_ranges = exit_ranges.status_closed
    print(exit_ranges.count().sum())

    entry_projections = entry_ranges.get_projections()
    print(entry_projections.shape)

    exit_projections = exit_ranges.get_projections()
    print(exit_projections.shape)

    fig = entry_projections.vbt.plot_projections(
        plot_projections=False,
        lower_trace_kwargs=dict(name="Lower (entry)", line_color="green"),
        middle_trace_kwargs=dict(name="Middle (entry)", line_color="green"),
        upper_trace_kwargs=dict(name="Upper (entry)", line_color="green"),
        plot_aux_middle=False,
        plot_fill=False
    )
    fig = exit_projections.vbt.plot_projections(
        plot_projections=False,
        lower_trace_kwargs=dict(name="Lower (exit)", line_color="orangered"),
        middle_trace_kwargs=dict(name="Middle (exit)", line_color="orangered"),
        upper_trace_kwargs=dict(name="Upper (exit)", line_color="orangered"),
        plot_aux_middle=False,
        plot_fill=False,
        fig=fig
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    entry_ranges = entries.vbt.signals.between_ranges(exits, close=data.close)
    entry_ranges = entry_ranges.status_closed
    print(entry_ranges.count().sum())

    exit_ranges = exits.vbt.signals.between_ranges(entries, close=data.close)
    exit_ranges = exit_ranges.status_closed
    print(exit_ranges.count().sum())

    entry_projections = entry_ranges.get_projections()
    print(entry_projections.shape)

    exit_projections = exit_ranges.get_projections()
    print(exit_projections.shape)

    rand_cols = np.random.choice(entry_projections.shape[1], 100)
    fig = entry_projections.iloc[:, rand_cols].vbt.plot_projections(plot_bands=False)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    rand_cols = np.random.choice(exit_projections.shape[1], 100)
    fig = exit_projections.iloc[:, rand_cols].vbt.plot_projections(plot_bands=False)
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    entry_projections = entry_ranges.get_projections(
        proj_period="30d", extend=True
    )
    print(entry_projections.shape)

    exit_projections = exit_ranges.get_projections(
        proj_period="30d", extend=True
    )
    print(exit_projections.shape)

    rand_cols = np.random.choice(entry_projections.shape[1], 100)
    fig = entry_projections.iloc[:, rand_cols].vbt.plot_projections()
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    rand_cols = np.random.choice(exit_projections.shape[1], 100)
    fig = exit_projections.iloc[:, rand_cols].vbt.plot_projections()
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    print(entry_ranges.wrapper.columns)

    fig = entry_ranges.plot_projections(
        column=(25, 30),
        last_n=10,
        proj_period="30d", 
        extend=True,
        plot_lower=False,
        plot_upper=False,
        plot_aux_middle=False,
        projection_trace_kwargs=dict(opacity=0.3)
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    exit_ranges = exits.vbt.signals.between_ranges(
        entries, 
        incl_open=True, 
        close=data.close
    )
    print(exit_ranges.count().sum())

    print(exit_ranges.wrapper.columns[exit_ranges.status_open.col_arr])

    fig = exit_ranges.status_closed.plot_projections(
        column=(20, 30), plot_bands=False
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    exit_ranges.plot_projections(
        column=(20, 30), plot_bands=False
    )
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()

    column = (20, 30)
    signal_index = data.wrapper.index[np.flatnonzero(exits[column])[-1]]
    plot_start_index = signal_index - pd.Timedelta(days=10)
    sub_close = data.close[plot_start_index:]
    sub_exits = exits.loc[plot_start_index:, column]

    # Criar o gráfico base
    fig = sub_close.vbt.plot()

    # Adicionar os sinais de saída
    sub_exits.vbt.signals.plot_as_exits(sub_close, fig=fig)

    # Obter e plotar as projeções
    projections = exit_ranges[column].status_closed.get_projections(
        start_value=sub_close.loc[signal_index],
        start_index=signal_index
    )
    projections.vbt.plot_projections(plot_bands=False, fig=fig)

    # Configurar e mostrar o gráfico
    fig.update_layout(
        width=width,
        height=height
    )
    fig.show()