from crewai import Task
from textwrap import dedent
import yaml
from pathlib import Path

class CustomTasks:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config'
            print(f"Procurando configuração em: {config_path}")  # Debug
        else:
            config_path = Path(config_path)
        
        config_file = config_path / 'tasks.yaml'
        if not config_file.exists():
            # Tentar encontrar em caminhos alternativos
            alt_path = Path(__file__).parent.parent.parent / 'config'
            if (alt_path / 'tasks.yaml').exists():
                config_file = alt_path / 'tasks.yaml'
            else:
                raise FileNotFoundError(f"Arquivo de configuração não encontrado em: {config_file} nem em {alt_path}")
            
        with open(config_file, 'r', encoding='utf-8') as file:
            self.tasks_config = yaml.safe_load(file)

    def debate_task(self, agent, rodada, i):
        debate_config = self.tasks_config['debate']
        return Task(
            description=debate_config['description'].format(
                rodada_num=rodada + 1,
                i=i
            ),
            expected_output=debate_config['expected_output'],
            agent=agent
        )

    def consolidation_task(self, agent):
        consolidacao_config = self.tasks_config['consolidacao']
        return Task(
            description=consolidacao_config['description'],
            expected_output=consolidacao_config['expected_output'],
            agent=agent
        )
