import vectorbtpro as vbt
from screeninfo import get_monitors
import numpy as np
import pandas as pd
from functools import partial
from itertools import combinations
import timeit

class Config:
    """
    Centraliza todas as configurações do sistema de análise de padrões.
    
    Esta classe segue o princípio de configuração centralizada, permitindo
    ajuste fácil de parâmetros sem necessidade de modificar o código-fonte.
    
    Atributos:
        db_config (dict): Configurações de conexão e seleção de dados
            path (str): Caminho para o banco de dados DuckDB
            symbols (list): Lista de símbolos para análise multi-ativos
            default_symbol (str): Símbolo padrão para análise single-asset
            start_date (str): Data inicial da análise
            end_date (str): Data final da análise
            
        plot_config (dict): Configurações visuais dos gráficos
            monitor_width_ratio (float): Proporção da largura do monitor (0-1)
            monitor_height_ratio (float): Proporção da altura do monitor (0-1)
            theme (str): Tema do gráfico ('dark' ou 'light')
            
        pattern_config (dict): Configurações do padrão base
            default_pattern (np.array): Sequência numérica que define o padrão
            resize_n (int): Número de pontos após redimensionamento
            resize_mode (vbt.enums.InterpMode): Modo de interpolação
            
        pattern_search_config (dict): Parâmetros para busca de padrões
            window (int): Tamanho da janela de busca
            max_window (int): Tamanho máximo da janela
            error_type (str): Tipo de erro ('relative' ou 'absolute')
            max_error (float): Erro máximo permitido
            max_error_interp_mode (str): Modo de interpolação do erro
            min_similarity (float): Similaridade mínima aceitável
            
        pattern_plot_config (dict): Configurações visuais dos padrões
            interp_mode (str): Modo de interpolação para visualização
            rescale_mode (str): Modo de reescala do padrão
            fill_distance (bool): Preencher área entre padrão e preço
            
        projection_config (dict): Configurações de projeção
            period (str): Período para projeção
            extend (bool): Extender projeções
            quantiles (list): Quantis para plotagem de bandas
            plot_bands (bool): Plotar bandas
            
        multi_asset_config (dict): Configurações de análise multi-ativos
            min_window_diff (int): Diferença mínima de janela
            default_patterns (dict): Padrões default para diferentes ativos
            
        indicator_config (dict): Configurações de indicadores
            macd (dict): Configurações do MACD
                fast_period (int): Período rápido
                slow_period (int): Período lento
                signal_period (int): Período do sinal
            sma (dict): Configurações da média móvel
                min_window (int): Período mínimo
                max_window (int): Período máximo
                fast_ratio (float): Proporção para janela rápida
                slow_ratio (float): Proporção para janela lenta
    """
    def __init__(self):
        # Configurações de Dados
        self.db_config = {
            'path': "../forex_market.duckdb",
            'symbols': ["AUDUSD", "GBPUSD", "EURUSD"],  # Lista de símbolos disponíveis
            'default_symbol': "EURUSD",        # Símbolo padrão
            'start_date': "2023-04-03",
            'end_date': "2023-04-07"
        }
        
        # Configurações de Plot
        self.plot_config = {
            'monitor_width_ratio': 0.8,
            'monitor_height_ratio': 0.8,
            'theme': 'dark'
        }
        
        # Configurações de Padrão
        self.pattern_config = {
            'default_pattern': np.array([2, 1, 2, 3, 4]),
            'resize_n': 10,
            'resize_mode': vbt.enums.InterpMode.Linear
        }
        
        # Configurações de Busca de Padrões
        self.pattern_search_config = {
            'window': 5,
            'max_window': 90,
            'error_type': "relative",
            'max_error': 0.005,
            'max_error_interp_mode': "discrete",
            'min_similarity': 0.85
        }
        
        # Configurações de Plot de Padrões
        self.pattern_plot_config = {
            'interp_mode': "nearest",
            'rescale_mode': "rebase",
            'fill_distance': True
        }
        
        # Configurações de projeção
        self.projection_config = {
            'period': 30,
            'extend': True,
            'quantiles': [0.2, 0.8],
            'plot_bands': False
        }
        
        # Configurações de análise multi-ativos
        self.multi_asset_config = {
            'min_window_diff': 5,
            'default_patterns': {
                'v-top': [1, 2, 1],
                'v-bottom': [2, 1, 2],
                'rising': [1, 2, 3],
                'falling': [3, 2, 1]
            }
        }
        
        # Configurações de indicadores
        self.indicator_config = {
            'macd': {
                'fast_period': 12,
                'slow_period': 26,
                'signal_period': 9
            },
            'sma': {
                'min_window': 10,
                'max_window': 30,
                'min_window_diff': 5  # Diferença mínima entre janelas rápida e lenta
            }
        }

        # Controle de execução de análises e gráficos
        self.execution_config = {
            'analysis': {
                'pattern_resize': False,      # Redimensionamento de padrões
                'pattern_similarity': False,   # Análise de similaridade
                'pattern_search': False,      # Busca de padrões
                'macd_analysis': False,      # Análise MACD
                'sma_crossover': True,      # Análise de cruzamento de médias
                'multi_asset': False,        # Análise multi-ativos
                'projections': True         # Análise de projeções
            },
            'plots': {
                'resized_pattern': False,     # Plot do padrão redimensionado
                'pattern_matches': False,     # Plot dos padrões encontrados
                'macd_patterns': False,      # Plot dos padrões no MACD
                'sma_crossovers': False,     # Plot dos cruzamentos de médias
                'projections': True,        # Plot das projeções
                'quantile_bands': False      # Plot das bandas de quantis
            }
        }

class DataHandler:
    """
    Gerencia o carregamento e manipulação dos dados financeiros.
    
    Esta classe é responsável por carregar dados do DuckDB e
    disponibilizá-los no formato adequado para análise, suportando
    tanto análise single-asset quanto multi-asset.
    
    Args:
        config (Config): Instância de configuração com parâmetros de dados
        
    Atributos:
        config (Config): Configurações do sistema
        data_original (vbt.DuckDBData): Dados brutos do banco
        data (pd.DataFrame): Dados filtrados pelo período selecionado
    """
    def __init__(self, config):
        self.config = config
        self.data_original = None
        self.data = None
        self.load_data()
    
    def load_data(self, symbols=None):
        """
        Carrega dados para um ou múltiplos ativos.
        
        Args:
            symbols (str|list, optional): Símbolo único ou lista de símbolos.
                Se None, usa o símbolo padrão da configuração.
        """
        symbols = symbols or self.config.db_config['default_symbol']
        self.data_original = vbt.DuckDBData.from_duckdb(
            symbols,
            start=self.config.db_config['start_date'],
            connection=self.config.db_config['path']
        )
        self.data = self.data_original.loc[
            self.config.db_config['start_date']:
            self.config.db_config['end_date']
        ]
    
    def get_data(self, symbols=None):
        """
        Retorna os dados processados para análise.
        
        Args:
            symbols (str|list, optional): Símbolo único ou lista de símbolos
                para retornar dados específicos.
                
        Returns:
            pd.DataFrame: DataFrame com dados OHLCV do período selecionado
        """
        if symbols and symbols != self.config.db_config['default_symbol']:
            self.load_data(symbols)
        return self.data
    
    def find_patterns_across_assets(self, patterns, windows):
        """
        Busca padrões em múltiplos ativos.
        
        Args:
            patterns (list): Lista de padrões para busca
            windows (list): Lista de tamanhos de janela
            
        Returns:
            vbt.Ranges: Ranges com padrões encontrados
        """
        multi_data = self.get_data(self.config.db_config['symbols'])
        return multi_data.hlc3.vbt.find_pattern(
            search_configs=[
                vbt.PSC(pattern=p, window=w)
                for p, w in zip(patterns, windows)
            ],
            min_similarity=self.config.pattern_search_config['min_similarity']
        )

class PlotSettings:
    """
    Gerencia as configurações visuais dos gráficos.
    
    Adapta as dimensões dos gráficos com base no tamanho do monitor
    e nas proporções definidas na configuração.
    
    Args:
        config (Config): Instância de configuração com parâmetros visuais
        
    Atributos:
        width (int): Largura calculada do gráfico em pixels
        height (int): Altura calculada do gráfico em pixels
    """
    def __init__(self, config):
        monitor = get_monitors()[0]
        self.width = int(monitor.width * config.plot_config['monitor_width_ratio'])
        self.height = int(monitor.height * config.plot_config['monitor_height_ratio'])

    def apply(self, fig):
        """
        Aplica as configurações visuais ao gráfico.
        
        Args:
            fig (go.Figure): Objeto de figura do Plotly
        """
        fig.update_layout(width=self.width, height=self.height)
        fig.show()

class PatternResizer:
    """
    Responsável pelo redimensionamento de padrões.
    
    Implementa diferentes métodos de interpolação para ajustar
    o tamanho dos padrões mantendo suas características essenciais.
    
    Args:
        pattern (np.array): Padrão numérico a ser redimensionado
        config (Config): Instância de configuração
        
    Métodos empíricos:
        - Utiliza interpolação linear para preservar tendências
        - Mantém pontos críticos (máximos e mínimos) do padrão
        - Permite ajuste fino através de diferentes modos de interpolação
    """
    def __init__(self, pattern, config):
        self.pattern = pattern
        self.config = config

    def resize(self, n=None, mode=None):
        """
        Redimensiona o padrão para um novo tamanho.
        
        Args:
            n (int, optional): Número de pontos desejado
            mode (vbt.enums.InterpMode, optional): Modo de interpolação
            
        Returns:
            np.array: Padrão redimensionado
        """
        n = n or self.config.pattern_config['resize_n']
        mode = mode or self.config.pattern_config['resize_mode']
        return vbt.nb.interp_resize_1d_nb(self.pattern, n, mode)

    def plot_resized(self, plot_settings, n=None, mode=None):
        resized_pattern = self.resize(n, mode)
        fig = pd.Series(resized_pattern).vbt.plot()
        plot_settings.apply(fig)

class PatternAnalyzer:
    """
    Analisa a similaridade entre padrões e séries temporais de preços.
    
    Esta classe implementa métodos para quantificar e visualizar o grau
    de similaridade entre um padrão de referência e os dados de preço.
    
    Args:
        data (pd.Series): Série temporal de preços para análise
        pattern (np.array): Padrão de referência para comparação
        config (Config): Instância de configuração
        
    Métodos empíricos:
        - Calcula distâncias absolutas entre padrão e preços
        - Normaliza as distâncias pelo range máximo possível
        - Converte distâncias em medida de similaridade (0-1)
    """
    def __init__(self, data, pattern, config):
        self.data = data
        self.pattern = pattern
        self.config = config

    def calculate_similarity(self, rescaled_pattern):
        """
        Calcula o índice de similaridade entre o padrão e os dados.
        
        Utiliza a métrica MAE (Mean Absolute Error) normalizada para
        quantificar a similaridade entre as séries temporais.
        
        Args:
            rescaled_pattern (np.array): Padrão redimensionado para comparação
            
        Returns:
            float: Índice de similaridade entre 0 (diferente) e 1 (idêntico)
        """
        abs_distances = np.abs(rescaled_pattern - self.data.values)
        mae = abs_distances.sum()
        max_abs_distances = np.column_stack((
            (self.data.max() - rescaled_pattern), 
            (rescaled_pattern - self.data.min())
        )).max(axis=1)
        max_mae = max_abs_distances.sum()
        return 1 - mae / max_mae

    def plot_pattern(self, pattern, plot_settings):
        """
        Visualiza o padrão sobreposto aos dados de preço.
        
        Cria um gráfico interativo mostrando a comparação visual
        entre o padrão e os dados reais.
        
        Args:
            pattern (np.array): Padrão a ser visualizado
            plot_settings (PlotSettings): Configurações de visualização
        """
        fig = self.data.vbt.plot_pattern(
            pattern,
            interp_mode=self.config.pattern_plot_config['interp_mode'],
            rescale_mode=self.config.pattern_plot_config['rescale_mode'],
            fill_distance=self.config.pattern_plot_config['fill_distance']
        )
        fig.show()

class PatternSearcher:
    """
    Busca ocorrências de padrões em séries temporais de preços.
    
    Implementa algoritmos de busca de padrões similares em dados
    históricos, permitindo identificar repetições e tendências.
    
    Args:
        price (pd.Series): Série temporal de preços para busca
        pattern (np.array): Padrão a ser procurado
        config (Config): Instância de configuração
        
    Métodos empíricos:
        - Utiliza janela deslizante para busca de padrões
        - Aplica métricas de similaridade configuráveis
        - Permite ajuste de tolerância a variações
    """
    def __init__(self, price, pattern, config):
        self.price = price
        self.pattern = pattern
        self.config = config

    def find_patterns(self):
        """
        Localiza todas as ocorrências do padrão nos dados.
        
        Utiliza os parâmetros configurados para buscar padrões
        similares ao padrão de referência na série temporal.
        
        Returns:
            vbt.Ranges: Objeto contendo os intervalos onde padrões foram encontrados
        """
        return self.price.vbt.find_pattern(
            self.pattern,
            window=self.config.pattern_search_config['window'],
            max_window=self.config.pattern_search_config['max_window'],
            error_type=self.config.pattern_search_config['error_type'],
            max_error=self.config.pattern_search_config['max_error'],
            max_error_interp_mode=self.config.pattern_search_config['max_error_interp_mode'],
            min_similarity=self.config.pattern_search_config['min_similarity']
        )

    def plot_patterns(self, pattern_ranges, plot_settings):
        """
        Visualiza os padrões encontrados na série temporal.
        
        Cria um gráfico interativo destacando as regiões onde
        foram encontrados padrões similares.
        
        Args:
            pattern_ranges (vbt.Ranges): Intervalos com padrões encontrados
            plot_settings (PlotSettings): Configurações de visualização
        """
        fig = pattern_ranges.plot()
        fig.show()

class PatternAnalysis:
    """
    Realiza análises avançadas de padrões em séries temporais.
    
    Implementa métodos para análise de padrões usando diferentes
    indicadores técnicos e métricas de similaridade.
    
    Args:
        data (vbt.Data): Dados OHLCV para análise
        config (Config): Configurações do sistema
        
    Atributos:
        data (vbt.Data): Dados de mercado
        config (Config): Configurações
        indicators (dict): Cache de indicadores calculados
    """
    def __init__(self, data, config):
        self.data = data
        self.config = config
        self.indicators = {}
    
    def calculate_macd(self):
        """
        Calcula o indicador MACD para análise de padrões.
        
        Returns:
            pd.Series: Valores do MACD
        """
        return self.data.run("talib_macd").macd
    
    def find_combined_patterns(self, price_pattern, macd_pattern, window=40):
        """
        Busca padrões combinados em preço e MACD.
        
        Args:
            price_pattern (np.array): Padrão de preço
            macd_pattern (np.array): Padrão de MACD
            window (int): Tamanho da janela
            
        Returns:
            tuple: (price_highs, macd_lows) Padrões encontrados
        """
        macd = self.calculate_macd()
        price_highs = vbt.PATSIM.run(
            self.data.hlc3,
            pattern=price_pattern,
            window=window,
            max_window=window + 10
        )
        macd_lows = vbt.PATSIM.run(
            macd,
            pattern=macd_pattern,
            window=window,
            max_window=window + 10
        )
        return price_highs, macd_lows

class ProjectionAnalysis:
    """
    Análise e geração de projeções baseadas em padrões.
    
    Implementa métodos para projetar movimentos futuros
    baseados em padrões históricos.
    
    Args:
        data (vbt.Data): Dados para análise
        config (Config): Configurações do sistema
    """
    def __init__(self, data, config):
        self.data = data
        self.config = config
    
    def calculate_sma_crossover_ranges(self, use_delta=True):
        """
        Calcula ranges baseados em cruzamentos de médias móveis.
        
        Args:
            use_delta (bool): Se True, usa delta_ranges, caso contrário usa between_ranges
            
        Returns:
            tuple: (entry_ranges, exit_ranges)
        """
        # Gera todas as combinações possíveis de janelas
        windows = np.arange(
            self.config.indicator_config['sma']['min_window'], 
            self.config.indicator_config['sma']['max_window'] + 1
        )
        window_tuples = list(combinations(windows, 2))
        
        # Filtra combinações com diferença mínima
        window_tuples = [
            (fast, slow) for fast, slow in window_tuples 
            if abs(fast - slow) >= self.config.indicator_config['sma']['min_window_diff']
        ]
        
        if not window_tuples:
            raise ValueError("Nenhuma combinação válida de janelas encontrada")
            
        fast_windows, slow_windows = zip(*window_tuples)
        
        # Calcula as médias móveis
        fast_sma = self.data.run("sma", fast_windows, short_name="fast_sma")
        slow_sma = self.data.run("sma", slow_windows, short_name="slow_sma")
        
        # Identifica cruzamentos
        entries = fast_sma.real_crossed_above(slow_sma.real)
        exits = fast_sma.real_crossed_below(slow_sma.real)

        if use_delta:
            # Usando delta_ranges
            entry_ranges = entries.vbt.signals.delta_ranges(
                self.config.projection_config['period'], 
                close=self.data.close
            ).status_closed
            
            exit_ranges = exits.vbt.signals.delta_ranges(
                self.config.projection_config['period'], 
                close=self.data.close
            ).status_closed
        else:
            # Usando between_ranges
            entry_ranges = entries.vbt.signals.between_ranges(
                exits, close=self.data.close
            ).status_closed
            
            exit_ranges = exits.vbt.signals.between_ranges(
                entries, close=self.data.close
            ).status_closed
        
        return entry_ranges, exit_ranges
    
    def plot_projections(self, entry_ranges, exit_ranges=None, n_random=100):
        """
        Plota projeções dos ranges encontrados.
        
        Args:
            entry_ranges: Ranges de entrada
            exit_ranges: Ranges de saída (opcional)
            n_random: Número de colunas aleatórias para plotar
        """
        # Plotar projeções de entrada
        entry_projections = entry_ranges.get_projections(
            proj_period=self.config.projection_config['period'],
            extend=self.config.projection_config['extend']
        )
        
        if entry_projections.shape[1] > 0:  # Verifica se há projeções
            if n_random and entry_projections.shape[1] > n_random:
                rand_cols = np.random.choice(entry_projections.shape[1], n_random)
                entry_projections = entry_projections.iloc[:, rand_cols]
            
            # Plotar projeções de entrada (verde)
            fig = entry_projections.vbt.plot_projections(
                plot_projections=False,
                lower_trace_kwargs=dict(name="Lower (entry)", line_color="green"),
                middle_trace_kwargs=dict(name="Middle (entry)", line_color="green"),
                upper_trace_kwargs=dict(name="Upper (entry)", line_color="green"),
                plot_aux_middle=False,
                plot_fill=False
            )
            
            # Se houver ranges de saída, plotar também
            if exit_ranges is not None:
                exit_projections = exit_ranges.get_projections(
                    proj_period=self.config.projection_config['period'],
                    extend=self.config.projection_config['extend']
                )
                
                if exit_projections.shape[1] > 0:
                    if n_random and exit_projections.shape[1] > n_random:
                        rand_cols = np.random.choice(exit_projections.shape[1], n_random)
                        exit_projections = exit_projections.iloc[:, rand_cols]
                    
                    # Plotar projeções de saída (vermelho)
                    fig = exit_projections.vbt.plot_projections(
                        plot_projections=False,
                        lower_trace_kwargs=dict(name="Lower (exit)", line_color="orangered"),
                        middle_trace_kwargs=dict(name="Middle (exit)", line_color="orangered"),
                        upper_trace_kwargs=dict(name="Upper (exit)", line_color="orangered"),
                        plot_aux_middle=False,
                        plot_fill=False,
                        fig=fig
                    )
            
            fig.update_layout(
                width=self.config.plot_config['monitor_width_ratio'],
                height=self.config.plot_config['monitor_height_ratio']
            )
            fig.show()
        else:
            print("Nenhuma projeção encontrada para plotar")

def main():
    """
    Função principal que orquestra a análise de padrões.
    
    Executa apenas as análises e visualizações configuradas
    em config.execution_config.
    """
    # Inicialização das configurações
    config = Config()
    
    # Configuração do tema
    vbt.settings.set_theme(config.plot_config['theme'])
    
    # Configurações de plotagem
    plot_settings = PlotSettings(config)

    # Manipulação de dados
    data_handler = DataHandler(config)
    data = data_handler.get_data()
    
    # Análise de padrões
    pattern = config.pattern_config['default_pattern']
    
    # Execução condicional das análises
    if config.execution_config['analysis']['pattern_resize']:
        pattern_resizer = PatternResizer(pattern, config)
        if config.execution_config['plots']['resized_pattern']:
            pattern_resizer.plot_resized(plot_settings)

    # Análise de similaridade
    if config.execution_config['analysis']['pattern_similarity']:
        pattern_analyzer = PatternAnalyzer(data.hlc3, pattern, config)
        similarity = pattern_analyzer.calculate_similarity(
            pattern_resizer.resize()
        )
        print(f"Similarity: {similarity}")
    
    # Busca de padrões
    if config.execution_config['analysis']['pattern_search']:
        pattern_searcher = PatternSearcher(data.hlc3, pattern, config)
        pattern_ranges = pattern_searcher.find_patterns()
        if config.execution_config['plots']['pattern_matches']:
            pattern_searcher.plot_patterns(pattern_ranges, plot_settings)
    
    # Análise MACD
    if config.execution_config['analysis']['macd_analysis']:
        pattern_analysis = PatternAnalysis(data, config)
        macd_patterns = pattern_analysis.calculate_macd()
        if config.execution_config['plots']['macd_patterns']:
            pattern_analysis.plot_macd_patterns(macd_patterns, plot_settings)
    
    # Análise de cruzamento de médias móveis
    if config.execution_config['analysis']['sma_crossover']:
        projection_analysis = ProjectionAnalysis(data, config)
        try:
            # Primeiro usando delta_ranges
            entry_ranges, exit_ranges = projection_analysis.calculate_sma_crossover_ranges(
                use_delta=True
            )
            
            if config.execution_config['plots']['projections']:
                print("\nProjeções usando delta_ranges:")
                projection_analysis.plot_projections(
                    entry_ranges, 
                    exit_ranges,
                    n_random=100
                )
            
            # Depois usando between_ranges
            entry_ranges, exit_ranges = projection_analysis.calculate_sma_crossover_ranges(
                use_delta=False
            )
            
            if config.execution_config['plots']['projections']:
                print("\nProjeções usando between_ranges:")
                projection_analysis.plot_projections(
                    entry_ranges, 
                    exit_ranges,
                    n_random=100
                )
                    
        except ValueError as e:
            print(f"Erro ao calcular ranges: {e}")

if __name__ == "__main__":
    main()
