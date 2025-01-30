from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class FetchAcademicReferencesInput(BaseModel):
    """Input schema for FetchAcademicReferences."""
    query: str = Field(..., description="Search query for academic references.")
    api_url: str = Field(..., description="API URL to fetch academic references.")

class FetchAcademicReferencesTool(BaseTool):
    name: str = "Fetch Academic References"
    description: str = (
        "Fetch academic references related to a specific topic from an API. "
        "This tool helps agents gather research materials for quantitative analysis."
    )
    args_schema: Type[BaseModel] = FetchAcademicReferencesInput

    def _run(self, query: str, api_url: str) -> list[dict]:
        import requests
        response = requests.get(api_url, params={"query": query})
        response.raise_for_status()
        return response.json()
