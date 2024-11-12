'''
Gostaria de criar um código que obtesse todos os comentários dos códigos que estão dentro de três aspas ("""..."""), de todos os códigos que estão dentro das pastas e subpastas do diretório 'vectorbtpro' e salvar os dados em markdown. A organização de cada comentário salvo em markdown deve ser a seguinte:
1 - Nome da pasta.
1.2 - Nome da subpasta. (Se houver)
1.3 - Nome do código.
1.4 - Nome da classe. (Se houver)
1.5 - Nome da função. (Se houver)
1.6 - Comentário entre 3 áspas.
'''

import os
import ast
import re
from pathlib import Path

def extract_docstrings(file_path):
    """Extrai docstrings de um arquivo Python."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        tree = ast.parse(content)
        docstrings = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                docstring = ast.get_docstring(node)
                if docstring:
                    class_name = None
                    func_name = None
                    
                    if isinstance(node, ast.ClassDef):
                        class_name = node.name
                    elif isinstance(node, ast.FunctionDef):
                        func_name = node.name
                        # Procura o nome da classe pai, se existir
                        for parent in ast.walk(tree):
                            if isinstance(parent, ast.ClassDef) and node in parent.body:
                                class_name = parent.name
                                break
                    
                    docstrings.append({
                        'class_name': class_name,
                        'function_name': func_name,
                        'docstring': docstring.strip()
                    })
        
        return docstrings
    except Exception as e:
        print(f"Erro ao processar {file_path}: {str(e)}")
        return []

def save_to_markdown(base_dir):
    """Salva os docstrings encontrados em um arquivo markdown."""
    output = []
    
    for root, dirs, files in os.walk(base_dir):
        python_files = [f for f in files if f.endswith('.py')]
        
        if python_files:
            rel_path = os.path.relpath(root, base_dir)
            parts = Path(rel_path).parts
            
            for file in python_files:
                file_path = os.path.join(root, file)
                docstrings = extract_docstrings(file_path)
                
                if docstrings:
                    for doc in docstrings:
                        # Para cada docstring, adiciona a hierarquia completa
                        if rel_path != '.':
                            output.append(f"# Pasta: {parts[0]}")
                            if len(parts) > 1:
                                output.append(f"## Subpasta: {'/'.join(parts[1:])}")
                        
                        output.append(f"### Arquivo: {file}")
                        
                        if not doc['class_name'] and not doc['function_name']:
                            output.append("#### Docstring do Módulo")
                        if doc['class_name']:
                            output.append(f"#### Classe: {doc['class_name']}")
                        if doc['function_name']:
                            output.append(f"#### Função: {doc['function_name']}")
                        
                        output.append(f"```\n{doc['docstring']}\n```\n")
                        # Adiciona uma linha em branco entre cada docstring
                        output.append("---\n")
    
    # Salva o resultado em um arquivo markdown
    with open('vectorbtpro_docs.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))

if __name__ == "__main__":
    vectorbtpro_dir = "../vectorbtpro"  # Ajustado para o diretório correto
    save_to_markdown(vectorbtpro_dir)