from crewai import Agent
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

class AgentesPortugues:
    def __init__(self):
        pass

    def criar_agente_leitor(self) -> Agent:
        """Cria um agente especializado em ler e extrair texto de PDFs"""
        return Agent(
            role='Leitor de PDF',
            goal='Extrair e organizar texto de questões de concurso em PDF',
            backstory="""Você é um especialista em processamento de documentos PDF.
            Sua função é extrair texto de forma organizada e estruturada, mantendo
            a formatação e identificando diferentes partes das questões.""",
            verbose=True,
            allow_delegation=False
        )

    def criar_agente_analista_gramatical(self) -> Agent:
        """Cria um agente especializado em análise gramatical"""
        return Agent(
            role='Analista Gramatical',
            goal='Analisar aspectos gramaticais das questões de português',
            backstory="""Você é um especialista em gramática da língua portuguesa.
            Sua função é identificar regras gramaticais, exceções e padrões
            comuns em questões de concurso.""",
            verbose=True,
            allow_delegation=True
        )

    def criar_agente_analista_interpretacao(self) -> Agent:
        """Cria um agente especializado em interpretação de texto"""
        return Agent(
            role='Analista de Interpretação',
            goal='Analisar aspectos de interpretação textual',
            backstory="""Você é um especialista em interpretação de textos.
            Sua função é identificar elementos como inferência, interpretação,
            coesão, coerência e outros aspectos textuais.""",
            verbose=True,
            allow_delegation=True
        )

    def criar_agente_padronizador(self) -> Agent:
        """Cria um agente especializado em identificar padrões de questões"""
        return Agent(
            role='Analista de Padrões',
            goal='Identificar e categorizar padrões recorrentes em questões',
            backstory="""Você é um especialista em análise de padrões.
            Sua função é identificar tendências, temas recorrentes e
            estruturas comuns em questões de concurso.""",
            verbose=True,
            allow_delegation=True
        )
