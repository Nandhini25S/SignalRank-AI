from fastapi import APIRouter, HTTPException
from models.schemas import IdeaRequest, EvaluationResponse
from services.keywords import extract_keywords
from services.github import search_github, filter_repos
from services.llm import evaluate_idea

router = APIRouter()

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(request: IdeaRequest):
    idea = request.idea.strip()
    if not idea or len(idea) < 10:
        raise HTTPException(status_code=400, detail="Idea too short. Give us something to work with.")

    keywords = extract_keywords(idea)
    if not keywords:
        raise HTTPException(status_code=400, detail="Couldn't extract meaningful keywords from your idea.")

    repos = await search_github(keywords)
    filtered = filter_repos(repos, keywords)
    result = await evaluate_idea(idea, filtered)
    return result
