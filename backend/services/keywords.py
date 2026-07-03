import re

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "that", "this", "is", "are", "was", "be", "it", "i",
    "my", "we", "you", "app", "tool", "platform", "system", "build",
    "create", "make", "want", "like", "using", "use", "based", "which"
}

def extract_keywords(idea: str, max_keywords: int = 5) -> list[str]:
    idea = idea.lower()
    idea = re.sub(r"[^a-z0-9\s]", "", idea)
    words = idea.split()
    keywords = [w for w in words if w not in STOPWORDS and len(w) > 3]
    # dedupe while preserving order
    seen = set()
    unique = []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            unique.append(k)
    return unique[:max_keywords]