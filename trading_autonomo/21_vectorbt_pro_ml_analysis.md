# Análise do Sistema de Machine Learning do VectorBT Pro

## 1. Visão Geral do Sistema

O sistema de machine learning do VectorBT Pro fornece uma integração robusta com modelos de aprendizado de máquina para previsão de mercado e otimização de estratégias.

## 2. Componentes Principais

### 2.1 Preparação de Dados
```python
from vectorbtpro.utils.ml import DataPreparator
import numpy as np
import pandas as pd

class MLDataPreparator:
    """Preparador de dados para ML."""
    
    def __init__(self):
        self.preparator = DataPreparator()
        
    def prepare_features(self, data: pd.DataFrame,
                        feature_columns: List[str],
                        target_column: str,
                        lookback: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """Prepara features para ML."""
        features = []
        targets = []
        
        for i in range(len(data) - lookback):
            feature_window = data[feature_columns].iloc[i:i+lookback]
            target = data[target_column].iloc[i+lookback]
            
            features.append(feature_window.values.flatten())
            targets.append(target)
            
        return np.array(features), np.array(targets)
        
    def create_sequences(self, data: np.ndarray,
                        sequence_length: int) -> np.ndarray:
        """Cria sequências para modelos recorrentes."""
        sequences = []
        
        for i in range(len(data) - sequence_length):
            sequence = data[i:i+sequence_length]
            sequences.append(sequence)
            
        return np.array(sequences)
```

### 2.2 Modelos de Previsão
```python
from sklearn.ensemble import RandomForestRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class MarketPredictor:
    """Preditor de mercado usando ML."""
    
    def create_rf_model(self, n_estimators: int = 100) -> RandomForestRegressor:
        """Cria modelo Random Forest."""
        return RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=42,
            n_jobs=-1
        )
        
    def create_lstm_model(self, sequence_length: int,
                         n_features: int) -> Sequential:
        """Cria modelo LSTM."""
        model = Sequential([
            LSTM(50, input_shape=(sequence_length, n_features),
                 return_sequences=True),
            LSTM(50),
            Dense(1)
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        return model
        
    def train_model(self, model, X_train: np.ndarray,
                    y_train: np.ndarray, **kwargs):
        """Treina modelo de ML."""
        if isinstance(model, RandomForestRegressor):
            model.fit(X_train, y_train)
        else:
            model.fit(
                X_train, y_train,
                epochs=kwargs.get('epochs', 100),
                batch_size=kwargs.get('batch_size', 32),
                validation_split=kwargs.get('validation_split', 0.2)
            )
```

### 2.3 Otimização de Hiperparâmetros
```python
from sklearn.model_selection import GridSearchCV
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor

class HyperparamOptimizer:
    """Otimizador de hiperparâmetros."""
    
    def optimize_rf(self, X: np.ndarray, y: np.ndarray,
                   param_grid: Dict) -> Dict:
        """Otimiza Random Forest."""
        model = RandomForestRegressor()
        
        grid_search = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=5,
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X, y)
        return grid_search.best_params_
        
    def optimize_lstm(self, build_fn: callable,
                     X: np.ndarray, y: np.ndarray,
                     param_grid: Dict) -> Dict:
        """Otimiza LSTM."""
        model = KerasRegressor(build_fn=build_fn)
        
        grid_search = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=3,
            n_jobs=1,
            verbose=1
        )
        
        grid_search.fit(X, y)
        return grid_search.best_params_
```

### 2.4 Avaliação de Modelos
```python
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

class ModelEvaluator:
    """Avaliador de modelos de ML."""
    
    def calculate_metrics(self, y_true: np.ndarray,
                         y_pred: np.ndarray) -> Dict:
        """Calcula métricas de performance."""
        return {
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'r2': r2_score(y_true, y_pred)
        }
        
    def plot_predictions(self, y_true: np.ndarray,
                        y_pred: np.ndarray,
                        title: str = 'Model Predictions'):
        """Plota previsões vs valores reais."""
        plt.figure(figsize=(12, 6))
        plt.plot(y_true, label='Actual')
        plt.plot(y_pred, label='Predicted')
        plt.title(title)
        plt.legend()
        plt.show()
```

## 3. Estratégias de ML

### 3.1 Estratégia Baseada em Random Forest
```python
class RFStrategy:
    """Estratégia usando Random Forest."""
    
    def __init__(self, lookback: int = 10):
        self.model = RandomForestRegressor(n_jobs=-1)
        self.lookback = lookback
        
    def generate_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Gera features técnicas."""
        features = pd.DataFrame(index=data.index)
        
        # Retornos
        features['returns'] = data['close'].pct_change()
        
        # Médias móveis
        for window in [5, 10, 20]:
            features[f'ma_{window}'] = data['close'].rolling(window).mean()
            
        # Volatilidade
        features['volatility'] = features['returns'].rolling(20).std()
        
        return features.dropna()
        
    def generate_signals(self, predictions: np.ndarray,
                        threshold: float = 0.0) -> pd.DataFrame:
        """Gera sinais de trading."""
        return pd.DataFrame({
            'entries': predictions > threshold,
            'exits': predictions < -threshold
        })
```

### 3.2 Estratégia Baseada em LSTM
```python
class LSTMStrategy:
    """Estratégia usando LSTM."""
    
    def __init__(self, sequence_length: int = 20):
        self.sequence_length = sequence_length
        self.model = None
        
    def build_model(self, n_features: int):
        """Constrói modelo LSTM."""
        self.model = Sequential([
            LSTM(64, input_shape=(self.sequence_length, n_features),
                 return_sequences=True),
            LSTM(32),
            Dense(16, activation='relu'),
            Dense(1)
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
    def prepare_sequences(self, features: pd.DataFrame) -> np.ndarray:
        """Prepara sequências para LSTM."""
        sequences = []
        
        for i in range(len(features) - self.sequence_length):
            sequence = features.iloc[i:i+self.sequence_length]
            sequences.append(sequence.values)
            
        return np.array(sequences)
```

## 4. Integração com Backtesting

### 4.1 Backtester de ML
```python
class MLBacktester:
    """Backtester para estratégias de ML."""
    
    def __init__(self, data: pd.DataFrame, model,
                 train_size: float = 0.8):
        self.data = data
        self.model = model
        self.train_size = train_size
        
    def walk_forward_test(self, window_size: int = 252):
        """Realiza teste walk-forward."""
        results = []
        
        for i in range(0, len(self.data) - window_size, window_size):
            # Treina modelo
            train_data = self.data.iloc[i:i+window_size]
            X_train, y_train = self._prepare_data(train_data)
            self.model.fit(X_train, y_train)
            
            # Testa modelo
            test_data = self.data.iloc[i+window_size:i+window_size*2]
            X_test, y_test = self._prepare_data(test_data)
            predictions = self.model.predict(X_test)
            
            results.append({
                'period': (test_data.index[0], test_data.index[-1]),
                'predictions': predictions,
                'actual': y_test
            })
            
        return results
```

## 5. Melhores Práticas

### 5.1 Desenvolvimento
- Validar dados cuidadosamente
- Evitar data leakage
- Usar cross-validation
- Implementar early stopping

### 5.2 Otimização
- Testar diferentes arquiteturas
- Otimizar hiperparâmetros
- Validar resultados
- Evitar overfitting

### 5.3 Produção
- Monitorar performance
- Atualizar modelos
- Validar previsões
- Manter logs

## 6. Recomendações

### 6.1 Modelagem
- Começar com modelos simples
- Validar premissas
- Testar robustez
- Documentar decisões

### 6.2 Dados
- Garantir qualidade
- Normalizar features
- Tratar outliers
- Manter consistência

### 6.3 Manutenção
- Retreinar modelos
- Atualizar features
- Validar performance
- Otimizar código
