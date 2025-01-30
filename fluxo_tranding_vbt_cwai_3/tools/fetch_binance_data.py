from crewai.tools import BaseTool
from typing import Type, Union, List
from pydantic import BaseModel, Field
import vectorbtpro as vbt
import pandas as pd
from pathlib import Path


class FetchBinanceDataInput(BaseModel):
    """Input schema for FetchBinanceData."""
    symbols: Union[str, List[str]] = Field(..., description="Single symbol or list of trading pairs")
    timeframe: str = Field(default="1m", description="Timeframe for the data")
    start: str = Field(default="5 years ago", description="Start time for data collection")
    end: str = Field(default=None, description="End time for data collection (optional)")


class FetchBinanceDataTool(BaseTool):
    name: str = "Fetch Binance Data"
    description: str = "Fetch cryptocurrency market data from Binance using VectorBT Pro."
    args_schema: Type[BaseModel] = FetchBinanceDataInput
    hdf_path: str = "data/crypto_base.h5"
    
    def __init__(self):
        super().__init__()
        Path("data").mkdir(parents=True, exist_ok=True)

    def _get_store(self):
        """Retorna um HDFStore configurado."""
        return pd.HDFStore(
            self.hdf_path,
            mode='a',
            complevel=9,
            complib='blosc'
        )

    def _update_symbol_data(self, symbol: str, start: str, end: str = None) -> pd.DataFrame:
        """Atualiza ou baixa dados para um símbolo específico."""
        try:
            # Normaliza o símbolo
            symbol = symbol.upper()
            
            with self._get_store() as store:
                key = f"{symbol}/1m"
                try:
                    existing_data = store[key]
                    # Se dados existem, atualiza a partir do último timestamp
                    last_timestamp = existing_data.index[-1]
                    
                    # Busca dados novos
                    data = vbt.BinanceData.pull(
                        symbol,
                        start=last_timestamp,
                        end=end,
                        timeframe="1m"
                    ).get()  # Obtém o DataFrame imediatamente
                    
                    if data.empty:
                        return existing_data
                        
                    # Concatena apenas dados novos
                    final_data = pd.concat([
                        existing_data, 
                        data[data.index > last_timestamp]
                    ])
                    final_data = final_data[~final_data.index.duplicated(keep='last')]
                    
                    store[key] = final_data
                    return final_data
                    
                except KeyError:
                    # Se não existem dados, faz download completo
                    data = vbt.BinanceData.pull(
                        symbol,
                        start=start,
                        end=end,
                        timeframe="1m"
                    ).get()  # Obtém o DataFrame imediatamente
                    
                    if data.empty:
                        raise Exception(f"Nenhum dado encontrado para {symbol}")
                        
                    store[key] = data
                    return data
                    
        except Exception as e:
            raise Exception(f"Erro ao atualizar dados para {symbol}: {str(e)}")

    def _run(
        self, 
        symbols: Union[str, List[str]], 
        timeframe: str = "1h",
        start: str = "5 years ago",
        end: str = None
    ) -> pd.DataFrame:
        """
        Executa o download e processamento dos dados.
        """
        try:
            # Validação do timeframe
            valid_timeframes = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
            if timeframe not in valid_timeframes:
                raise ValueError(f"Timeframe inválido. Use um dos seguintes: {', '.join(valid_timeframes)}")
            
            # Converte símbolo único para lista
            if isinstance(symbols, str):
                symbols = [symbols]
            
            # Download/atualização dos dados
            all_data = {}
            for symbol in symbols:
                # Sempre baixa em 1m
                symbol_data = self._update_symbol_data(symbol, start, end)
                
                # Converte para objeto Data do VBT
                vbt_data = vbt.Data.from_data(symbol_data)
                
                # Usa a configuração de features do BinanceData
                vbt_data.use_feature_config_of(vbt.BinanceData)
                
                # Resample se necessário usando o método nativo do VBT
                if timeframe != "1m":
                    symbol_data = symbol_data.resample(timeframe).agg({
                        'Open': 'first',
                        'High': 'max',
                        'Low': 'min',
                        'Close': 'last',
                        'Volume': 'sum'
                    })
                
                all_data[symbol] = symbol_data
            
            # Retorna DataFrame único ou múltiplos alinhados
            if len(all_data) == 1:
                return list(all_data.values())[0]
            
            return pd.concat(all_data.values(), axis=1, keys=all_data.keys())
            
        except Exception as e:
            raise Exception(f"Erro ao processar dados: {str(e)}")