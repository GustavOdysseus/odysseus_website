import os
import glob

def get_symbols_from_csvs(directory):
    # Obter lista de arquivos CSV
    csv_files = glob.glob(os.path.join(directory, '*_1m.csv'))
    
    # Extrair símbolos dos nomes dos arquivos
    symbols = []
    for file in csv_files:
        # Pegar só o nome do arquivo sem o caminho
        filename = os.path.basename(file)
        # Remover '_1m.csv' e converter para maiúsculo
        symbol = filename.replace('_1m.csv', '').upper()
        symbols.append(symbol)
    
    # Ordenar alfabeticamente
    symbols.sort()
    
    return symbols

# Usar a função
directory = r'D:\Caleb\caleb\Python\mercado\mercado\reinaldo\FOREX\simbolos'
symbols = get_symbols_from_csvs(directory)

# Imprimir os símbolos encontrados
print("Símbolos encontrados:")
for symbol in symbols:
    print(f"- {symbol}")

print(f"\nTotal de símbolos: {len(symbols)}")


