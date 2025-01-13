from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import numpy as np

class CalculateMetricsInput(BaseModel):
    """Input schema for CalculateMetrics."""
    returns: list[float] = Field(..., description="List of financial returns for analysis.")

class CalculateMetricsTool(BaseTool):
    name: str = "Calculate Metrics"
    description: str = (
        "Calculate key financial metrics like Sharpe ratio, volatility, average return, and drawdown. "
        "The agent can use this tool for performance evaluation."
    )
    args_schema: Type[BaseModel] = CalculateMetricsInput

    def _run(self, returns: list[float]) -> dict:
        returns_array = np.array(returns)
        avg_return = np.mean(returns_array)
        volatility = np.std(returns_array)
        sharpe_ratio = avg_return / volatility if volatility != 0 else 0
        max_drawdown = np.min(returns_array)

        return {
            "average_return": avg_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
        }
