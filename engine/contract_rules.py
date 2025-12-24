from pydantic import BaseModel, Field
from typing import List, Optional

class RiskClause(BaseModel):
    clause_name: str = Field(description="The name of the clause (e.g., 'Automatic Renewal', 'Limitation of Liability')")
    risk_level: str = Field(description="Risk level: Low, Medium, High")
    summary: str = Field(description="A brief explanation of why this clause is risky for the user")
    original_text: str = Field(description="The exact text from the contract (as required by LangExtract source grounding)")

class KeyDate(BaseModel):
    event: str = Field(description="The event the date refers to (e.g., 'Termination Notice Deadline', 'Contract End Date')")
    date_description: str = Field(description="The date or formula for calculating it (e.g., '30 days before anniversary')")
    risk_summary: Optional[str] = Field(description="Any specific risk associated with this date")

class ContractAnalysis(BaseModel):
    contract_type: str = Field(description="The type of contract (e.g., NDA, SaaS Agreement, Lease)")
    fairness_score: int = Field(description="A score from 1-100 representing how fair the contract is to the user (signing party)")
    high_risk_clauses: List[RiskClause] = Field(description="A list of identified high-risk clauses")
    key_dates: List[KeyDate] = Field(description="A list of important dates extracted from the contract")
    overall_summary: str = Field(description="A high-level human-readable summary of the contract's impact")
