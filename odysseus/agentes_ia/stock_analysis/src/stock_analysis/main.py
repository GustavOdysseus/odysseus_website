import warnings
import logging
import sys
from crew import StockAnalysisCrew

# Suprimir avisos específicos do ChromaDB
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger("chromadb").setLevel(logging.ERROR)

def run():
    inputs = {
        'query': 'Qual empresa você quer analisar?',
        'company_stock': 'IBIT',
    }
    return StockAnalysisCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Treina a equipe por um determinado número de iterações.
    """
    inputs = {
        'query': 'Qual foi a receita do ano passado?',
        'company_stock': 'IBIT',
    }
    try:
        StockAnalysisCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"Ocorreu um erro durante o treinamento da equipe: {e}")
    
if __name__ == "__main__":
    print("## Bem-vindo à Equipe de Análise de Ações")
    print('-------------------------------')
    result = run()
    print("\n\n########################")
    print("## Aqui está o Relatório")
    print("########################\n")
    print(result)
