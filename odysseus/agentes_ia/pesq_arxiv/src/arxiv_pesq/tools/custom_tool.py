from crewai_tools import BaseTool, PDFSearchTool
import arxiv
from datetime import datetime
import json
import yaml
import requests
from typing import List, Dict, Any, Optional
import os
from config.settings import SOLICITACOES, TEMPLATE_YAML, CONTROLES, RESTRICOES
import logging
import traceback

logger = logging.getLogger(__name__)

class ArxivSearchTool(BaseTool):
    name: str = "Arxiv Search Tool"
    description: str = (
        "Ferramenta para buscar e recuperar artigos do Arxiv baseado em palavras-chave ou tópicos. "
        "Prioriza artigos recentes, considerando relevância, impacto e citações."
    )
    
    # Variáveis de classe para os diretórios
    _cache_dir: str = None
    _cache_file: str = None

    def __init__(self):
        super().__init__()
        # Obtém o diretório raiz do projeto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
        
        # Define os diretórios usando o caminho absoluto
        self._cache_dir = os.path.join(project_root, "cache_artigos")
        self._cache_file = os.path.join(self._cache_dir, "artigos_analisados.json")
        
        # Cria o diretório de cache se não existir
        if not os.path.exists(self._cache_dir):
            print(f"Criando diretório de cache: {self._cache_dir}")
            os.makedirs(self._cache_dir, exist_ok=True)
        
        self._init_cache()

    def _init_cache(self):
        """Inicializa ou carrega o cache de artigos"""
        if not os.path.exists(self._cache_file):
            self._save_cache({})
        
    def _load_cache(self) -> Dict:
        """Carrega o cache de artigos analisados"""
        try:
            with open(self._cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_cache(self, cache_data: Dict):
        """Salva o cache de artigos"""
        with open(self._cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

    def _is_article_analyzed(self, paper_id: str) -> bool:
        """Verifica se um artigo já foi analisado"""
        cache = self._load_cache()
        return paper_id in cache

    def _add_to_cache(self, paper_info: Dict):
        """Adiciona um artigo ao cache"""
        cache = self._load_cache()
        cache[paper_info['id']] = {
            'title': paper_info['title'],
            'authors': paper_info['authors'],
            'published': paper_info['published'],
            'analyzed_date': datetime.now().isoformat(),
            'topic': paper_info.get('query', 'não especificado')
        }
        self._save_cache(cache)

    def _run(self, query: str, max_results: int = 3) -> str:
        client = arxiv.Client()
        
        current_year = datetime.now().year
        last_year = current_year - 1
        date_filter = f' AND (submittedDate:[{last_year} TO {current_year}])'
        full_query = f'(ti:"{query}" OR abs:"{query}"){date_filter}'
        
        search = arxiv.Search(
            query=full_query,
            max_results=max_results * 2,  # Busca mais resultados para compensar os já analisados
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )
        
        results = []
        try:
            for paper in client.results(search):
                paper_id = paper.get_short_id()
                
                # Pula artigos já analisados
                if self._is_article_analyzed(paper_id):
                    continue
                
                paper_info = {
                    'id': paper_id,
                    'title': paper.title,
                    'authors': [author.name for author in paper.authors],
                    'published': paper.published.date().isoformat(),
                    'url': paper.pdf_url,
                    'primary_category': paper.primary_category,
                    'categories': paper.categories,
                    'query': query
                }
                results.append(paper_info)
                
                # Para quando atingir o número desejado de novos artigos
                if len(results) >= max_results:
                    break
                
            if not results:
                return "Nenhum artigo novo encontrado para a busca especificada."
                
            response = {
                'query': query,
                'total_results': len(results),
                'papers': results,
                'message': f"Encontrados {len(results)} novos artigos para análise."
            }
            
            # Adiciona os novos artigos ao cache
            for paper in results:
                self._add_to_cache(paper)
                
            return json.dumps(response, ensure_ascii=False, indent=2)
            
        except Exception as e:
            return f"Erro na busca: {str(e)}"

    def get_analyzed_articles(self, topic: str = None) -> Dict:
        """Retorna os artigos já analisados, opcionalmente filtrados por tópico"""
        cache = self._load_cache()
        if topic:
            return {k: v for k, v in cache.items() if v.get('topic') == topic}
        return cache

class PDFAnalysisTool(BaseTool):
    name: str = "PDF Analysis Tool"
    description: str = (
        "Ferramenta para análise de PDFs do Arxiv, extraindo informações relevantes "
        "baseadas em solicitações específicas."
    )

    def __init__(self):
        super().__init__()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
        self._pdf_dir = os.path.join(project_root, "artigos_cientificos")
        
        if not os.path.exists(self._pdf_dir):
            os.makedirs(self._pdf_dir, exist_ok=True)
            logger.info(f"Diretório de PDFs criado: {self._pdf_dir}")

    def _run(self, paper_id: str) -> Dict[str, Any]:
        """Processa um PDF do Arxiv e extrai informações baseadas nas solicitações."""
        try:
            # Baixar o PDF se necessário
            pdf_path = self._download_pdf(paper_id)
            if not pdf_path:
                return {"error": f"Não foi possível baixar o PDF para {paper_id}"}

            # Extrair texto do PDF
            text_content = self._extract_text(pdf_path)
            if not text_content:
                return {"error": f"Não foi possível extrair texto do PDF {paper_id}"}

            # Converter SOLICITACOES string para dicionário
            solicitacoes_dict = self._parse_solicitacoes(SOLICITACOES)
            
            # Processar solicitações
            results = {}
            for key, query in solicitacoes_dict.items():
                try:
                    response = self._process_query(text_content, query)
                    results[key] = response
                except Exception as e:
                    logger.error(f"Erro ao processar {key}: {str(e)}")
                    results[key] = f"Erro ao processar {key}: {str(e)}"

            # Adicionar metadados
            paper = next(arxiv.Client().results(arxiv.Search(id_list=[paper_id])))
            metadata = {
                'title': paper.title,
                'authors': [author.name for author in paper.authors],
                'published': paper.published.isoformat(),
                'pdf_path': pdf_path,
                'arxiv_id': paper.get_short_id()
            }

            return {
                'metadata': metadata,
                'analysis': results
            }

        except Exception as e:
            logger.error(f"Erro ao processar o PDF: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            return {"error": f"Erro ao processar o PDF: {str(e)}"}

    def _parse_solicitacoes(self, solicitacoes_str: str) -> Dict[str, str]:
        """Converte a string de solicitações em um dicionário."""
        solicitacoes_dict = {}
        
        # Remove as tags e quebras de linha desnecessárias
        content = solicitacoes_str.strip()
        content = content.replace('\n<solicitacoes>\n', '')
        content = content.replace('</solicitacoes>\n', '')
        
        # Divide as solicitações por número
        items = content.split('\n')
        current_key = None
        current_value = []
        
        for item in items:
            item = item.strip()
            if not item:
                continue
                
            # Verifica se é uma nova solicitação
            if item[0].isdigit() and ' - ' in item:
                # Salva a solicitação anterior se existir
                if current_key:
                    solicitacoes_dict[current_key] = ' '.join(current_value)
                
                # Inicia nova solicitação
                parts = item.split(' - ', 2)
                if len(parts) >= 2:
                    current_key = parts[1].split(' - ')[0].strip()
                    current_value = [parts[-1].strip()]
            else:
                # Continua acumulando o valor da solicitação atual
                if current_key:
                    current_value.append(item)
        
        # Salva a última solicitação
        if current_key:
            solicitacoes_dict[current_key] = ' '.join(current_value)
            
        return solicitacoes_dict

    def _process_query(self, text_content: str, query: str) -> str:
        """
        Processa uma consulta específica no texto do PDF.
        Pode ser expandido com técnicas mais avançadas de NLP.
        """
        # Implementação básica - pode ser melhorada com técnicas mais sofisticadas
        relevant_sections = []
        paragraphs = text_content.split('\n\n')
        
        for paragraph in paragraphs:
            if query.lower() in paragraph.lower():
                relevant_sections.append(paragraph.strip())
        
        if relevant_sections:
            return ' '.join(relevant_sections[:3])  # Retorna até 3 parágrafos relevantes
        return "Informação não encontrada"

    def _download_pdf(self, paper_id: str) -> Optional[str]:
        """Baixa o PDF do Arxiv se ainda não existir."""
        try:
            pdf_path = os.path.join(self._pdf_dir, f"{paper_id}.pdf")
            
            if os.path.exists(pdf_path):
                logger.info(f"PDF já existe: {pdf_path}")
                return pdf_path

            logger.info(f"Baixando PDF para {paper_id}")
            paper = next(arxiv.Client().results(arxiv.Search(id_list=[paper_id])))
            
            # Baixa o PDF usando o método download_pdf do arxiv
            paper.download_pdf(
                dirpath=self._pdf_dir,
                filename=f"{paper_id}.pdf"
            )
            
            if os.path.exists(pdf_path):
                logger.info(f"PDF baixado com sucesso: {pdf_path}")
                return pdf_path
            else:
                logger.error(f"PDF não foi baixado: {pdf_path}")
                return None

        except Exception as e:
            logger.error(f"Erro ao baixar PDF {paper_id}: {str(e)}")
            logger.error(traceback.format_exc())
            return None

    def _extract_text(self, pdf_path: str) -> Optional[str]:
        """Extrai texto do PDF usando PyPDF2."""
        try:
            import PyPDF2
            text = []
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text.append(page.extract_text())
            return '\n'.join(text)
        except Exception as e:
            logger.error(f"Erro ao extrair texto do PDF: {str(e)}")
            return None

class YAMLValidationTool(BaseTool):
    name: str = "YAML Validation Tool"
    description: str = (
        "Ferramenta para validar e revisar YAMLs produzidos, garantindo conformidade "
        "com o template, solicitações e requisitos especificados."
    )

    def _run(self, yaml_content: str, template: str) -> str:
        """
        Valida o YAML usando o template pré-definido em settings.py
        
        Args:
            yaml_content: Conteúdo YAML a ser validado
            
        Returns:
            Relatório de validação em formato YAML
        """
        try:
            content = yaml.safe_load(yaml_content)
            template_struct = yaml.safe_load(template)
            
            # Validação estrutural
            validation_results = {
                'estrutura': self._validate_structure(content, template_struct),
                'conteudo': self._validate_content(content),
                'formato': self._validate_format(content)
            }
            
            # Gera relatório de validação
            validation = {
                'validation_result': {
                    'is_valid': all(result['is_valid'] for result in validation_results.values()),
                    'details': validation_results,
                    'suggestions': self._generate_suggestions(validation_results)
                }
            }
            
            return yaml.dump(validation, allow_unicode=True)
            
        except Exception as e:
            return f"Erro na validação do YAML: {str(e)}"

    def _validate_structure(self, content: Dict, template: Dict) -> Dict:
        """Valida a estrutura do YAML contra o template"""
        required_fields = template.get('ARTIGO', {}).keys()
        content_fields = content.get('ARTIGO', {}).keys()
        missing_fields = [field for field in required_fields if field not in content_fields]
        
        return {
            'is_valid': len(missing_fields) == 0,
            'missing_fields': missing_fields if missing_fields else None,
            'message': 'Estrutura completa' if not missing_fields else 'Campos obrigatórios ausentes'
        }

    def _validate_content(self, content: Dict) -> Dict:
        """Valida o conteúdo dos campos"""
        artigo = content.get('ARTIGO', {})
        empty_fields = [field for field, value in artigo.items() if not value or value.isspace()]
        
        return {
            'is_valid': len(empty_fields) == 0,
            'empty_fields': empty_fields if empty_fields else None,
            'message': 'Conteúdo válido' if not empty_fields else 'Campos vazios encontrados'
        }

    def _validate_format(self, content: Dict) -> Dict:
        """Valida o formato e consistência do YAML"""
        artigo = content.get('ARTIGO', {})
        format_issues = []
        
        # Verifica se há campos com formatação inconsistente
        for field, value in artigo.items():
            if not isinstance(value, str):
                format_issues.append(f"{field}: tipo inválido")
            elif len(value.strip()) < 10 and field not in ['ARQUIVO']:
                format_issues.append(f"{field}: conteúdo muito curto")
        
        return {
            'is_valid': len(format_issues) == 0,
            'format_issues': format_issues if format_issues else None,
            'message': 'Formato correto' if not format_issues else 'Problemas de formato encontrados'
        }

    def _generate_suggestions(self, validation_results: Dict) -> List[str]:
        """Gera sugestões baseadas nos resultados da validação"""
        suggestions = []
        
        if not validation_results['estrutura']['is_valid']:
            suggestions.append("Complete todos os campos obrigatórios do template")
        
        if not validation_results['conteudo']['is_valid']:
            suggestions.append("Preencha todos os campos com conteúdo relevante")
        
        if not validation_results['formato']['is_valid']:
            suggestions.append("Corrija os problemas de formato identificados")
        
        suggestions.extend([
            "Certifique-se de que o conteúdo está em português do Brasil",
            "Confirme se as informações técnicas não foram traduzidas",
            "Verifique se as análises estão suficientemente detalhadas"
        ])
        
        return suggestions

if __name__ == "__main__":
    print("\n=== VERIFICAÇÃO INICIAL DE DIRETÓRIOS ===")
    search_tool = ArxivSearchTool()
    pdf_tool = PDFAnalysisTool()
    yaml_tool = YAMLValidationTool()
    
    print(f"Diretório de cache: {search_tool._cache_dir}")
    print(f"Cache existe: {os.path.exists(search_tool._cache_dir)}")
    print(f"Arquivo de cache existe: {os.path.exists(search_tool._cache_file)}")
    
    print(f"\nDiretório de PDFs: {pdf_tool._pdf_dir}")
    print(f"Diretório de PDFs existe: {os.path.exists(pdf_tool._pdf_dir)}")
    
    print("\n=== TESTE DE BUSCA ===")
    search_results = search_tool.run("quantum finance", max_results=2)
    print("Resultados da busca:", search_results)
    
    results = json.loads(search_results)
    if results.get('papers'):
        first_paper = results['papers'][0]
        print("\n=== TESTE DE DOWNLOAD PDF ===")
        print(f"Baixando PDF do artigo: {first_paper['title']}")
        pdf_path = pdf_tool.run(paper_id=first_paper['id'])
        print(f"PDF salvo em: {pdf_path}")
        
        print("\n=== TESTE DE VALIDAÇÃO YAML ===")
        # YAML de teste
        test_yaml = """
ARTIGO:
    ARQUIVO: "teste.pdf"
    OBJETIVOS: "Análise de métodos quânticos em finanças"
    GAP: "Lacuna na aplicação de computação quântica em análise financeira"
    METODOLOGIA: "Abordagem experimental usando quantum annealing"
    DATASET: "Dados financeiros históricos"
    RESULTADOS: "Melhoria significativa na otimização de portfólio"
    LIMITAÇÕES: "Restrições de hardware quântico atual"
    CONCLUSÃO: "Potencial promissor para aplicações financeiras"
    AVALIAÇÃO: "Resultados validados estatisticamente"
"""
        # Template de teste
        test_template = """
ARTIGO:
    ARQUIVO: ""
    OBJETIVOS: ""
    GAP: ""
    METODOLOGIA: ""
    DATASET: ""
    RESULTADOS: ""
    LIMITAÇÕES: ""
    CONCLUSÃO: ""
    AVALIAÇÃO: ""
"""
        print("\nValidando YAML de teste...")
        validation_result = yaml_tool.run(test_yaml, test_template)
        print("\nResultado da validação:")
        print(validation_result)
        
        print("\n=== VERIFICAÇÃO FINAL DE ARQUIVOS ===")
        print(f"Cache existe: {os.path.exists(search_tool._cache_file)}")
        print(f"PDF existe: {os.path.exists(pdf_path)}")
        
        print("\n=== TESTE DE CACHE ===")
        cached_articles = search_tool.get_analyzed_articles()
        print("\nArtigos em cache:")
        print(json.dumps(cached_articles, indent=2, ensure_ascii=False))
    