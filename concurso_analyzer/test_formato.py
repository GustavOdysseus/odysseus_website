from analise_questoes import QuestionAnalyzer

# Questões de teste com diferentes tipos de armadilhas
questoes_teste = [
    {
        'id': '1',
        'content': """
        Leia o texto:
        
        "A inflação do mês de junho ficou em 0,5%, segundo dados do IBGE. O índice foi puxado principalmente pela alta dos alimentos, que subiram 1,2%. 
        Por outro lado, os preços dos combustíveis caíram 2,3%, ajudando a segurar o índice geral."
        
        Sobre o texto, é correto afirmar que:
        a) A inflação subiu principalmente devido aos combustíveis
        b) Os alimentos foram o principal fator de alta no mês
        c) O índice geral ficou em 1,2% no mês de junho
        d) Houve queda generalizada nos preços
        """
    },
    {
        'id': '2',
        'content': '''
        Leia o poema:
        
        "Amor é fogo que arde sem se ver;
        É ferida que dói e não se sente;
        É um contentamento descontente;
        É dor que desatina sem doer."
        
        O poema acima apresenta:
        a) Apenas metáforas sobre o amor
        b) Somente comparações diretas
        c) Paradoxos para definir o amor
        d) Descrições literais do sentimento
        '''
    },
    {
        'id': '3',
        'content': '''
        Analise o gráfico de vendas da empresa XYZ:
        
        2020: 100 unidades
        2021: 150 unidades
        2022: 225 unidades
        
        Com base nos dados apresentados, pode-se afirmar que:
        a) O crescimento foi linear ao longo dos anos
        b) Houve um aumento de 50% a cada ano
        c) O maior crescimento ocorreu entre 2021 e 2022
        d) As vendas triplicaram em dois anos
        '''
    }
]

def test_novo_formato():
    analyzer = QuestionAnalyzer()
    
    print("Testando novo formato de análise...")
    for questao in questoes_teste:
        resultado = analyzer.analyze_question(questao)
        print(f"\nAnálise da Questão {questao['id']}:")
        print("="*50)
        print(f"Categoria Principal: {resultado['categoria_principal']}")
        print(f"Subtema Específico: {resultado['subtema_especifico']}")
        print(f"Nível de Dificuldade: {resultado['dificuldade']}")
        print(f"Justificativa: {resultado['justificativa_dificuldade']}")
        print("\nPrincipais Armadilhas:")
        for armadilha in resultado['armadilhas']:
            print(f"• {armadilha}")
        print("\nResumo Analítico:")
        print(resultado['resumo_analitico'])
        print("="*50)

if __name__ == "__main__":
    test_novo_formato()
