import json
from datetime import date
from pathlib import Path
import os
import requests

from models.QuerySpec import QuerySpec

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SYSTEM_PROMPT_PATH = PROJECT_ROOT / "prompts" / "QueryInterpreter.md"


async def interpret_query(user_query: str) -> QuerySpec:
    system_prompt = SYSTEM_PROMPT_PATH.read_text().replace(
        "{{today}}", date.today().isoformat()
    )
    schema = json.dumps(QuerySpec.model_json_schema(), indent=2)

    # Use OpenRouter API
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://huggingface.co/spaces",
        "X-Title": "UNOCHA Geo-Insight"
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json={
            "model": "claude-3.5-sonnet",
            "max_tokens": 1024,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Interpret this query:\n\n{user_query}\n\n"
                        "Respond with a single JSON object matching this schema — no markdown, no explanation:\n"
                        f"{schema}"
                    ),
                }
            ],
        }
    )
    
    response.raise_for_status()
    text = response.json()["choices"][0]["message"]["content"].strip()
    
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return QuerySpec.model_validate_json(text)
