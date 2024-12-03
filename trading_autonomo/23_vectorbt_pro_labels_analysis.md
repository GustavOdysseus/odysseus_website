# Análise do Sistema de Labels do VectorBT Pro

## 1. Visão Geral do Sistema

O sistema de labels do VectorBT Pro fornece uma estrutura robusta para rotulagem de dados de mercado, essencial para análise técnica e machine learning.

## 2. Componentes Principais

### 2.1 Gerenciador de Labels
```python
from vectorbtpro.labels import LabelManager
import pandas as pd
import numpy as np

class MarketLabeler:
    """Gerenciador de labels de mercado."""
    
    def __init__(self):
        self.label_manager = LabelManager()
        
    def label_trends(self, close: pd.Series,
                    window: int = 20) -> pd.Series:
        """Rotula tendências de mercado."""
        # Calcula retornos
        returns = close.pct_change(window)
        
        # Inicializa labels
        labels = pd.Series(index=close.index, dtype=str)
        
        # Define thresholds
        up_threshold = 0.02  # 2% de alta
        down_threshold = -0.02  # 2% de baixa
        
        # Rotula tendências
        labels[returns > up_threshold] = 'uptrend'
        labels[returns < down_threshold] = 'downtrend'
        labels[(returns >= down_threshold) & 
              (returns <= up_threshold)] = 'sideways'
        
        return labels
        
    def label_volatility(self, close: pd.Series,
                        window: int = 20) -> pd.Series:
        """Rotula volatilidade."""
        # Calcula volatilidade
        returns = close.pct_change()
        volatility = returns.rolling(window).std()
        
        # Inicializa labels
        labels = pd.Series(index=close.index, dtype=str)
        
        # Define thresholds
        high_vol = volatility.quantile(0.75)
        low_vol = volatility.quantile(0.25)
        
        # Rotula volatilidade
        labels[volatility > high_vol] = 'high'
        labels[volatility < low_vol] = 'low'
        labels[(volatility >= low_vol) & 
              (volatility <= high_vol)] = 'medium'
        
        return labels
```

### 2.2 Detector de Padrões
```python
class PatternLabeler:
    """Rotulador de padrões técnicos."""
    
    def label_candlestick_patterns(self, ohlc: pd.DataFrame) -> pd.DataFrame:
        """Rotula padrões de candlestick."""
        labels = pd.DataFrame(index=ohlc.index)
        
        # Calcula características dos candles
        body = ohlc['close'] - ohlc['open']
        upper_shadow = ohlc['high'] - ohlc[['open', 'close']].max(axis=1)
        lower_shadow = ohlc[['open', 'close']].min(axis=1) - ohlc['low']
        
        # Doji
        doji_threshold = 0.1
        labels['doji'] = abs(body) < (
            (ohlc['high'] - ohlc['low']) * doji_threshold
        )
        
        # Hammer
        labels['hammer'] = (lower_shadow > (abs(body) * 2)) & (
            upper_shadow < abs(body)
        )
        
        # Shooting Star
        labels['shooting_star'] = (upper_shadow > (abs(body) * 2)) & (
            lower_shadow < abs(body)
        )
        
        # Engulfing
        prev_body = body.shift(1)
        labels['bullish_engulfing'] = (
            (body > 0) & 
            (prev_body < 0) & 
            (body.abs() > prev_body.abs())
        )
        
        labels['bearish_engulfing'] = (
            (body < 0) & 
            (prev_body > 0) & 
            (body.abs() > prev_body.abs())
        )
        
        return labels
        
    def label_chart_patterns(self, close: pd.Series,
                            window: int = 20) -> pd.DataFrame:
        """Rotula padrões de gráfico."""
        labels = pd.DataFrame(index=close.index)
        
        # Calcula máximos e mínimos
        rolling_max = close.rolling(window).max()
        rolling_min = close.rolling(window).min()
        
        # Double Top
        labels['double_top'] = (
            (close == rolling_max) & 
            (close.shift(window//2) == rolling_max.shift(window//2))
        )
        
        # Double Bottom
        labels['double_bottom'] = (
            (close == rolling_min) & 
            (close.shift(window//2) == rolling_min.shift(window//2))
        )
        
        # Head and Shoulders
        # Simplificação do padrão
        peak_1 = rolling_max.shift(window)
        peak_2 = rolling_max.shift(window//2)
        peak_3 = rolling_max
        
        labels['head_shoulders'] = (
            (peak_2 > peak_1) & 
            (peak_2 > peak_3) & 
            (abs(peak_1 - peak_3) < (peak_2 * 0.1))
        )
        
        return labels
```

### 2.3 Gerador de Sinais
```python
class SignalGenerator:
    """Gerador de sinais baseado em labels."""
    
    def generate_trend_signals(self, labels: pd.Series) -> pd.DataFrame:
        """Gera sinais baseados em tendência."""
        signals = pd.DataFrame(index=labels.index)
        
        # Entry signals
        signals['entry_long'] = (
            (labels == 'uptrend') & 
            (labels.shift(1) != 'uptrend')
        )
        
        signals['entry_short'] = (
            (labels == 'downtrend') & 
            (labels.shift(1) != 'downtrend')
        )
        
        # Exit signals
        signals['exit_long'] = (
            (labels != 'uptrend') & 
            (labels.shift(1) == 'uptrend')
        )
        
        signals['exit_short'] = (
            (labels != 'downtrend') & 
            (labels.shift(1) == 'downtrend')
        )
        
        return signals
        
    def generate_pattern_signals(self, pattern_labels: pd.DataFrame) -> pd.DataFrame:
        """Gera sinais baseados em padrões."""
        signals = pd.DataFrame(index=pattern_labels.index)
        
        # Entry signals
        signals['entry_long'] = (
            pattern_labels['bullish_engulfing'] | 
            pattern_labels['hammer'] | 
            pattern_labels['double_bottom']
        )
        
        signals['entry_short'] = (
            pattern_labels['bearish_engulfing'] | 
            pattern_labels['shooting_star'] | 
            pattern_labels['double_top'] | 
            pattern_labels['head_shoulders']
        )
        
        return signals
```

### 2.4 Integração com ML
```python
class MLLabeler:
    """Integração de labels com ML."""
    
    def prepare_features(self, ohlcv: pd.DataFrame,
                        labels: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepara features e labels para ML."""
        # Calcula features técnicas
        features = pd.DataFrame(index=ohlcv.index)
        
        # Retornos
        features['returns'] = ohlcv['close'].pct_change()
        
        # Médias móveis
        for window in [5, 10, 20]:
            features[f'ma_{window}'] = (
                ohlcv['close'].rolling(window).mean()
            )
            
        # Volatilidade
        features['volatility'] = (
            features['returns'].rolling(20).std()
        )
        
        # Volume
        features['volume_ma'] = (
            ohlcv['volume'].rolling(20).mean()
        )
        
        # Adiciona padrões como features
        for col in labels.columns:
            features[f'pattern_{col}'] = labels[col].astype(int)
            
        return features.dropna(), labels
        
    def train_classifier(self, features: pd.DataFrame,
                        labels: pd.Series,
                        test_size: float = 0.2):
        """Treina classificador para labels."""
        # Split dados
        X_train, X_test, y_train, y_test = train_test_split(
            features, labels,
            test_size=test_size,
            random_state=42
        )
        
        # Cria e treina modelo
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        # Avalia modelo
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        print(f'Train accuracy: {train_score:.4f}')
        print(f'Test accuracy: {test_score:.4f}')
        
        return model
```

## 3. Análise de Labels

### 3.1 Analisador de Labels
```python
class LabelAnalyzer:
    """Analisador de labels."""
    
    def calculate_label_stats(self, labels: pd.Series) -> Dict:
        """Calcula estatísticas dos labels."""
        stats = {}
        
        # Contagem de labels
        stats['counts'] = labels.value_counts()
        
        # Proporções
        stats['proportions'] = labels.value_counts(normalize=True)
        
        # Duração média
        durations = []
        current_label = None
        current_duration = 0
        
        for label in labels:
            if label == current_label:
                current_duration += 1
            else:
                if current_label is not None:
                    durations.append({
                        'label': current_label,
                        'duration': current_duration
                    })
                current_label = label
                current_duration = 1
                
        stats['avg_durations'] = pd.DataFrame(durations).groupby(
            'label')['duration'].mean()
        
        return stats
        
    def analyze_transitions(self, labels: pd.Series) -> pd.DataFrame:
        """Analisa transições entre labels."""
        transitions = pd.DataFrame(
            index=labels.unique(),
            columns=labels.unique(),
            data=0
        )
        
        for i in range(len(labels)-1):
            current = labels.iloc[i]
            next_label = labels.iloc[i+1]
            transitions.loc[current, next_label] += 1
            
        return transitions
```

## 4. Melhores Práticas

### 4.1 Desenvolvimento
- Validar labels
- Testar consistência
- Documentar regras
- Manter logs

### 4.2 Otimização
- Ajustar thresholds
- Validar padrões
- Testar robustez
- Avaliar resultados

### 4.3 Produção
- Monitorar qualidade
- Atualizar regras
- Validar sinais
- Manter documentação

## 5. Recomendações

### 5.1 Labeling
- Começar simples
- Validar premissas
- Testar consistência
- Documentar decisões

### 5.2 Padrões
- Validar detecção
- Ajustar parâmetros
- Testar robustez
- Manter logs

### 5.3 Manutenção
- Atualizar regras
- Revisar thresholds
- Otimizar código
- Documentar mudanças
