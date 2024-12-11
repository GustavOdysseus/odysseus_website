from analise_questoes import QuestionAnalyzer

def test_timing():
    analyzer = QuestionAnalyzer()
    
    # Testa com o primeiro PDF
    pdf_path = "/Users/gustavomonteiro/Desktop/prova/Simulado_port_1.pdf"
    
    # Extrai texto e separa questões
    text = analyzer.extract_text_from_pdf(pdf_path)
    questions = analyzer.split_into_questions(text)
    
    # Analisa as primeiras 5 questões para teste
    results = []
    for question in questions[:5]:
        result = analyzer.analyze_question(question)
        if result:
            results.append(result)
    
    # Gera visualizações
    analyzer.generate_visualizations(results)

if __name__ == "__main__":
    test_timing()
