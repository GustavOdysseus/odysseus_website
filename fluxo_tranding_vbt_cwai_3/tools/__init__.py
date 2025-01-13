import os
import importlib
from typing import List
from crewai.tools import BaseTool

def get_tool_classes() -> List[BaseTool]:
    tools = []
    # Obtém o diretório atual onde está o __init__.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Lista todos os arquivos Python no diretório
    for file in os.listdir(current_dir):
        if file.endswith('.py') and file != '__init__.py':
            module_name = file[:-3]  # Remove .py
            try:
                # Importa dinamicamente o módulo
                module = importlib.import_module(f'.{module_name}', package='tools')
                
                # Procura por classes que terminam com 'Tool'
                for attr_name in dir(module):
                    if attr_name.endswith('Tool'):
                        tool_class = getattr(module, attr_name)
                        if isinstance(tool_class, type) and issubclass(tool_class, BaseTool):
                            tools.append(tool_class)
            except ImportError:
                continue
    
    return tools

# Obtém todas as ferramentas dinamicamente
available_tools = get_tool_classes()

# Define __all__ dinamicamente
__all__ = [tool.__name__ for tool in available_tools]

# Importa todas as ferramentas para o namespace
for tool in available_tools:
    globals()[tool.__name__] = tool