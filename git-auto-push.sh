#!/bin/bash

cd "$(dirname "$0")"  # Move para o diretório do script

# Adiciona todas as mudanças
git add .

# Faz commit com timestamp
git commit -m "Auto commit $(date '+%Y-%m-%d %H:%M:%S')"

# Push para o repositório remoto
git push
