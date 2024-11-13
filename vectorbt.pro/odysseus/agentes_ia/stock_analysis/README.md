# Equipe de IA para Análise de Ações
## Introdução
Este projeto é um exemplo usando o framework CrewAI para automatizar o processo de análise de ações. O CrewAI orquestra agentes autônomos de IA, permitindo que eles colaborem e executem tarefas complexas de forma eficiente.

Por [@joaomdmoura](https://x.com/joaomdmoura)

## Índice
- [Framework CrewAI](#framework-crewai)
- [Executando o script](#executando-o-script)
- [Detalhes e Explicação](#detalhes-e-explicação)
- [Usando GPT 3.5](#usando-gpt-35)
- [Usando Modelos Locais com Ollama](#usando-modelos-locais-com-ollama)
- [Contribuindo](#contribuindo)
- [Suporte e Contato](#suporte-e-contato)
- [Licença](#licença)

## Framework CrewAI
O CrewAI é projetado para facilitar a colaboração de agentes de IA que interpretam papéis. Neste exemplo, esses agentes trabalham juntos para fornecer uma análise completa de ações e recomendação de investimento.

## Executando o Script
Por padrão, ele usa GPT-4, então você deve ter acesso a ele para executar.

***Aviso:** Isso usará gpt-4 a menos que você altere, 
e ao fazer isso, custará dinheiro.*

- **Configure o Ambiente**: Copie `.env.example` e configure as variáveis de ambiente para [Browseless](https://www.browserless.io/), [Serper](https://serper.dev/), [SEC-API](https://sec-api.io) e [OpenAI](https://platform.openai.com/api-keys)
- **Instale as Dependências**: Execute `poetry install --no-root`
- **Execute o Script**: Execute `poetry run python3 main.py` (Nota: execute do diretório que contém main.py)

## Detalhes e Explicação
- **Executando o Script**: Execute `python main.py` e insira a empresa a ser analisada quando solicitado. O script utilizará o framework CrewAI para analisar a empresa e gerar um relatório detalhado.
- **Componentes Principais**:
  - `./main.py`: Arquivo principal do script
  - `./stock_analysis_tasks.py`: Arquivo principal com os prompts das tarefas
  - `./stock_analysis_agents.py`: Arquivo principal com a criação dos agentes
  - `./tools`: Contém as classes de ferramentas usadas pelos agentes

## Usando GPT 3.5
O CrewAI permite passar um argumento llm para o construtor do agente, que será seu cérebro. Assim, mudar o agente para usar GPT-3.5 em vez de GPT-4 é tão simples quanto passar esse argumento no agente que você quer usar esse LLM (em `main.py`).
```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model='gpt-3.5') # Carregando GPT-3.5

def especialista_local(self):
    return Agent(
      role='O Melhor Analista Financeiro',
      goal="""Impressionar todos os clientes com sua análise 
      de dados financeiros e tendências de mercado""",
      backstory="""O analista financeiro mais experiente com 
      muita expertise em análise do mercado de ações e estratégias
      de investimento que está trabalhando para um cliente super importante.""",
      verbose=True,
      llm=llm, # <----- passando nossa referência llm aqui
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        CalculatorTools.calculate,
        SECTools.search_10q,
        SECTools.search_10k
      ]
    )
```

## Usando Modelos Locais com Ollama
O framework CrewAI suporta integração com modelos locais, como o Ollama, para maior flexibilidade e personalização. Isso permite utilizar seus próprios modelos, o que pode ser particularmente útil para tarefas especializadas ou preocupações com privacidade de dados.

### Configurando o Ollama
- **Instale o Ollama**: Certifique-se de que o Ollama esteja instalado corretamente em seu ambiente. Siga o guia de instalação fornecido pelo Ollama para instruções detalhadas.
- **Configure o Ollama**: Configure o Ollama para trabalhar com seu modelo local. Você provavelmente precisará [ajustar o modelo usando um Modelfile](https://github.com/jmorganca/ollama/blob/main/docs/modelfile.md). Recomendo adicionar `Observation` como palavra de parada e ajustar `top_p` e `temperature`.

### Integrando Ollama com CrewAI
- Instancie o Modelo Ollama: Crie uma instância do modelo Ollama. Você pode especificar o modelo e a URL base durante a instanciação. Por exemplo:

```python
from langchain.llms import Ollama
ollama_openhermes = Ollama(model="openhermes")
# Passe o Modelo Ollama para os Agentes: Ao criar seus agentes dentro do framework CrewAI, você pode passar o modelo Ollama como argumento para o construtor do Agent. Por exemplo:

def especialista_local(self):
    return Agent(
      role='O Melhor Analista Financeiro',
      goal="""Impressionar todos os clientes com sua análise 
      de dados financeiros e tendências de mercado""",
      backstory="""O analista financeiro mais experiente com 
      muita expertise em análise do mercado de ações e estratégias
      de investimento que está trabalhando para um cliente super importante.""",
      verbose=True,
      llm=ollama_openhermes, # Modelo Ollama passado aqui
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        CalculatorTools.calculate,
        SECTools.search_10q,
        SECTools.search_10k
      ]
    )
```

### Vantagens de Usar Modelos Locais
- **Privacidade**: Modelos locais permitem o processamento de dados dentro de sua própria infraestrutura, garantindo a privacidade dos dados.
- **Personalização**: Você pode personalizar o modelo para atender melhor às necessidades específicas de suas tarefas.
- **Desempenho**: Dependendo da sua configuração, modelos locais podem oferecer benefícios de desempenho, especialmente em termos de latência.

## Licença
Este projeto está licenciado sob a Licença MIT.
