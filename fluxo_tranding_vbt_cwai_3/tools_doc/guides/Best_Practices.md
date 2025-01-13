# Melhores Práticas para Ferramentas CrewAI

## Introdução
Este guia apresenta as melhores práticas para desenvolvimento, implementação e manutenção de ferramentas no CrewAI. Seguir estas práticas ajudará a criar ferramentas mais robustas, eficientes e fáceis de manter.

## Princípios Fundamentais

### 1. Responsabilidade Única
- Cada ferramenta deve ter um propósito claro e específico
- Evite ferramentas que fazem muitas coisas diferentes
- Divida funcionalidades complexas em múltiplas ferramentas

### 2. Consistência
- Siga padrões de nomenclatura consistentes
- Mantenha estrutura de código uniforme
- Use convenções estabelecidas do projeto

### 3. Robustez
- Implemente validação abrangente
- Trate erros adequadamente
- Forneça feedback claro

## Práticas de Desenvolvimento

### 1. Documentação
```python
class ExemploFerramenta(BaseTool):
    """
    Ferramenta para processamento de exemplo.
    
    Esta ferramenta demonstra as melhores práticas de documentação.
    
    Attributes:
        name (str): Nome único da ferramenta
        description (str): Descrição detalhada
        args_schema (Type[BaseModel]): Schema de argumentos
        
    Examples:
        >>> ferramenta = ExemploFerramenta()
        >>> resultado = ferramenta.run(
        ...     entrada="exemplo",
        ...     config={"opcao": "valor"}
        ... )
    
    Note:
        Certifique-se de validar todas as entradas
        antes do processamento.
    """
```

### 2. Validação de Entrada
```python
def _validar_entrada(self, entrada: Any) -> bool:
    """
    Valida entrada antes do processamento.
    
    Args:
        entrada: Dados a serem validados
        
    Returns:
        bool: True se válido, False caso contrário
        
    Raises:
        ValueError: Se a entrada for inválida
    """
    if entrada is None:
        raise ValueError("Entrada não pode ser None")
        
    if isinstance(entrada, str) and not entrada.strip():
        raise ValueError("Entrada não pode ser vazia")
        
    return True
```

### 3. Tratamento de Erros
```python
def _run(self, *args, **kwargs):
    """
    Implementação principal com tratamento de erros.
    
    Returns:
        Any: Resultado do processamento
        
    Raises:
        ToolUsageErrorException: Para erros de uso
        Exception: Para outros erros
    """
    try:
        # Validação
        self._validar_entrada(*args, **kwargs)
        
        # Processamento
        resultado = self._processar(*args, **kwargs)
        
        # Pós-processamento
        return self._formatar_saida(resultado)
        
    except ValueError as e:
        raise ToolUsageErrorException(str(e))
    except Exception as e:
        self._logger.error(f"Erro inesperado: {str(e)}")
        raise
```

## Otimização de Performance

### 1. Cache Eficiente
```python
class FerramentaOtimizada(BaseTool):
    def __init__(self):
        self._cache = {}
        self._cache_hits = 0
        self._cache_misses = 0
        
    def cache_function(self, args, result):
        # Decide se deve cachear
        if self._is_cacheable(args):
            self._update_metrics("hit")
            return True
        self._update_metrics("miss")
        return False
        
    def _is_cacheable(self, args):
        # Implementa lógica de decisão de cache
        return True
        
    def _update_metrics(self, tipo: str):
        if tipo == "hit":
            self._cache_hits += 1
        else:
            self._cache_misses += 1
```

### 2. Processamento Assíncrono
```python
class FerramentaAssincrona(BaseTool):
    async def _run_async(self, *args, **kwargs):
        """Versão assíncrona do processamento."""
        return await self._processar_async(*args, **kwargs)
        
    def _run(self, *args, **kwargs):
        """Wrapper síncrono para compatibilidade."""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            self._run_async(*args, **kwargs)
        )
```

### 3. Otimização de Memória
```python
class FerramentaEficiente(BaseTool):
    def _processar_stream(self, entrada: Iterator):
        """Processa dados em streaming para economia de memória."""
        for item in entrada:
            yield self._processar_item(item)
            
    def _limpar_recursos(self):
        """Libera recursos após processamento."""
        self._cache.clear()
        gc.collect()
```

## Monitoramento e Logging

### 1. Logging Estruturado
```python
class FerramentaMonitorada(BaseTool):
    def __init__(self):
        self._logger = Logger()
        self._metrics = MetricsCollector()
        
    def _run(self, *args, **kwargs):
        self._logger.info(
            "Iniciando processamento",
            extra={
                "args": args,
                "kwargs": kwargs,
                "tool": self.name
            }
        )
        
        try:
            with self._metrics.measure_time():
                resultado = self._processar(*args, **kwargs)
                
            self._logger.info(
                "Processamento concluído",
                extra={"resultado": resultado}
            )
            
            return resultado
            
        except Exception as e:
            self._logger.error(
                "Erro no processamento",
                extra={"error": str(e)},
                exc_info=True
            )
            raise
```

### 2. Métricas
```python
class MetricsCollector:
    def __init__(self):
        self.tempos = []
        self.erros = 0
        self.sucessos = 0
        
    @contextmanager
    def measure_time(self):
        inicio = time.time()
        try:
            yield
            self.sucessos += 1
        except Exception:
            self.erros += 1
            raise
        finally:
            duracao = time.time() - inicio
            self.tempos.append(duracao)
            
    def get_stats(self):
        return {
            "tempo_medio": statistics.mean(self.tempos),
            "tempo_max": max(self.tempos),
            "sucessos": self.sucessos,
            "erros": self.erros,
            "taxa_erro": self.erros/(self.sucessos+self.erros)
        }
```

## Testes

### 1. Testes Unitários
```python
def test_ferramenta_processamento():
    ferramenta = MinhaFerramenta()
    
    # Teste básico
    resultado = ferramenta.run("teste")
    assert resultado == "TESTE"
    
    # Teste de erro
    with pytest.raises(ValueError):
        ferramenta.run("")
        
    # Teste de cache
    resultado1 = ferramenta.run("cache")
    resultado2 = ferramenta.run("cache")
    assert resultado1 == resultado2
```

### 2. Testes de Integração
```python
@pytest.mark.integration
def test_integracao_ferramentas():
    ferramenta1 = Ferramenta1()
    ferramenta2 = Ferramenta2()
    
    # Teste fluxo completo
    resultado1 = ferramenta1.run("entrada")
    resultado_final = ferramenta2.run(resultado1)
    
    assert resultado_final == "PROCESSADO"
```

### 3. Testes de Performance
```python
@pytest.mark.benchmark
def test_performance_ferramenta(benchmark):
    ferramenta = MinhaFerramenta()
    
    def run_test():
        for _ in range(1000):
            ferramenta.run("teste")
            
    # Executa benchmark
    resultado = benchmark(run_test)
    
    # Verifica limites
    assert resultado.stats.mean < 0.1  # 100ms max
```

## Segurança

### 1. Validação de Entrada
```python
def _sanitizar_entrada(self, entrada: str) -> str:
    """Sanitiza entrada para prevenir injeção."""
    return bleach.clean(entrada)
    
def _validar_tamanho(self, dados: Any) -> bool:
    """Previne ataques DoS."""
    tamanho = len(str(dados))
    return tamanho <= self.MAX_INPUT_SIZE
```

### 2. Controle de Acesso
```python
class FerramentaSegura(BaseTool):
    def __init__(self, permissoes: List[str]):
        self.permissoes = permissoes
        
    def _verificar_permissao(self, contexto: dict) -> bool:
        """Verifica se tem permissão necessária."""
        return all(
            p in contexto.get("permissoes", [])
            for p in self.permissoes
        )
        
    def _run(self, *args, contexto: dict, **kwargs):
        if not self._verificar_permissao(contexto):
            raise PermissionError("Acesso negado")
```

## Conclusão
Seguir estas melhores práticas ajudará a criar ferramentas mais robustas, eficientes e seguras no CrewAI. Lembre-se de que estas são diretrizes gerais e podem precisar ser adaptadas para casos específicos.
