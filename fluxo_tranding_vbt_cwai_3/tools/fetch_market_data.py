from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class FetchMarketDataInput(BaseModel):
    """Input schema for FetchMarketData."""
    api_url: str = Field(..., description="URL to fetch macroeconomic and microeconomic data.")

class FetchMarketDataTool(BaseTool):
    name: str = "Fetch Market Data"
    description: str = (
        "Fetch macroeconomic and microeconomic data from a given API URL. "
        "The agent can use this tool to retrieve current market conditions."
    )
    args_schema: Type[BaseModel] = FetchMarketDataInput

    def _run(self, api_url: str) -> dict:
        import requests
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
