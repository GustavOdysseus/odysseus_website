from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class FetchHistoricalDataInput(BaseModel):
    """Input schema for FetchHistoricalData."""
    api_url: str = Field(..., description="URL to fetch historical market data.")

class FetchHistoricalDataTool(BaseTool):
    name: str = "Fetch Historical Data"
    description: str = (
        "Fetch historical market data from a specified API URL. "
        "Useful for analyzing past trends and preparing datasets for modeling."
    )
    args_schema: Type[BaseModel] = FetchHistoricalDataInput

    def _run(self, api_url: str) -> dict:
        import requests
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
