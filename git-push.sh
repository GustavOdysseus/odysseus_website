#!/bin/bash

# Adiciona todas as mudanças
git add .

# Pega a data atual para usar no commit
current_date=$(date "+%Y-%m-%d %H:%M:%S")

# Faz o commit com a data
git commit -m "Atualização automática - $current_date"

# Faz o push para o branch atual
git push origin $(git rev-parse --abbrev-ref HEAD)
