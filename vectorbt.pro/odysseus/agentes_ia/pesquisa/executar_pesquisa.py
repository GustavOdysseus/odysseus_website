from pathlib import Path
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

from src.flows.flow_manager import FlowManager
from src.equipes.equipes_genericas import GerenciadorEquipes
from src.logging.logging_config import LoggingConfig

class ExecutorPesquisa:
    """Executor do flow de pesquisa científica."""
    
    def __init__(self):
        self.logger = LoggingConfig().get_logger(__name__)
        self.base_path = Path(__file__).parent / "src"
        
        # Inicializa gerenciadores
        self.gerenciador_equipes = GerenciadorEquipes(
            caminho_config=str(self.base_path / "configuracoes/equipes/arxiv_equipe.yaml")
        )
        self.flow_manager = FlowManager(
            caminho_config=str(self.base_path / "flows/config"),
            flow_name="pesquisa_cientifica"
        )
        
    async def executar_pesquisa(self, query: str, filtros: Dict[str, Any] = None):
        """
        Executa o flow completo de pesquisa científica.
        
        Args:
            query: Query de pesquisa
            filtros: Filtros adicionais para a pesquisa
        """
        try:
            self.logger.info(f"Iniciando pesquisa com query: {query}")
            
            # Prepara inputs
            inputs = {
                "query": query,
                "filtros": filtros or {},
                "timestamp": datetime.now().isoformat()
            }
            
            # Cria equipe
            crew = self.gerenciador_equipes.criar_equipe("arxiv_crew")
            
            # Inicializa flow
            await self.flow_manager.inicializar_flow([crew], inputs)
            
            # Executa flow
            resultado = await self.flow_manager._executar_crew(crew)
            
            self.logger.info("Pesquisa concluída com sucesso")
            return resultado
            
        except Exception as e:
            self.logger.error(f"Erro durante execução da pesquisa: {str(e)}")
            raise

async def main():
    # Configuração da pesquisa
    query = "quantum finance machine learning"
    filtros = {
        "date_start": "2020",
        "max_results": 50,
        "categories": ["q-fin", "cs.LG"]
    }
    
    # Executa pesquisa
    executor = ExecutorPesquisa()
    try:
        resultado = await executor.executar_pesquisa(query, filtros)
        print("\nResultados da Pesquisa:")
        print("=" * 50)
        print(f"Query: {query}")
        print(f"Artigos encontrados: {len(resultado.get('artigos_encontrados', []))}")
        print(f"Análises concluídas: {len(resultado.get('analise_final', []))}")
        print("\nRecomendações principais:")
        for rec in resultado.get('recomendacoes', [])[:3]:
            print(f"- {rec}")
            
    except Exception as e:
        print(f"Erro durante execução: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
