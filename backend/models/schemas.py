from pydantic import BaseModel
from typing import List, Optional

class IdeaRequest(BaseModel):
    idea: str

class RepoSignal(BaseModel):
    name: str
    description: Optional[str]
    stars: int
    url: str
    created_at: str

class Scores(BaseModel):
    originality: int
    saturation: int
    execution_difficulty: int

class EvaluationResponse(BaseModel):
    interpretation: str
    repos: List[RepoSignal]
    scores: Scores
    verdict: str
    improvements: List[str]