import os
import json
from openai import AsyncOpenAI
from models.schemas import RepoSignal, Scores, EvaluationResponse

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a brutally honest idea evaluator. You do not soften blows. You do not encourage unless it is genuinely deserved.

Rules:
- Your verdict MUST match your scores. If originality is 2/10, the verdict must say it's been done to death — not "moderately common".
- Low originality + high saturation = the verdict should be scathing. Use sarcasm if warranted.
- Never open with soft language: banned openers include "Moderately", "Interesting", "This could", "While", "Although".
- Open with the sharpest truth first. No warm-up sentences.
- Forbidden phrases: "Great idea", "innovative", "exciting", "interesting", "could be useful".
- Improvements must be specific and directional — not generic startup platitudes like "improve the algorithm" or "enhance user experience".
- Scores must be brutally accurate. If GitHub has 10+ repos doing this, originality ≤ 3.

Verdict tone guide by originality score:
- 0-3: Sarcastic, blunt. This has been built. Say it like that.
- 4-6: Direct, skeptical. Potential exists but the bar to stand out is named explicitly.
- 7-10: Still critical. Name exactly what makes it worth pursuing.

You must respond ONLY with a valid JSON object in this exact structure:
{
  "interpretation": "<1-2 line restatement of what the idea actually is>",
  "scores": {
    "originality": <0-10>,
    "saturation": <0-10>,
    "execution_difficulty": <0-10>
  },
  "verdict": "<sharp, memorable 1-2 sentence verdict — no fluff, no soft openers>",
  "improvements": ["<specific direction 1>", "<specific direction 2>", "<specific direction 3>"]
}"""

def format_repos(repos: list[RepoSignal]) -> str:
    if not repos:
        return "No relevant GitHub repos found."
    lines = []
    for r in repos:
        lines.append(f"- {r.name} ({r.stars}⭐, created {r.created_at}): {r.description}")
    return "\n".join(lines)

async def evaluate_idea(idea: str, repos: list[RepoSignal]) -> EvaluationResponse:
    repo_context = format_repos(repos)

    user_message = f"""Idea submitted for evaluation:
\"{idea}\"

Relevant GitHub projects already in existence:
{repo_context}

Evaluate this idea honestly based on the GitHub landscape above."""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)

    return EvaluationResponse(
        interpretation=data["interpretation"],
        repos=repos,
        scores=Scores(**data["scores"]),
        verdict=data["verdict"],
        improvements=data["improvements"]
    )