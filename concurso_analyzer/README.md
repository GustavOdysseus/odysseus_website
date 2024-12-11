# Concurso Analyzer 📝🤖

## Descrição do Projeto
Sistema de análise inteligente de provas e questões de concursos, utilizando CrewAI e processamento de linguagem natural.

## Funcionalidades
- Extração de questões de PDFs
- Análise linguística detalhada
- Identificação de padrões e similaridades
- Geração de estatísticas e relatórios

## Pré-requisitos
- Python 3.9+
- OpenAI API Key

## Instalação

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/concurso-analyzer.git
cd concurso-analyzer
```

2. Crie um ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
```

4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```
OPENAI_API_KEY=sua_chave_aqui
```

## Uso Básico
```python
from concurso_crew import ConcursoAnalyzerCrew

analyzer = ConcursoAnalyzerCrew()
resultado = analyzer.analyze_exam(
    pdf_path='caminho/para/sua/prova.pdf', 
    exam_name='nome-do-concurso'
)
print(resultado)
```

## Executando Testes
```bash
pytest test_concurso_crew.py
```

## Estrutura do Projeto
```
concurso_analyzer/
│
├── tools/
│   ├── pdf_tools.py
│   ├── language_tools.py
│   ├── similarity_tools.py
│   └── statistics_tools.py
│
├── concurso_crew.py      # Classe principal
├── error_handler.py      # Tratamento de erros
├── test_concurso_crew.py # Testes
└── requirements.txt
```

## Contribuição
1. Faça um fork do projeto
2. Crie sua branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença
MIT License
