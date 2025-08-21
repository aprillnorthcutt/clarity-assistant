from typing import List
from pydantic import BaseModel, Field

class Action(BaseModel):
    step: int
    title: str
    details: str

class BudgetAdj(BaseModel):
    category: str
    change: str
    period: str
    rationale: str

class FinancePlan(BaseModel):
    summary: str
    actions: List[Action] = Field(default_factory=list)
    budget_adjustments: List[BudgetAdj] = Field(default_factory=list)
    risks_or_considerations: List[str] = Field(default_factory=list)
    clarifying_questions: List[str] = Field(default_factory=list)
    tone: str

def validate_finance_plan(obj: dict) -> FinancePlan:
    return FinancePlan(**obj)
