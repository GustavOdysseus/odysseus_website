"""
Modelos de pesquisa do sistema Odysseus.

Este módulo define os modelos Pydantic que validam as configurações YAML
relacionadas à pesquisa científica, incluindo definições de artigos,
análises e relatórios. Os modelos servem como esquemas de validação
para as configurações definidas em YAML.

Classes:
    ArxivArticle: Modelo para artigos do arXiv
    ArticleAnalysis: Modelo para análise de artigos
    ReviewReport: Modelo para relatórios de revisão
    ResearchOutput: Modelo para saída de pesquisa

Exemplo de arquivo YAML:
```yaml
# research/article_analysis.yaml
query: "machine learning optimization"
filters:
  date_range:
    start: "2023-01-01"
    end: "2024-01-01"
  categories:
    - "cs.AI"
    - "cs.LG"
  min_relevance: 0.8

articles:
  - arxiv_id: "2401.12345"
    title: "Advanced ML Optimization"
    authors:
      - "John Doe"
      - "Jane Smith"
    categories:
      - "cs.AI"
      - "cs.LG"
    primary_category: "cs.AI"
    published_date: "2024-01-15"

analyses:
  - arxiv_id: "2401.12345"
    objectives: "Investigar novas técnicas de otimização"
    methodology: "Análise comparativa de algoritmos"
    key_findings:
      - "Melhoria de 25% na convergência"
      - "Redução de 40% no tempo de treino"
    relevance_score: 0.95
    technical_score: 0.88
    applicability:
      industry: 0.9
      research: 0.85

review:
  methodology_score: 0.92
  coverage_score: 0.88
  recommendations:
    - "Expandir análise para datasets maiores"
    - "Incluir comparação com métodos clássicos"
  reviewer_id: "rev_001"
  status: "approved"

output:
  synthesis:
    main_findings: "Avanços significativos em otimização"
    impact_areas:
      - "Treinamento de modelos grandes"
      - "Otimização em tempo real"
  recommendations:
    - "Adotar nova técnica X para casos Y"
    - "Investigar aplicações em domínio Z"
  metrics:
    confidence: 0.92
    coverage: 0.85
```
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class ArxivArticle(BaseModel):
    """
    Modelo para validação de configurações de artigos do arXiv.
    
    Este modelo define a estrutura esperada para configurações YAML
    de artigos científicos do arXiv.

    Exemplo:
    ```yaml
    arxiv_id: "2401.12345"
    title: "Advanced ML Optimization"
    authors:
      - "John Doe"
      - "Jane Smith"
    abstract: "Este artigo apresenta..."
    categories:
      - "cs.AI"
      - "cs.LG"
    published_date: "2024-01-15"
    primary_category: "cs.AI"
    pdf_url: "https://arxiv.org/pdf/2401.12345"
    doi: "10.1234/example.doi"
    ```

    Atributos:
        arxiv_id (str): ID único do artigo no arXiv
        title (str): Título do artigo
        authors (List[str]): Lista de autores
        abstract (str): Resumo do artigo
        categories (List[str]): Categorias do artigo
        published_date (datetime): Data de publicação
        updated_date (Optional[datetime]): Data de atualização
        pdf_url (str): URL do PDF
        primary_category (str): Categoria principal
        comment (Optional[str]): Comentários adicionais
        journal_ref (Optional[str]): Referência do journal
        doi (Optional[str]): DOI do artigo
    """
    arxiv_id: str
    title: str
    authors: List[str]
    abstract: str
    categories: List[str]
    published_date: datetime
    updated_date: Optional[datetime] = None
    pdf_url: str
    primary_category: str
    comment: Optional[str] = None
    journal_ref: Optional[str] = None
    doi: Optional[str] = None

class ArticleAnalysis(BaseModel):
    """
    Modelo para validação de configurações de análise de artigos.
    
    Este modelo define a estrutura esperada para configurações YAML
    de análises detalhadas de artigos científicos.

    Exemplo:
    ```yaml
    arxiv_id: "2401.12345"
    objectives: "Investigar novas técnicas de otimização"
    methodology: "Análise comparativa de algoritmos"
    key_findings:
      - "Melhoria de 25% na convergência"
      - "Redução de 40% no tempo de treino"
    limitations:
      - "Testado apenas em datasets pequenos"
    future_work:
      - "Expandir para casos de uso industrial"
    relevance_score: 0.95
    technical_score: 0.88
    innovation_score: 0.90
    applicability:
      industry: 0.9
      research: 0.85
    citations_analysis:
      total_citations: 45
      impact_factor: 8.5
    ```

    Atributos:
        arxiv_id (str): ID do artigo analisado
        objectives (str): Objetivos do estudo
        methodology (str): Metodologia utilizada
        key_findings (List[str]): Principais descobertas
        limitations (List[str]): Limitações identificadas
        future_work (List[str]): Trabalhos futuros sugeridos
        relevance_score (float): Score de relevância (0-1)
        technical_score (float): Score técnico (0-1)
        innovation_score (float): Score de inovação (0-1)
        applicability (Dict[str, float]): Scores de aplicabilidade
        citations_analysis (Optional[Dict]): Análise de citações
        reviewer_notes (Optional[str]): Notas do revisor
    """
    arxiv_id: str
    objectives: str
    methodology: str
    key_findings: List[str]
    limitations: List[str]
    future_work: List[str]
    relevance_score: float = Field(ge=0.0, le=1.0)
    technical_score: float = Field(ge=0.0, le=1.0)
    innovation_score: float = Field(ge=0.0, le=1.0)
    applicability: Dict[str, float]
    citations_analysis: Optional[Dict] = None
    reviewer_notes: Optional[str] = None

class ReviewReport(BaseModel):
    """
    Modelo para validação de configurações de relatórios de revisão.
    
    Este modelo define a estrutura esperada para configurações YAML
    de relatórios de revisão de pesquisa.

    Exemplo:
    ```yaml
    selection_evaluation:
      coverage: 0.92
      relevance: 0.88
      diversity: 0.85
    analysis_evaluation:
      depth: 0.90
      accuracy: 0.87
      completeness: 0.93
    methodology_score: 0.92
    coverage_score: 0.88
    recommendations:
      - "Expandir análise para datasets maiores"
      - "Incluir comparação com métodos clássicos"
    revision_history:
      - date: "2024-01-15"
        reviewer: "John Doe"
        changes: "Adicionada análise de limitações"
    reviewer_id: "rev_001"
    status: "approved"
    next_steps:
      - "Incorporar feedback do revisor 2"
      - "Atualizar métricas de performance"
    ```

    Atributos:
        selection_evaluation (Dict[str, Any]): Avaliação da seleção
        analysis_evaluation (Dict[str, Any]): Avaliação das análises
        methodology_score (float): Score da metodologia (0-1)
        coverage_score (float): Score de cobertura (0-1)
        recommendations (List[str]): Recomendações
        revision_history (List[Dict]): Histórico de revisões
        reviewer_id (str): ID do revisor
        review_date (datetime): Data da revisão
        status (str): Status da revisão
        next_steps (Optional[List[str]]): Próximos passos
    """
    selection_evaluation: Dict[str, Any] = Field(..., description="Avaliação da seleção dos artigos")
    analysis_evaluation: Dict[str, Any] = Field(..., description="Avaliação das análises realizadas")
    methodology_score: float = Field(ge=0.0, le=1.0)
    coverage_score: float = Field(ge=0.0, le=1.0)
    recommendations: List[str]
    revision_history: List[Dict]
    reviewer_id: str
    review_date: datetime = Field(default_factory=datetime.now)
    status: str
    next_steps: Optional[List[str]] = Field(default=None, description="Próximos passos")

class ResearchOutput(BaseModel):
    """
    Modelo para validação de configurações de saída de pesquisa.
    
    Este modelo define a estrutura esperada para configurações YAML
    da saída completa de um processo de pesquisa.

    Exemplo:
    ```yaml
    query: "machine learning optimization"
    articles:
      - arxiv_id: "2401.12345"
        title: "Advanced ML Optimization"
        authors: ["John Doe", "Jane Smith"]
    analyses:
      - arxiv_id: "2401.12345"
        objectives: "Investigar novas técnicas"
        key_findings: ["Melhoria de 25% na convergência"]
    synthesis:
      main_findings: "Avanços significativos em otimização"
      impact_areas:
        - "Treinamento de modelos grandes"
        - "Otimização em tempo real"
    recommendations:
      - "Adotar nova técnica X para casos Y"
      - "Investigar aplicações em domínio Z"
    metrics:
      confidence: 0.92
      coverage: 0.85
    timeline:
      start: "2024-01-01T00:00:00"
      end: "2024-01-15T23:59:59"
    status: "completed"
    next_steps:
      - "Publicar relatório final"
      - "Preparar apresentação"
    metadata:
      team_id: "research_001"
      project: "ML Optimization Survey"
    ```

    Atributos:
        query (str): Query de pesquisa original
        articles (List[ArxivArticle]): Artigos analisados
        analyses (List[ArticleAnalysis]): Análises realizadas
        synthesis (Dict[str, Any]): Síntese dos resultados
        recommendations (List[str]): Recomendações
        metrics (Dict[str, float]): Métricas da pesquisa
        timeline (Dict[str, datetime]): Timeline do processo
        status (str): Status da pesquisa
        next_steps (Optional[List[str]]): Próximos passos
        metadata (Optional[Dict]): Metadados adicionais
    """
    query: str
    articles: List[ArxivArticle]
    analyses: List[ArticleAnalysis]
    synthesis: Dict[str, Any]
    recommendations: List[str]
    metrics: Dict[str, float]
    timeline: Dict[str, datetime]
    status: str
    next_steps: Optional[List[str]] = None
    metadata: Optional[Dict] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
