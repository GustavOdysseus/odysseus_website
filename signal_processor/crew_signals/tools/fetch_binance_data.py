from typing import List, Type, Union, Literal, Optional
from pathlib import Path

import vectorbtpro as vbt
import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr


class SmartBinanceUpdater(vbt.DataUpdater):
    """Atualizador inteligente que só atualiza símbolos com dados desatualizados."""
    
    def __init__(self, data, max_age_days=7, **kwargs):
        """
        Args:
            data: Dados iniciais
            max_age_days (int): Idade máxima dos dados em dias
            **kwargs: Argumentos adicionais passados para DataUpdater
        """
        super().__init__(data, **kwargs)
        self._max_age = vbt.timedelta(f"{max_age_days} days")
        self._data = data
        
    @property
    def data(self):
        """Retorna os dados atuais."""
        return self._data
        
    @data.setter
    def data(self, value):
        """Define novos dados."""
        self._data = value
        
    def _needs_update(self, symbol_data):
        """Verifica se os dados do símbolo precisam ser atualizados."""
        if len(symbol_data.index) == 0:
            return True
            
        last_date = symbol_data.index[-1]
        current_time = vbt.utc_datetime()
        age = current_time - last_date
        
        needs_update = age >= self._max_age
        print(f"Verificando atualização:")
        print(f"- Último dado: {last_date}")
        print(f"- Hora atual UTC: {current_time}")
        print(f"- Idade dos dados: {age}")
        print(f"- Idade máxima permitida: {self._max_age}")
        print(f"- Precisa atualizar: {needs_update}")
        
        return needs_update
        
    def update(self, **kwargs):
        """Atualiza apenas os símbolos que precisam ser atualizados."""
        symbols_to_update = []
        
        # Verifica cada símbolo
        for symbol in self.data.symbols:
            symbol_data = self.data.select([symbol])
            if self._needs_update(symbol_data):
                symbols_to_update.append(symbol)
                print(f"Símbolo {symbol} precisa ser atualizado. Último dado: {symbol_data.index[-1]}")
                
        if not symbols_to_update:
            print("Nenhum símbolo precisa ser atualizado")
            return
            
        # Atualiza apenas os símbolos necessários
        print(f"Atualizando símbolos: {symbols_to_update}")
        updated_data = self.data.update(
            symbols=symbols_to_update,
            **kwargs
        )
        
        if updated_data is not None:
            self._data = updated_data


class FetchBinanceDataInput(BaseModel):
    """Input schema for FetchBinanceData."""
    symbols: Union[str, List[str]] = Field(..., description="Single symbol or list of trading pairs")
    timeframe: str = Field(default="1m", description="Timeframe for the data")
    start: str = Field(default="5 years ago", description="Start time for data collection")
    end: Optional[str] = Field(default=None, description="End time for data collection (optional)")
    market_type: Literal["spot", "futures"] = Field(default="spot", description="Market type (spot or futures)")


class BinanceDataManager:
    """Gerenciador de dados da Binance com suporte a cache em DuckDB."""

    def __init__(self, db_file: Path = None):
        """
        Args:
            db_file: Caminho para o arquivo DuckDB. Se None, usa o diretório padrão.
        """
        self._base_timeframe = "1m"  # Sempre busca em 1 minuto para ter mais granularidade
        
        if db_file is None:
            db_file = Path(__file__).parent.parent / "data" / "binance" / "binance_data.duckdb"
            
        db_file.parent.mkdir(parents=True, exist_ok=True)
        self._db_file = db_file
        self._updater = None
        
    def _load_or_fetch_data(self, symbols: Union[str, List[str]], start: str, end: str = None, market_type: str = "spot", timeframe: str = "1m") -> vbt.Data:
        """Carrega dados existentes ou busca novos dados.
        
        Args:
            symbols: Lista de símbolos ou símbolo único
            start: Data inicial
            end: Data final (opcional)
            market_type: Tipo de mercado (spot ou futures)
            timeframe: Timeframe desejado para os dados (ex: "1m", "5m", "1h")
        """
        if isinstance(symbols, str):
            symbols = [symbols]
            
        table_name = f"binance_{market_type}_data"
        fetch_kwargs = dict(
            timeframe=self._base_timeframe,  # Sempre busca em 1 minuto
            start=start,
            end=end,
            klines_type=market_type.upper(),
            tz="UTC",
            show_progress=True
        )
        
        try:
            # Tenta carregar dados existentes do DuckDB
            data = vbt.Data.from_duckdb(
                symbols,
                connection=str(self._db_file),
                table=table_name,
                fetch_kwargs=fetch_kwargs,
                missing_index='drop'  # Remove linhas com dados faltantes em vez de preencher com NaN
            )
            
            if len(data.index) > 0:
                # Configura o atualizador se ainda não existir
                if self._updater is None:
                    self._updater = SmartBinanceUpdater(data)
                    
                # Atualiza os dados existentes
                print(f"\nÚltima data dos dados existentes: {data.index[-1]}")
                updated_data = self._updater.update(
                    fetch_kwargs=fetch_kwargs,
                    silence_warnings=True,  # Silencia avisos de alinhamento
                    missing_index='drop'  # Remove linhas com dados faltantes
                )
                
                # Se não houve atualização, usa os dados existentes
                if updated_data is None:
                    updated_data = data
                
                # Retorna os dados no timeframe solicitado
                if timeframe != self._base_timeframe:
                    try:
                        # Usa a configuração de features do BinanceData
                        updated_data.use_feature_config_of(vbt.BinanceData)
                        updated_data = updated_data.resample(timeframe)
                    except Exception as e:
                        print(f"Erro ao fazer resample: {str(e)}")
                        print("Retornando dados no timeframe base (1m)")
                        
                return updated_data
                
        except Exception as e:
            print(f"Nenhum dado existente encontrado: {str(e)}")
            # Se não encontrou dados, busca novos
        
        try:
            # Busca novos dados da Binance apenas se necessário
            print("\nBuscando novos dados da Binance...")
            data = vbt.BinanceData.pull(
                symbols,
                **fetch_kwargs
            )
            
            # Salva os dados no DuckDB
            data.to_duckdb(
                connection=str(self._db_file),
                table=table_name,
                if_exists="replace"
            )
            
            # Configura o updater com os novos dados
            self._updater = SmartBinanceUpdater(data)
            
            # Retorna os dados no timeframe solicitado
            if timeframe != self._base_timeframe:
                try:
                    data = data.resample(timeframe)
                except Exception as e:
                    print(f"Erro ao fazer resample: {str(e)}")
                    print("Retornando dados no timeframe base (1m)")
                
            return data
            
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar dados: {str(e)}")


class FetchBinanceDataTool(BaseTool):
    """Ferramenta para buscar dados da Binance."""
    name: str = "Fetch Binance Data"
    description: str = "Fetch cryptocurrency market data from Binance using VectorBT Pro."
    args_schema: Type[BaseModel] = FetchBinanceDataInput
    
    # Atributos privados
    _data_manager: BinanceDataManager = PrivateAttr()
    
    def __init__(self, db_file: Path = None):
        """Inicializa a ferramenta.
        
        Args:
            db_file: Caminho para o arquivo DuckDB. Se None, usa o diretório padrão.
        """
        super().__init__()
        self._data_manager = BinanceDataManager(db_file=db_file)

    def _run(self, symbols: Union[str, List[str]], start: str, end: str = None, market_type: str = "spot", timeframe: str = "1m") -> vbt.Data:
        """Executa a ferramenta.
        
        Args:
            symbols: Lista de símbolos ou símbolo único
            start: Data inicial
            end: Data final (opcional)
            market_type: Tipo de mercado (spot ou futures)
            timeframe: Timeframe desejado para os dados (ex: "1m", "5m", "1h")
        """
        try:
            data = self._data_manager._load_or_fetch_data(
                symbols, 
                start, 
                end, 
                market_type,
                timeframe=timeframe
            )
            
            if data is None or len(data.index) == 0:
                raise ValueError("Nenhum dado foi retornado")
                
            return data
            
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar dados: {str(e)}")


if __name__ == "__main__":
    import time
    import logging
    logging.basicConfig(level=logging.INFO)

    # Instancia a ferramenta com timeframe de 5 minutos
    tool = FetchBinanceDataTool()

    print("\n=== Teste de Integração com DuckDB ===")

    print("\nTeste 1: Buscando dados de múltiplos símbolos...")
    start_time = time.time()
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "FETUSDT"]
    data = tool._run(symbols, start="1 month ago", timeframe="5m")
    print(f"✓ Sucesso! Tempo: {time.time() - start_time:.2f}s")
    print("Últimos dados:")
    print(f"Timestamp: {data.index[-1]}")
    print(f"Open: {data.open.iloc[-1]}")
    print(f"High: {data.high.iloc[-1]}")
    print(f"Low: {data.low.iloc[-1]}")
    print(f"Close: {data.close.iloc[-1]}")
    print(f"Volume: {data.volume.iloc[-1]}")

    # Espera 10 segundos
    print("\nEsperando 10 segundos...")
    time.sleep(10)

    print("\nTeste 2: Verificando atualização seletiva...")
    start_time = time.time()
    data = tool._run(symbols, start="1 month ago", timeframe="5m")
    print(f"✓ Sucesso! Tempo: {time.time() - start_time:.2f}s")
    print("Últimos dados:")
    print(data.close)