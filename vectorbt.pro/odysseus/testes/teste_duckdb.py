import vectorbtpro as vbt
import duckdb

# Configurações
DB_PATH = "forex_market.duckdb"

def check_data(symbol):
    """Verifica os dados do símbolo no DuckDB usando o método from_duckdb"""
    try:
        print(f"\nVerificando dados inseridos para o símbolo: {symbol}")
        
        # Carregar os dados do DuckDB para o símbolo
        duckdb_data = vbt.DuckDBData.from_duckdb(symbol, connection=DB_PATH)
        
        # Exibir os primeiros registros
        print(f"\nPrimeiros registros de {symbol}:")
        print(duckdb_data.get().head())

        # Verificar informações do DataFrame
        print(f"\nInformações gerais dos dados de {symbol}:")
        print(duckdb_data.get().info())

        # Verificar as colunas e o índice
        print(f"\nColunas dos dados de {symbol}: {duckdb_data.get().columns}")
        print(f"Índice dos dados de {symbol}: {duckdb_data.get().index}")

        # Exibir as últimas 5 linhas para verificar o final da série de dados
        print(f"\nÚltimos registros de {symbol}:")
        print(duckdb_data.get().tail())

    except Exception as e:
        print(f"Erro ao consultar a tabela {symbol} no DuckDB. Detalhes: {e}")

def main():
    # Lista dos símbolos a serem verificados
    symbols = ["AUDCAD", "EURUSD", "GBPUSD", "BCOUSD"]  # Adicione os símbolos que desejar verificar
    
    # Verificar os dados de cada símbolo
    for symbol in symbols:
        check_data(symbol)
        # Carregar os dados do DuckDB (usando o símbolo AUDCAD, por exemplo)
        data = vbt.DuckDBData.from_duckdb("AUDCAD", connection="forex_market.duckdb")

        # Plotar o gráfico OHLC
        fig = data.plot(column=["Open", "High", "Low", "Close"], trace_names=["Open", "High", "Low", "Close"])
        fig.show()

if __name__ == "__main__":
    main()
