from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class ValidateComplianceInput(BaseModel):
    """Input schema for ValidateCompliance."""
    data: dict = Field(..., description="Data to validate for compliance.")

class ValidateComplianceTool(BaseTool):
    name: str = "Validate Compliance"
    description: str = (
        "Checks whether the provided data complies with predefined criteria. "
        "The agent can use this tool to ensure outputs meet the required standards."
    )
    args_schema: Type[BaseModel] = ValidateComplianceInput

    def _run(self, data: dict) -> bool:
        return data.get("status") == "compliant"
