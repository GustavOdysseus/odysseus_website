import os
from analise_questoes import QuestionAnalyzer
from datetime import datetime
import pandas as pd
import json
from tqdm import tqdm
import time

class BatchProcessor:
    def __init__(self, pdf_dir, output_dir="resultados"):
        self.pdf_dir = pdf_dir
        self.output_dir = output_dir
        self.analyzer = QuestionAnalyzer()
        
        # Cria diretório de resultados se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        # Configura log de erros e progresso
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(output_dir, f"error_log_{timestamp}.txt")
        self.progress_file = os.path.join(output_dir, f"progress_log_{timestamp}.txt")
        
    def log_progress(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.progress_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[{timestamp}] {message}")
        
    def log_error(self, pdf_file: str, question_id: str, error: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] PDF: {pdf_file}, Questão {question_id}: {error}\n")
        print(f"[ERRO] PDF: {pdf_file}, Questão {question_id}: {error}")
    
    def save_partial_results(self, results: list, batch_number: int):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = os.path.join(self.output_dir, f"resultados_batch_{batch_number}_{timestamp}")
        
        # Salva em formato legível
        with open(f"{base_filename}.txt", "w", encoding='utf-8') as f:
            f.write(f"=== Análise de Questões ===\n")
            f.write(f"Total de questões analisadas: {len(results)}\n\n")
            
            for i, result in enumerate(results, 1):
                f.write(f"\n{'='*50}\n")
                f.write(f"Questão {i}\n")
                f.write(f"{'='*50}\n\n")
                f.write(f"Categoria Principal: {result['categoria_principal']}\n")
                f.write(f"Subtema Específico: {result['subtema_especifico']}\n")
                f.write(f"Nível de Dificuldade: {result['dificuldade']}\n")
                f.write(f"Justificativa: {result['justificativa_dificuldade']}\n\n")
                f.write("Principais Armadilhas:\n")
                for armadilha in result['armadilhas']:
                    f.write(f"• {armadilha}\n")
                f.write(f"\nResumo Analítico:\n{result['resumo_analitico']}\n")
        
        # Mantém os outros formatos como backup
        df = pd.DataFrame(results)
        df.to_csv(f"{base_filename}.csv", index=False)
        with open(f"{base_filename}.json", "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        self.log_progress(f"Resultados salvos em: {base_filename}")
    
    def process_pdf(self, pdf_path: str) -> list:
        pdf_name = os.path.basename(pdf_path)
        self.log_progress(f"Iniciando processamento de {pdf_name}")
        
        try:
            # Fase 1: Extração do texto
            start_time = time.time()
            self.log_progress("Fase 1: Extraindo texto do PDF...")
            text = self.analyzer.extract_text_from_pdf(pdf_path)
            extraction_time = time.time() - start_time
            self.log_progress(f"Texto extraído em {extraction_time:.2f} segundos")
            
            # Fase 2: Separação em questões
            start_time = time.time()
            self.log_progress("Fase 2: Separando questões...")
            questions = self.analyzer.split_into_questions(text)
            split_time = time.time() - start_time
            self.log_progress(f"Encontradas {len(questions)} questões em {split_time:.2f} segundos")
            
            results = []
            total = len(questions)
            
            # Fase 3: Análise das questões
            self.log_progress("Fase 3: Iniciando análise das questões...")
            analysis_start = time.time()
            
            for i, question in enumerate(tqdm(questions, desc=f"Analisando questões de {pdf_name}")):
                question_start = time.time()
                try:
                    result = self.analyzer.analyze_question(question)
                    if result:
                        results.append(result)
                        question_time = time.time() - question_start
                        self.log_progress(f"Questão {i+1}/{total} analisada em {question_time:.2f} segundos")
                        
                        # Salva a cada 10 questões
                        if (i + 1) % 10 == 0:
                            self.save_partial_results(results, f"{pdf_name}_{i+1}")
                            avg_time = (time.time() - analysis_start) / (i + 1)
                            eta = avg_time * (total - (i + 1))
                            self.log_progress(f"Progresso: {i+1}/{total} questões. Tempo médio por questão: {avg_time:.2f}s. ETA: {eta:.2f}s")
                            
                except Exception as e:
                    self.log_error(pdf_name, question['id'], str(e))
                    continue
            
            total_time = time.time() - analysis_start
            self.log_progress(f"Análise de {pdf_name} concluída em {total_time:.2f} segundos")
            return results
            
        except Exception as e:
            self.log_error(pdf_name, "PDF_EXTRACTION", str(e))
            return []
    
    def process_all_pdfs(self):
        all_results = []
        start_time = time.time()
        
        # Lista todos os PDFs no diretório
        pdf_files = [f for f in os.listdir(self.pdf_dir) if f.lower().endswith('.pdf')]
        self.log_progress(f"Encontrados {len(pdf_files)} arquivos PDF")
        
        # Processa cada PDF
        for i, pdf_file in enumerate(pdf_files, 1):
            pdf_path = os.path.join(self.pdf_dir, pdf_file)
            self.log_progress(f"\nProcessando PDF {i}/{len(pdf_files)}: {pdf_file}")
            
            results = self.process_pdf(pdf_path)
            all_results.extend(results)
            
            # Salva resultados deste PDF
            self.save_partial_results(results, f"completo_{pdf_file}")
        
        # Salva todos os resultados juntos
        self.save_partial_results(all_results, "todos_resultados")
        
        total_time = time.time() - start_time
        self.log_progress(f"\nProcessamento completo finalizado em {total_time:.2f} segundos")
        return all_results

def main():
    pdf_dir = "/Users/gustavomonteiro/Desktop/prova"
    processor = BatchProcessor(pdf_dir)
    
    processor.log_progress("=== Iniciando processamento de todos os PDFs ===")
    results = processor.process_all_pdfs()
    
    processor.log_progress("\n=== Processamento concluído! ===")
    processor.log_progress(f"Total de questões analisadas: {len(results)}")
    processor.log_progress(f"Verifique a pasta 'resultados' para ver os arquivos gerados")
    processor.log_progress(f"Verifique os arquivos de log para ver o progresso e possíveis erros")

if __name__ == "__main__":
    main()
