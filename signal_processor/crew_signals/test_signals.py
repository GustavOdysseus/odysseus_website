from signals_crew import CrewSignals

def test_signal_generation():
    # Instancia a crew de sinais
    crew_signals = CrewSignals()
    
    # Define os inputs para a tarefa
    inputs = {
        "task_description": """
        Gerar sinais de trading com as seguintes características:
        1. Usar RSI (Relative Strength Index) com período de 14
        2. Usar Moving Average (MA) de 20 períodos
        3. Gerar sinais de compra quando:
           - RSI < 30 (sobrevenda) E
           - Preço cruza acima da MA
        4. Gerar sinais de venda quando:
           - RSI > 70 (sobrecompra) E
           - Preço cruza abaixo da MA
        """,
        "task_output": "Lista de sinais otimizados com seus respectivos parâmetros e métricas de performance",
        "task_name": "rsi_ma_crossover_strategy"
    }
    
    # Executa a crew com os inputs definidos
    result = crew_signals.crew().kickoff(inputs=inputs)
    
    # Imprime o resultado
    print("\nResultado da execução:")
    print("=" * 50)
    print(result)
    
if __name__ == "__main__":
    print("Iniciando teste de geração de sinais...")
    test_signal_generation()
