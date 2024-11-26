import vectorbtpro as vbt
import time
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

if __name__ == "__main__":
    start_time = time.time()
    DB_PATH = "../forex_market.duckdb"
    symbol = "EURUSD"
    data = vbt.DuckDBData.from_duckdb(symbol, start="2013-01-01", connection=DB_PATH)
    close = data.close
    descricao_serie = close.describe()
    print(descricao_serie)

    # Análise anual
    descricao_anual = []
    for ano in range(2013, 2024):
        data_ano = close.loc[f"{ano}"]
        descricao_ano = data_ano.describe()
        descricao_anual.append(descricao_ano)
    print(descricao_anual)

    # Análise semanal
    freq = "w"
    weekly = data.close.vbt.resample_apply(freq, vbt.nb.last_reduce_nb)
    max_weekly = data.high.vbt.resample_apply(freq, vbt.nb.max_reduce_nb)
    min_weekly = data.low.vbt.resample_apply(freq, vbt.nb.min_reduce_nb)
    # Obter o índice de datas do resample para converter o array em uma série
    weekly_dates = data.close.vbt.resample_apply(freq, vbt.nb.last_reduce_nb).index
    # Calcular desvio padrão e amplitude
    weekly_std = weekly.std()
    weekly_range = max_weekly - min_weekly

    # Calcular a razão desvio padrão/amplitude
    weekly_ratio = (weekly_std / weekly_range)
    # Converter para uma série Pandas para usar métodos como .dropna() e .plot()
    weekly_ratio_df = pd.DataFrame(weekly_ratio, index=weekly_dates, columns=['Razão']).dropna()
    print('Razão entre Desvio Padrão e Amplitude (Semanal)')
    print(weekly_ratio_df)

    # Visualizar a série temporal dessa razão
    # Plot para visualizar
    ax = weekly_ratio_df.plot(title='Razão entre Desvio Padrão e Amplitude (Semanal)')
    plt.xlabel('Data')
    plt.ylabel('Razão (Desvio Padrão / Amplitude)')
    plt.grid(True)
    plt.show()

    # Agrupar usando vbt.Grouper para criar grupos automaticamente
    group_labels = pd.qcut(weekly_ratio, q=6, labels=False)  # Dividir em 3 grupos
    grouper = vbt.Grouper(index=weekly_ratio.index, group_by=group_labels)

    # Verificar a distribuição dos grupos
    group_counts = grouper.get_index().value_counts().sort_index()
    print("Distribuição dos grupos:")
    print(group_counts)

    # Plotar a distribuição dos grupos
    group_counts.plot(kind='bar', title='Distribuição dos Grupos de Semanas')
    plt.xlabel('Grupo')
    plt.ylabel('Número de Semanas')
    plt.grid(True)
    plt.show()

    # Visualizar os grupos em um gráfico de dispersão
    plt.figure(figsize=(14, 7))
    sns.set_theme(style="whitegrid")

    plot_data = pd.DataFrame({
        'Date': weekly_ratio.index,
        'Ratio': weekly_ratio,
        'Cluster': group_labels
    })

    sns.scatterplot(
        data=plot_data,
        x='Date',
        y='Ratio',
        hue='Cluster',
        palette='viridis',
        s=100
    )

    plt.title('Agrupamento de Semanas por Razão de Desvio Padrão/Amplitude')
    plt.xlabel('Data')
    plt.ylabel('Razão (Desvio Padrão / Amplitude)')
    plt.legend(title='Cluster')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print(f"Tempo total de execução: {time.time() - start_time:.2f} segundos")