import httpx
import os
from models.schemas import RepoSignal

GITHUB_API = "https://api.github.com/search/repositories"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github+json",
    **({"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {})
}

async def search_github(keywords: list[str], max_results: int = 8) -> list[RepoSignal]:
    query = "+".join(keywords)
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": max_results
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(GITHUB_API, headers=HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

    repos = []
    for item in data.get("items", []):
        repos.append(RepoSignal(
            name=item["full_name"],
            description=item.get("description") or "",
            stars=item["stargazers_count"],
            url=item["html_url"],
            created_at=item["created_at"][:10],
        ))
    return repos

def filter_repos(repos: list[RepoSignal], keywords: list[str]) -> list[RepoSignal]:
    """Keep only repos whose name or description overlaps with keywords."""
    keywords_lower = [k.lower() for k in keywords]
    scored = []
    for repo in repos:
        text = f"{repo.name} {repo.description}".lower()
        hits = sum(1 for k in keywords_lower if k in text)
        if hits > 0:
            scored.append((hits, repo))
    scored.sort(key=lambda x: -x[0])
    filtered = [r for _, r in scored]
    # fallback: return top 5 even if no keyword match
    return filtered[:5] if filtered else repos[:5]