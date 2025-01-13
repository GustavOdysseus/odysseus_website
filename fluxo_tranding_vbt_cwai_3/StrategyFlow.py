from crewai.flow.flow import Flow, start, listen, router, or_, and_
from StrategyCrew import ModularStrategyCrew  # Importing the correct class


class AdvancedStrategyFlow(Flow[dict]):
    """
    Flow avançado de estratégia que utiliza o ModularStrategyCrew para carregar agentes e tarefas.
    """
    def __init__(self):
        """
        Inicializa o fluxo e a configuração da equipe.
        """
        super().__init__()
        self.crew = ModularStrategyCrew().build()  # Build the Crew from ModularStrategyCrew

        self.initial_state = {
            "metas": {
                "lucro_alvo": 0.10,
                "max_drawdown": 0.05,
                "perda_diaria_max": 0.01
            },
            "tipo_ativo": "Forex",
            "iteracoes": 0,
            "resultados_backtest": {},
            "status": "inicial",
            "compliance_ok": None
        }

    ##############################
    # Métodos de Execução
    ##############################

    @start
    async def definir_metas(self):
        """Define as metas iniciais e inicia o fluxo."""
        self.state["status"] = "metas_definidas"
        return "metas_definidas"

    @listen("metas_definidas")
    async def solicitar_contexto_mercado(self):
        """Solicita contexto macro e microeconômico."""
        return "contexto_solicitado"

    @listen("contexto_solicitado")
    async def equipe_inteligencia_mercado(self):
        """Chama a equipe Inteligência de Mercado para fornecer contexto."""
        task = next(t for t in self.crew.tasks if t.description == "Coletar dados macroeconômicos e microeconômicos.")
        output = task.execute_sync()
        self.state.update({
            "contexto_mercado": output.raw,
            "status": "contexto_atualizado"
        })
        return "contexto_atualizado"

    @listen("contexto_atualizado")
    async def solicitar_pesquisa_quantitativa(self):
        """Solicita insights quantitativos e acadêmicos."""
        return "pesquisa_solicitada"

    @listen("pesquisa_solicitada")
    async def equipe_pesquisa_quantitativa(self):
        """Chama a equipe de Pesquisa Quantitativa para fornecer modelos."""
        task = next(t for t in self.crew.tasks if t.description == "Analisar dados e gerar indicadores.")
        output = task.execute_sync()
        self.state.update({
            "pesquisa": output.raw,
            "status": "pesquisa_concluida"
        })
        return "pesquisa_concluida"

    @listen(and_("contexto_atualizado", "pesquisa_concluida"))
    async def solicitar_dados(self):
        """Solicita coleta e preparação de dados históricos."""
        return "dados_solicitados"

    @listen("dados_solicitados")
    async def equipe_dados_integracao(self):
        """Chama a equipe de Dados para preparar os dados históricos."""
        task = next(t for t in self.crew.tasks if t.description == "Coletar e preparar dados históricos.")
        output = task.execute_sync()
        self.state["dados_historicos"] = output.raw
        self.state["status"] = "dados_preparados"
        return "dados_preparados"

    @listen("dados_preparados")
    async def equipe_analise_quantitativa(self):
        """Executa backtesting usando os dados e indicadores."""
        task = next(t for t in self.crew.tasks if t.description == "Executar backtesting.")
        output = task.execute_sync()
        self.state["resultados_backtest"] = output.raw
        self.state["status"] = "backtest_concluido"
        return "backtest_concluido"

    @listen("backtest_concluido")
    async def equipe_gestao_riscos(self):
        """Valida os resultados contra as metas estabelecidas."""
        task = next(t for t in self.crew.tasks if t.description == "Validar conformidade com politicas de risco.")
        output = task.execute_sync()
        resultados = self.state["resultados_backtest"]
        metas = self.state["metas"]
        compliance = output.raw.get("compliance", False)
        if compliance and resultados["lucro"] >= metas["lucro_alvo"] and resultados["drawdown"] <= metas["max_drawdown"]:
            self.state["compliance_ok"] = True
            return "estrategia_aprovada"
        else:
            self.state["compliance_ok"] = False
            return "necessita_ajustes"

    ##############################
    # Roteadores Estratégicos
    ##############################

    @router(equipe_gestao_riscos)
    async def router_gestao_riscos(self):
        """Decide o próximo passo após a gestão de riscos."""
        if self.state["compliance_ok"]:
            return "finalizar"
        elif self.state["iteracoes"] >= 5:
            return "finalizar_falha"
        else:
            return "ajustar_estrategia"

    @listen("ajustar_estrategia")
    async def comite_ajustes(self):
        """Realiza ajustes no contexto e reinicia o fluxo."""
        iteracao_atual = self.state["iteracoes"]
        self.state["iteracoes"] = iteracao_atual + 1
        self.state.update({
            "contexto_mercado": {
                "macro": {"politica_monetaria": "dovish" if iteracao_atual > 2 else "hawkish"},
                "micro": {"ativos_relevantes": ["USD/JPY", "AUD/USD"]}
            },
            "status": "contexto_revisado"
        })
        return "contexto_revisado"

    @listen("finalizar")
    async def equipe_documentacao(self):
        """Finaliza o fluxo e salva os resultados."""
        task = next(t for t in self.crew.tasks if t.description == "Documentar os resultados finais.")
        output = task.execute_sync()
        self.state.update({
            "documentacao_final": output.raw,
            "status": "estrategia_finalizada"
        })
        return "estrategia_finalizada"

    @listen("finalizar_falha")
    async def equipe_documentacao_falha(self):
        """Documenta o fracasso em atingir as metas."""
        self.state["status"] = "falha_documentada"
        return "falha_documentada"

if __name__ == "__main__":
    flow = AdvancedStrategyFlow()
    final_output = flow.kickoff()
    print("Estado final:", flow.state)
    print("Saídas dos métodos:", flow.method_outputs)
