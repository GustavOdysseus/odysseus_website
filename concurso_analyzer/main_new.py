from crew_new import ConcursoAnalyzer
import os
import spacy
from dotenv import load_dotenv

def main():
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar se a API key está configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("\nErro: OPENAI_API_KEY não encontrada!")
        print("Por favor, configure sua API key no arquivo .env")
        return
    
 
    
    # Inicializar o analisador
    analyzer = ConcursoAnalyzer()
    
    # Diretório onde estão os PDFs das provas
    pdf_directory = "/Users/gustavomonteiro/Desktop/prova/"
    
    # Criar diretório se não existir
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)
    
    # Listar todos os PDFs no diretório
    pdf_paths = []
    for file in os.listdir(pdf_directory):
        if file.endswith(".pdf"):
            pdf_paths.append(os.path.join(pdf_directory, file))
    
    if not pdf_paths:
        print("\nNenhum arquivo PDF encontrado na pasta 'provas/'")
        print("Por favor, adicione seus arquivos PDF de provas nesta pasta.")
        return
    
    print(f"\nAnalisando {len(pdf_paths)} arquivos de prova...")
    
    # Executar a análise
    result = analyzer.analyze_exams(pdf_paths)
    
    # Imprimir resultados
    print("\nResultados da Análise:")
    print("----------------------")
    print(result)

if __name__ == "__main__":
    main()
