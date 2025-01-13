# Padrões de Design para Ferramentas CrewAI

## Introdução
Este guia apresenta os principais padrões de design utilizados no desenvolvimento de ferramentas para o CrewAI. Estes padrões ajudam a criar código mais organizado, manutenível e extensível.

## Padrões Fundamentais

### 1. Factory Method
Usado para criar ferramentas de forma flexível e extensível.

```python
class FerramentaFactory:
    @staticmethod
    def criar_ferramenta(tipo: str, **kwargs) -> BaseTool:
        if tipo == "processador":
            return ProcessadorTool(**kwargs)
        elif tipo == "analisador":
            return AnalisadorTool(**kwargs)
        else:
            raise ValueError(f"Tipo desconhecido: {tipo}")

# Uso
ferramenta = FerramentaFactory.criar_ferramenta(
    "processador",
    config={"opcao": "valor"}
)
```

### 2. Strategy
Para implementar diferentes algoritmos ou comportamentos.

```python
class EstrategiaProcessamento(ABC):
    @abstractmethod
    def processar(self, dados: Any) -> Any:
        pass

class ProcessamentoSimples(EstrategiaProcessamento):
    def processar(self, dados: Any) -> Any:
        return dados.upper()

class ProcessamentoAvancado(EstrategiaProcessamento):
    def processar(self, dados: Any) -> Any:
        return f"AVANCADO: {dados.upper()}"

class FerramentaProcessamento(BaseTool):
    def __init__(self, estrategia: EstrategiaProcessamento):
        self.estrategia = estrategia
        
    def _run(self, entrada: str):
        return self.estrategia.processar(entrada)
```

### 3. Template Method
Para definir o esqueleto de um algoritmo em uma operação.

```python
class FerramentaBase(BaseTool):
    def _run(self, entrada: Any) -> Any:
        # Template method
        self._validar(entrada)
        resultado = self._processar(entrada)
        return self._formatar(resultado)
        
    @abstractmethod
    def _validar(self, entrada: Any) -> bool:
        pass
        
    @abstractmethod
    def _processar(self, entrada: Any) -> Any:
        pass
        
    @abstractmethod
    def _formatar(self, resultado: Any) -> Any:
        pass

class MinhaFerramenta(FerramentaBase):
    def _validar(self, entrada: Any) -> bool:
        return bool(entrada)
        
    def _processar(self, entrada: Any) -> Any:
        return entrada.upper()
        
    def _formatar(self, resultado: Any) -> Any:
        return f"Resultado: {resultado}"
```

## Padrões Estruturais

### 1. Decorator
Para adicionar funcionalidades a ferramentas existentes.

```python
def log_execucao(func):
    def wrapper(self, *args, **kwargs):
        print(f"Executando {self.name}")
        resultado = func(self, *args, **kwargs)
        print(f"Concluído {self.name}")
        return resultado
    return wrapper

class FerramentaLogada(BaseTool):
    @log_execucao
    def _run(self, entrada: str):
        return self._processar(entrada)
```

### 2. Composite
Para criar hierarquias de ferramentas.

```python
class FerramentaComposta(BaseTool):
    def __init__(self, ferramentas: List[BaseTool]):
        self.ferramentas = ferramentas
        
    def _run(self, entrada: Any) -> Any:
        resultado = entrada
        for ferramenta in self.ferramentas:
            resultado = ferramenta.run(resultado)
        return resultado

# Uso
ferramenta = FerramentaComposta([
    ProcessadorTool(),
    AnalisadorTool(),
    FormatadorTool()
])
```

### 3. Adapter
Para compatibilidade com diferentes interfaces.

```python
class BibliotecaExterna:
    def processar_dados(self, dados: str) -> str:
        return f"Processado: {dados}"

class AdaptadorBiblioteca(BaseTool):
    def __init__(self):
        self.biblioteca = BibliotecaExterna()
        
    def _run(self, entrada: str) -> str:
        return self.biblioteca.processar_dados(entrada)
```

## Padrões Comportamentais

### 1. Observer
Para notificação de eventos durante o processamento.

```python
class ObservadorFerramenta(ABC):
    @abstractmethod
    def on_inicio(self, ferramenta: str):
        pass
        
    @abstractmethod
    def on_conclusao(self, ferramenta: str, resultado: Any):
        pass

class FerramentaObservavel(BaseTool):
    def __init__(self):
        self.observadores: List[ObservadorFerramenta] = []
        
    def adicionar_observador(self, obs: ObservadorFerramenta):
        self.observadores.append(obs)
        
    def _notificar_inicio(self):
        for obs in self.observadores:
            obs.on_inicio(self.name)
            
    def _notificar_conclusao(self, resultado: Any):
        for obs in self.observadores:
            obs.on_conclusao(self.name, resultado)
            
    def _run(self, entrada: Any) -> Any:
        self._notificar_inicio()
        resultado = self._processar(entrada)
        self._notificar_conclusao(resultado)
        return resultado
```

### 2. Chain of Responsibility
Para processamento em cadeia.

```python
class ProcessadorBase(ABC):
    def __init__(self, proximo: Optional["ProcessadorBase"] = None):
        self.proximo = proximo
        
    @abstractmethod
    def processar(self, dados: Any) -> Any:
        pass
        
    def proxima_etapa(self, dados: Any) -> Any:
        if self.proximo:
            return self.proximo.processar(dados)
        return dados

class ValidadorEntrada(ProcessadorBase):
    def processar(self, dados: Any) -> Any:
        if not dados:
            raise ValueError("Dados inválidos")
        return self.proxima_etapa(dados)

class Normalizador(ProcessadorBase):
    def processar(self, dados: Any) -> Any:
        dados_norm = dados.lower().strip()
        return self.proxima_etapa(dados_norm)

class FerramentaEncadeada(BaseTool):
    def __init__(self):
        self.chain = ValidadorEntrada(
            Normalizador(None)
        )
        
    def _run(self, entrada: Any) -> Any:
        return self.chain.processar(entrada)
```

### 3. State
Para comportamento variável baseado em estado.

```python
class EstadoFerramenta(ABC):
    @abstractmethod
    def processar(self, dados: Any) -> Any:
        pass

class EstadoNormal(EstadoFerramenta):
    def processar(self, dados: Any) -> Any:
        return dados.upper()

class EstadoOtimizado(EstadoFerramenta):
    def processar(self, dados: Any) -> Any:
        return dados.upper()[:100]

class FerramentaComEstado(BaseTool):
    def __init__(self):
        self.estado = EstadoNormal()
        
    def set_estado(self, estado: EstadoFerramenta):
        self.estado = estado
        
    def _run(self, entrada: Any) -> Any:
        return self.estado.processar(entrada)
```

## Padrões de Concorrência

### 1. Producer-Consumer
Para processamento assíncrono.

```python
class FerramentaAssincrona(BaseTool):
    def __init__(self):
        self.fila = asyncio.Queue()
        self.resultados = {}
        
    async def _producer(self, dados: Any):
        await self.fila.put(dados)
        
    async def _consumer(self):
        while True:
            dados = await self.fila.get()
            resultado = await self._processar_async(dados)
            self.resultados[id(dados)] = resultado
            self.fila.task_done()
            
    async def _run_async(self, entrada: Any) -> Any:
        await self._producer(entrada)
        consumer = asyncio.create_task(self._consumer())
        await self.fila.join()
        consumer.cancel()
        return self.resultados[id(entrada)]
```

### 2. Thread Pool
Para processamento paralelo.

```python
class FerramentaParalela(BaseTool):
    def __init__(self, max_workers: int = 4):
        self.pool = ThreadPoolExecutor(max_workers=max_workers)
        
    def _processar_item(self, item: Any) -> Any:
        return item.upper()
        
    def _run(self, items: List[Any]) -> List[Any]:
        futures = [
            self.pool.submit(self._processar_item, item)
            for item in items
        ]
        return [f.result() for f in futures]
```

## Conclusão
A aplicação apropriada destes padrões de design pode melhorar significativamente a qualidade e manutenibilidade das ferramentas CrewAI. Escolha os padrões que melhor se adequam às suas necessidades específicas e lembre-se de que a simplicidade é uma virtude - use padrões apenas quando eles realmente agregam valor ao seu código.
