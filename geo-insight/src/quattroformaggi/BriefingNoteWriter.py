from pathlib import Path
import os
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SYSTEM_PROMPT_PATH = PROJECT_ROOT / "prompts" / "BriefingNoteWriter.md"


async def brief_writer(
    data_as_csv: str, message: str, articles: str, interpretation_notes: str | None = None
) -> str:
    notes_instruction = (
        f"\n5. **Interpretation Notes:** Add the following as the first paragraph of the briefing note:\n{interpretation_notes}\n"
        if interpretation_notes
        else ""
    )

    notes_instruction += f"This is the original user query: {message}."
    notes_instruction += f"These are the most recent articles from that area and sector{articles}. Summarise them in the introduction."
    system_prompt = SYSTEM_PROMPT_PATH.read_text().replace(
        "{{interpretation_notes}}", notes_instruction
    )

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
            "max_tokens": 2048,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": (f"Data (CSV):\n{data_as_csv}"),
                }
            ],
        }
    )
    
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
