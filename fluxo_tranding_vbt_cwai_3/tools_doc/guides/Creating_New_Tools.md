# Guia: Criando Novas Ferramentas

## Introdução
Este guia fornece instruções detalhadas sobre como criar novas ferramentas no CrewAI. Você aprenderá as melhores práticas e padrões para implementar ferramentas eficientes e robustas.

## Passo a Passo

### 1. Definição do Schema
```python
from pydantic import BaseModel, Field

class MinhaFerramentaSchema(BaseModel):
    entrada: str = Field(
        ...,
        description="Descrição detalhada do parâmetro"
    )
    configuracao: dict = Field(
        default_factory=dict,
        description="Configurações opcionais"
    )
```

### 2. Implementação da Ferramenta
```python
from crewai.tools import BaseTool

class MinhaFerramenta(BaseTool):
    name = "minha_ferramenta"
    description = """
    Descrição detalhada da ferramenta.
    Inclua exemplos de uso e casos de uso.
    """
    args_schema = MinhaFerramentaSchema
    
    def _run(self, entrada: str, configuracao: dict = None):
        # Implementação da lógica
        resultado = self._processar(entrada, configuracao)
        return resultado
        
    def _processar(self, entrada: str, config: dict):
        # Lógica específica da ferramenta
        pass
```

### 3. Adição de Cache
```python
class MinhaFerramentaCacheavel(BaseTool):
    def cache_function(self, args, result):
        # Decide se deve cachear baseado nos argumentos
        return len(args.get("entrada", "")) > 100
```

### 4. Tratamento de Erros
```python
class MinhaFerramentaSegura(BaseTool):
    def _run(self, entrada: str):
        try:
            return self._processar(entrada)
        except ValueError as e:
            raise ToolUsageErrorException(
                f"Erro no processamento: {str(e)}"
            )
        except Exception as e:
            self._logger.error(f"Erro inesperado: {str(e)}")
            raise
```

## Padrões de Design

### 1. Composição
```python
class FerramentaComposta(BaseTool):
    def __init__(self):
        self.ferramenta1 = Ferramenta1()
        self.ferramenta2 = Ferramenta2()
        
    def _run(self, entrada: str):
        # Usa múltiplas ferramentas
        resultado1 = self.ferramenta1.run(entrada)
        return self.ferramenta2.run(resultado1)
```

### 2. Decorator
```python
def validar_entrada(func):
    def wrapper(self, entrada: str, *args, **kwargs):
        if not self._validar(entrada):
            raise ValueError("Entrada inválida")
        return func(self, entrada, *args, **kwargs)
    return wrapper

class FerramentaValidada(BaseTool):
    @validar_entrada
    def _run(self, entrada: str):
        return self._processar(entrada)
```

### 3. Strategy
```python
class EstrategiaProcessamento(ABC):
    @abstractmethod
    def processar(self, entrada: str) -> str:
        pass

class FerramentaFlexivel(BaseTool):
    def __init__(self, estrategia: EstrategiaProcessamento):
        self.estrategia = estrategia
        
    def _run(self, entrada: str):
        return self.estrategia.processar(entrada)
```

## Melhores Práticas

### 1. Documentação
```python
class FerramentaBemDocumentada(BaseTool):
    """
    Ferramenta para processamento de dados.
    
    Attributes:
        name: Nome único da ferramenta
        description: Descrição detalhada
        
    Examples:
        >>> ferramenta = FerramentaBemDocumentada()
        >>> resultado = ferramenta.run("exemplo")
    """
```

### 2. Validação
```python
class FerramentaRobusta(BaseTool):
    def _validar_entrada(self, entrada: str) -> bool:
        if not entrada:
            return False
        if len(entrada) > 1000:
            return False
        return True
        
    def _run(self, entrada: str):
        if not self._validar_entrada(entrada):
            raise ValueError("Entrada inválida")
```

### 3. Logging
```python
class FerramentaMonitorada(BaseTool):
    def __init__(self):
        self._logger = Logger()
        
    def _run(self, entrada: str):
        self._logger.info(f"Processando entrada: {entrada}")
        try:
            resultado = self._processar(entrada)
            self._logger.info("Processamento concluído")
            return resultado
        except Exception as e:
            self._logger.error(f"Erro: {str(e)}")
            raise
```

## Exemplos Completos

### 1. Ferramenta de Processamento de Texto
```python
class ProcessadorTextoSchema(BaseModel):
    texto: str = Field(..., description="Texto para processar")
    max_length: int = Field(
        default=100,
        description="Tamanho máximo"
    )
    formato: str = Field(
        default="plain",
        description="Formato de saída"
    )

class ProcessadorTexto(BaseTool):
    name = "processador_texto"
    description = "Processa e formata texto"
    args_schema = ProcessadorTextoSchema
    
    def _run(
        self,
        texto: str,
        max_length: int = 100,
        formato: str = "plain"
    ):
        # Validação
        if not self._validar_texto(texto):
            raise ValueError("Texto inválido")
            
        # Processamento
        texto = self._limitar_tamanho(texto, max_length)
        
        # Formatação
        if formato == "html":
            return self._format_html(texto)
        return texto
        
    def _validar_texto(self, texto: str) -> bool:
        return bool(texto and len(texto.strip()) > 0)
        
    def _limitar_tamanho(self, texto: str, max_length: int) -> str:
        return texto[:max_length]
        
    def _format_html(self, texto: str) -> str:
        return f"<p>{texto}</p>"
```

### 2. Ferramenta de Análise de Dados
```python
class AnalisadorDadosSchema(BaseModel):
    dados: list = Field(..., description="Dados para análise")
    metricas: list = Field(
        default=["media", "mediana"],
        description="Métricas a calcular"
    )

class AnalisadorDados(BaseTool):
    name = "analisador_dados"
    description = "Analisa conjuntos de dados"
    args_schema = AnalisadorDadosSchema
    
    def __init__(self):
        self._logger = Logger()
        self._cache = {}
        
    def cache_function(self, args, result):
        # Cache para conjuntos grandes
        return len(args.get("dados", [])) > 1000
        
    def _run(self, dados: list, metricas: list = None):
        try:
            self._logger.info(f"Analisando {len(dados)} items")
            resultados = {}
            
            for metrica in (metricas or ["media", "mediana"]):
                resultados[metrica] = self._calcular_metrica(
                    dados, metrica
                )
                
            return resultados
            
        except Exception as e:
            self._logger.error(f"Erro na análise: {str(e)}")
            raise
            
    def _calcular_metrica(self, dados: list, metrica: str):
        if metrica == "media":
            return sum(dados) / len(dados)
        elif metrica == "mediana":
            return sorted(dados)[len(dados)//2]
        else:
            raise ValueError(f"Métrica não suportada: {metrica}")
```

## Conclusão
A criação de novas ferramentas no CrewAI é um processo estruturado que requer atenção a vários aspectos como documentação, validação, tratamento de erros e performance. Seguindo as melhores práticas e padrões apresentados neste guia, você pode criar ferramentas robustas e eficientes que se integram perfeitamente ao ecossistema CrewAI.
