from crewai_tools import BaseTool


class CalculatorTool(BaseTool):
    name: str = "Ferramenta de Cálculo"
    description: str = (
        "Útil para realizar qualquer cálculo matemático, como soma, subtração, multiplicação, divisão, etc. "
        "A entrada para esta ferramenta deve ser uma expressão matemática, alguns exemplos são `200*7` ou `5000/2*10`."
    )

    def _run(self, operation: str) -> int:
        # Implementação aqui
        return eval(operation)
