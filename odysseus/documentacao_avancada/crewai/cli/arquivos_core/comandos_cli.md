# Comandos Disponíveis na CLI do CrewAI

## 1. Comandos de Criação
```bash
crewai create [TYPE] [NAME] [OPTIONS]
```
### Tipos Disponíveis:
- `crew`: Criar nova equipe
- `pipeline`: Criar novo pipeline
- `flow`: Criar novo fluxo

### Opções:
- `--provider`: Especificar o provedor para a equipe
- `--skip_provider`: Pular validação do provedor

## 2. Comandos de Treinamento e Avaliação
```bash
crewai train [OPTIONS]
```
### Opções:
- `n_iterations`: Número de iterações de treinamento
- `filename`: Nome do arquivo para salvar resultados

```bash
crewai test [OPTIONS]
```
### Opções:
- `n_iterations`: Número de iterações de teste
- `model`: Modelo a ser usado para teste

## 3. Comandos de Execução
```bash
crewai run              # Executar equipe
crewai replay [TASK_ID] # Reproduzir tarefa específica
```

## 4. Comandos de Memória
```bash
crewai reset-memories [OPTIONS]
```
### Opções:
- `--long`: Resetar memória longa
- `--short`: Resetar memória curta
- `--entities`: Resetar entidades
- `--knowledge`: Resetar conhecimento
- `--kickoff_outputs`: Resetar outputs de kickoff
- `--all`: Resetar todas as memórias

## 5. Comandos de Gerenciamento
```bash
crewai install          # Instalar Crew
crewai update          # Atualizar configurações
```

## 6. Comandos de Fluxo
```bash
crewai flow run        # Executar fluxo
crewai flow plot       # Visualizar fluxo
crewai flow add-crew [CREW_NAME]  # Adicionar equipe ao fluxo
```

## 7. Comandos CrewAI+
```bash
crewai signup          # Criar conta
crewai login           # Autenticar
```

## 8. Comandos de Deploy
```bash
crewai deploy create [OPTIONS]  # Criar deployment
```
### Opções:
- `--yes`: Confirmar automaticamente

```bash
crewai deploy list     # Listar deployments
crewai deploy push [UUID]    # Publicar deployment
crewai deploy status [UUID]  # Verificar status
crewai deploy logs [UUID]    # Ver logs
crewai deploy remove [UUID]  # Remover deployment
```

## 9. Comandos de Ferramentas
```bash
crewai tool create [HANDLE]    # Criar ferramenta
crewai tool install [HANDLE]   # Instalar ferramenta
crewai tool publish [OPTIONS]  # Publicar ferramenta
```
### Opções de Publicação:
- `--public`: Tornar público
- `--force`: Forçar publicação

## 10. Comandos de Log
```bash
crewai log-tasks-outputs    # Ver outputs das últimas tarefas
```

## Exemplos de Uso

### Criar Nova Equipe
```bash
crewai create crew minha-equipe --provider openai
```

### Treinar Equipe
```bash
crewai train --n_iterations 5 --filename resultados.json
```

### Gerenciar Fluxo
```bash
crewai create flow meu-fluxo
crewai flow add-crew equipe-analise
crewai flow run
```

### Deploy
```bash
crewai deploy create --yes
crewai deploy push
crewai deploy logs
```

## Notas Importantes

1. **Autenticação**
   - Alguns comandos requerem autenticação prévia
   - Use `signup` ou `login` antes de comandos CrewAI+

2. **Memória**
   - O reset de memórias é irreversível
   - Use com cautela as opções de reset

3. **Deploy**
   - UUIDs são necessários para operações específicas
   - Mantenha registro dos UUIDs dos deployments

4. **Ferramentas**
   - Handles devem ser únicos
   - Verifique compatibilidade antes da instalação
