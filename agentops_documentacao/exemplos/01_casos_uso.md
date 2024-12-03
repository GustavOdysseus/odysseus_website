# Casos de Uso do AgentOps

## 1. Monitoramento de Chatbots

### Cenário
Monitoramento de uma frota de chatbots de atendimento ao cliente.

```python
from agentops import Client
from crewai import Agent, Task, Crew

# Configuração
client = Client()
client.configure(api_key="sua_api_key")

# Monitoramento do chatbot
def monitor_chatbot():
    client.start_session(tags=["chatbot", "customer_service"])
    
    try:
        # Lógica do chatbot
        response = chatbot.process_message(user_input)
        
        # Registro de métricas
        client.log_metric(
            name="response_time",
            value=response.time,
            tags={"intent": response.intent}
        )
        
        return response
        
    except Exception as e:
        client.log_error(
            error=str(e),
            severity="high"
        )
        raise e
    finally:
        client.end_session()
```

## 2. Análise de Documentos

### Cenário
Sistema de análise de documentos usando LlamaIndex.

```python
from agentops import Client
from llama_index import VectorStoreIndex, SimpleDirectoryReader

# Configuração
client = Client()
client.configure(api_key="sua_api_key")
client.start_session(tags=["document_analysis"])

try:
    # Carregamento de documentos
    documents = SimpleDirectoryReader('data').load_data()
    
    # Métricas de documentos
    client.log_metric(
        name="document_count",
        value=len(documents)
    )
    
    # Indexação
    index = VectorStoreIndex.from_documents(documents)
    
    # Consultas
    query_engine = index.as_query_engine()
    response = query_engine.query("Análise financeira")
    
    # Métricas de consulta
    client.log_metric(
        name="query_time",
        value=response.time
    )
    
except Exception as e:
    client.log_error(error=str(e))
finally:
    client.end_session()
```

## 3. Agentes Colaborativos

### Cenário
Equipe de agentes trabalhando em análise de dados.

```python
from agentops import Client
from crewai import Agent, Task, Crew

# Configuração
client = Client()
client.configure(api_key="sua_api_key")

# Criação dos agentes
analyst = Agent(
    role="Analista",
    goal="Analisar dados",
    backstory="Especialista em análise"
)

researcher = Agent(
    role="Pesquisador",
    goal="Coletar dados",
    backstory="Especialista em pesquisa"
)

# Monitoramento da crew
client.start_session(tags=["data_analysis"])

try:
    # Criação das tarefas
    research_task = Task(
        description="Coletar dados",
        agent=researcher
    )
    
    analysis_task = Task(
        description="Analisar tendências",
        agent=analyst
    )
    
    # Execução
    crew = Crew(
        agents=[researcher, analyst],
        tasks=[research_task, analysis_task]
    )
    
    result = crew.kickoff()
    
    # Métricas
    client.log_metric(
        name="execution_time",
        value=result.time
    )
    
except Exception as e:
    client.log_error(error=str(e))
finally:
    client.end_session()
```

## 4. Processamento de Linguagem Natural

### Cenário
Sistema de NLP com múltiplos modelos.

```python
from agentops import Client
from langchain.llms import OpenAI
from langchain.chains import LLMChain

# Configuração
client = Client()
client.configure(api_key="sua_api_key")

def process_text(text, model="gpt-4"):
    client.start_session(
        tags=["nlp", model],
        custom_metrics={"text_length": len(text)}
    )
    
    try:
        # Processamento
        llm = OpenAI(model=model)
        chain = LLMChain(llm=llm)
        result = chain.run(text)
        
        # Métricas
        client.log_metric(
            name="tokens_used",
            value=result.token_usage
        )
        
        return result
        
    except Exception as e:
        client.log_error(error=str(e))
    finally:
        client.end_session()
```

## 5. Automação de Processos

### Cenário
Automação de processos de negócio com agentes.

```python
from agentops import Client
import autogen

# Configuração
client = Client()
client.configure(api_key="sua_api_key")

def automate_process(task_description):
    client.start_session(tags=["automation"])
    
    try:
        # Configuração dos agentes
        assistant = autogen.AssistantAgent(
            name="assistant"
        )
        
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy"
        )
        
        # Execução
        start_time = time.time()
        result = user_proxy.initiate_chat(
            assistant,
            message=task_description
        )
        
        # Métricas
        execution_time = time.time() - start_time
        client.log_metric(
            name="process_time",
            value=execution_time
        )
        
        return result
        
    except Exception as e:
        client.log_error(error=str(e))
    finally:
        client.end_session()
```

## 6. Análise de Sentimento

### Cenário
Sistema de análise de sentimento em redes sociais.

```python
from agentops import Client
from langchain.llms import OpenAI

# Configuração
client = Client()
client.configure(api_key="sua_api_key")

def analyze_sentiment(posts):
    client.start_session(tags=["sentiment_analysis"])
    
    try:
        llm = OpenAI()
        results = []
        
        for post in posts:
            # Análise
            sentiment = llm.analyze_sentiment(post)
            results.append(sentiment)
            
            # Métricas
            client.log_metric(
                name="sentiment_score",
                value=sentiment.score,
                tags={"platform": post.platform}
            )
        
        return results
        
    except Exception as e:
        client.log_error(error=str(e))
    finally:
        client.end_session()
```

## 7. Sistema de Recomendação

### Cenário
Sistema de recomendação de produtos.

```python
from agentops import Client
from llama_index import VectorStoreIndex

# Configuração
client = Client()
client.configure(api_key="sua_api_key")

def get_recommendations(user_id, n=5):
    client.start_session(
        tags=["recommendations"],
        custom_metrics={"user_id": user_id}
    )
    
    try:
        # Carregamento do perfil
        user_profile = load_user_profile(user_id)
        
        # Recomendações
        index = VectorStoreIndex.load("products")
        results = index.similarity_search(
            user_profile,
            k=n
        )
        
        # Métricas
        client.log_metric(
            name="recommendations_count",
            value=len(results)
        )
        
        return results
        
    except Exception as e:
        client.log_error(error=str(e))
    finally:
        client.end_session()
```

## 8. Processamento de Imagens

### Cenário
Sistema de análise de imagens com múltiplos modelos.

```python
from agentops import Client
from langchain.tools import Tool

# Configuração
client = Client()
client.configure(api_key="sua_api_key")

def process_image(image_path, tasks=["object_detection", "classification"]):
    client.start_session(tags=["image_processing"])
    
    try:
        results = {}
        
        for task in tasks:
            # Processamento
            tool = Tool.from_type(task)
            result = tool.process(image_path)
            results[task] = result
            
            # Métricas
            client.log_metric(
                name=f"{task}_time",
                value=result.time
            )
        
        return results
        
    except Exception as e:
        client.log_error(error=str(e))
    finally:
        client.end_session()
```

## 9. Assistente Virtual

### Cenário
Assistente virtual multimodal.

```python
from agentops import Client
from crewai import Agent, Task, Crew

# Configuração
client = Client()
client.configure(api_key="sua_api_key")

class VirtualAssistant:
    def __init__(self):
        self.client = client
        self.session_active = False
    
    def start_session(self):
        self.client.start_session(tags=["virtual_assistant"])
        self.session_active = True
    
    def process_input(self, input_data):
        if not self.session_active:
            self.start_session()
        
        try:
            # Processamento
            input_type = detect_input_type(input_data)
            
            if input_type == "text":
                result = self.process_text(input_data)
            elif input_type == "image":
                result = self.process_image(input_data)
            else:
                raise ValueError(f"Tipo não suportado: {input_type}")
            
            # Métricas
            self.client.log_metric(
                name="processing_time",
                value=result.time,
                tags={"input_type": input_type}
            )
            
            return result
            
        except Exception as e:
            self.client.log_error(error=str(e))
            raise e
    
    def end_session(self):
        if self.session_active:
            self.client.end_session()
            self.session_active = False
```

## 10. Pipeline de ETL

### Cenário
Pipeline de ETL com monitoramento.

```python
from agentops import Client
from langchain.agents import Tool, AgentExecutor

# Configuração
client = Client()
client.configure(api_key="sua_api_key")

class ETLPipeline:
    def __init__(self):
        self.client = client
    
    def extract(self, source):
        self.client.start_session(tags=["etl", "extract"])
        
        try:
            # Extração
            data = self.read_source(source)
            
            # Métricas
            self.client.log_metric(
                name="records_extracted",
                value=len(data)
            )
            
            return data
            
        except Exception as e:
            self.client.log_error(error=str(e))
            raise e
        finally:
            self.client.end_session()
    
    def transform(self, data):
        self.client.start_session(tags=["etl", "transform"])
        
        try:
            # Transformação
            result = self.apply_transformations(data)
            
            # Métricas
            self.client.log_metric(
                name="transformation_time",
                value=result.time
            )
            
            return result
            
        except Exception as e:
            self.client.log_error(error=str(e))
            raise e
        finally:
            self.client.end_session()
    
    def load(self, data, target):
        self.client.start_session(tags=["etl", "load"])
        
        try:
            # Carregamento
            result = self.write_target(data, target)
            
            # Métricas
            self.client.log_metric(
                name="records_loaded",
                value=len(data)
            )
            
            return result
            
        except Exception as e:
            self.client.log_error(error=str(e))
            raise e
        finally:
            self.client.end_session()
```
