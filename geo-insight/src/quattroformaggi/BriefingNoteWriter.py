import os
from pathlib import Path
from openai import AsyncOpenAI  # Używamy asynchronicznego klienta

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
    notes_instruction += f"These are the most recent articles from that area and sector: {articles}. Summarise them in the introduction."
    
    system_prompt = SYSTEM_PROMPT_PATH.read_text().replace(
        "{{interpretation_notes}}", notes_instruction
    )

    # Inicjalizacja klienta OpenRouter (korzysta ze standardu OpenAI)
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("openai_api_key"),
        
    )

    # Wysłanie zapytania asynchronicznie (zauważ 'await' na początku)
    response = await client.chat.completions.create(
        model="openai/gpt-4o-mini", # Przykładowy darmowy model - możesz zmienić
        max_tokens=2048,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"Data (CSV):\n{data_as_csv}",
            }
        ],
    )

    # Struktura zwracanej odpowiedzi z OpenRouter jest inna niż w Anthropic
    return response.choices[0].message.content