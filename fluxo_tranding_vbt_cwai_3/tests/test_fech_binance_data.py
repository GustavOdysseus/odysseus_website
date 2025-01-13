import unittest
from pathlib import Path
import pandas as pd
import vectorbtpro as vbt
from tools.fetch_binance_data import FetchBinanceDataTool

class TestFetchBinanceData(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para cada teste."""
        self.tool = FetchBinanceDataTool()

    def tearDown(self):
        """Limpeza após cada teste."""
        try:
            Path("data/crypto_base.h5").unlink()
        except FileNotFoundError:
            pass

    def test_initialization(self):
        """Testa a inicialização da ferramenta."""
        self.assertEqual(self.tool.hdf_path, "data/crypto_base.h5")
        self.assertTrue(Path("data").exists())

    def test_single_symbol_fetch(self):
        """Testa download de um único símbolo."""
        result = self.tool._run(
            symbols="BTCUSDT",
            timeframe="1h",
            start="1 day ago"
        )
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(Path("data/crypto_base.h5").exists())
        
        # Verifica se os dados foram salvos corretamente
        with pd.HDFStore("data/crypto_base.h5", mode='r') as store:
            data = store["BTCUSDT/1m"]
            self.assertIsInstance(data, pd.DataFrame)
            self.assertTrue(len(data) > 0)

    def test_multiple_symbols(self):
        """Testa o download de múltiplos símbolos."""
        result = self.tool._run(
            symbols=["BTCUSDT", "ETHUSDT"],
            timeframe="1h",
            start="2023-01-01",
            end="2023-01-02"
        )
        # Verifica a estrutura multi-índice com os símbolos e colunas OHLCV
        self.assertTrue(('BTCUSDT', 'Open') in result.columns)
        self.assertTrue(('ETHUSDT', 'Open') in result.columns)

    def test_resample_functionality(self):
        """Testa a funcionalidade de resample."""
        result = self.tool._run(
            symbols="BTCUSDT",
            timeframe="1h",
            start="2023-01-01",
            end="2023-01-02"
        )
        # Verifica se as colunas OHLCV padrão do VBT estão presentes
        self.assertTrue('Open' in result.columns)
        self.assertTrue('High' in result.columns)
        self.assertTrue('Low' in result.columns)
        self.assertTrue('Close' in result.columns)
        self.assertTrue('Volume' in result.columns)

    def test_data_update(self):
        """Testa a atualização de dados existentes."""
        # Primeiro download
        result1 = self.tool._run(
            symbols="BTCUSDT",
            timeframe="1h",
            start="2 days ago",
            end="1 day ago"
        )
        
        # Segundo download com período sobreposto
        result2 = self.tool._run(
            symbols="BTCUSDT",
            timeframe="1h",
            start="1 day ago"
        )
        
        self.assertIsInstance(result1, pd.DataFrame)
        self.assertIsInstance(result2, pd.DataFrame)
        self.assertTrue(len(result2) > 0)

if __name__ == '__main__':
    unittest.main()