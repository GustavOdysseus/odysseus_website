import duckdb
import vectorbtpro as vbt
import os
import json
import pandas as pd

# Configurações
CSV_DIR = r'D:\Caleb\caleb\Python\mercado\mercado\reinaldo\FOREX\simbolos'
DB_PATH = "forex_market.duckdb"

def load_categories():
    """Carrega categorias do JSON"""
    with open("symbol_categories.json", "r") as f:
        return json.load(f)

def import_data(con, categories):
    """Importa dados dos CSVs para o DuckDB usando CSVData do vectorbt"""
    
    for symbol in categories.keys():
        file_path = os.path.join(CSV_DIR, f"{symbol.lower()}_1m.csv")
        
        print(f"\nIniciando o processamento do símbolo: {symbol}")
        print(f"Localização do arquivo CSV: {file_path}")
        
        try:
            # Tentativa de leitura do arquivo CSV
            print(f"Tentando carregar o arquivo CSV para {symbol}...")
            csv_data = vbt.CSVData.from_csv(paths=file_path)
            #csv_data = pd.read_csv(file_path, index_col=0, parse_dates=True)
            print(f"Arquivo CSV carregado com sucesso para {symbol}!")
            
            
            # Tentativa de inserção dos dados no DuckDB
            print(f"Tentando inserir os dados no DuckDB na tabela '{symbol}'...")
            csv_data.to_duckdb(DB_PATH, table=symbol, if_exists='append')
            print(f"Dados inseridos com sucesso no DuckDB para o símbolo {symbol}!")
            
        except Exception as e:
            print(f"Erro ao processar o símbolo {symbol}. Detalhes do erro: {e}")
            continue

def main():
    print("Iniciando o processo de importação de dados...")
    
    # Tentativa de conexão com o banco de dados
    try:
        con = duckdb.connect(DB_PATH)
        print(f"Conectado ao banco de dados DuckDB em {DB_PATH}")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados DuckDB. Detalhes: {e}")
        return
    
    # Carregar categorias para processar os arquivos CSV
    try:
        categories = load_categories()
        print(f"Categorias carregadas com sucesso do arquivo JSON. Total de {len(categories)} símbolos.")
    except Exception as e:
        print(f"Erro ao carregar categorias do arquivo JSON. Detalhes: {e}")
        return
    
    # Importar dados dos arquivos CSV usando VectorBT
    try:
        import_data(con, categories)
    except Exception as e:
        print(f"Erro durante a importação dos dados dos arquivos CSV. Detalhes: {e}")
    
    # Tentativa de consultar dados do DuckDB
    try:
        print("\nConsultando dados do símbolo EURUSD no banco de dados DuckDB...")
        duckdb_data = vbt.DuckDBData.from_duckdb("EURUSD", connection=DB_PATH)
        print("Consulta realizada com sucesso!")
        print("\nPrimeiros registros do EURUSD:")
        print(duckdb_data.get().head())
    except Exception as e:
        print(f"Erro ao consultar os dados do símbolo EURUSD. Detalhes: {e}")
    
    # Fechar conexão com o banco de dados
    try:
        con.close()
        print("Conexão com o banco de dados DuckDB encerrada com sucesso.")
    except Exception as e:
        print(f"Erro ao encerrar a conexão com o banco de dados DuckDB. Detalhes: {e}")

if __name__ == "__main__":
    main()
