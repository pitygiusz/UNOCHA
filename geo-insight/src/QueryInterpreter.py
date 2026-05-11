import os
import json
from datetime import date
from pathlib import Path

from openai import AsyncOpenAI  
from QuerySpec import QuerySpec

SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent / "QueryInterpreter.md"


async def interpret_query(user_query: str) -> QuerySpec:
    system_prompt = SYSTEM_PROMPT_PATH.read_text().replace(
        "{{today}}", date.today().isoformat()
    )
    schema = json.dumps(QuerySpec.model_json_schema(), indent=2)

    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("openai_api_key"),
        
    )

    response = await client.chat.completions.create(
        model="google/gemini-3-flash-preview", 
        max_tokens=1024,
        response_format={"type": "json_object"}, 
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": (
                    f"Interpret this query:\n\n{user_query}\n\n"
                    "Respond with a single JSON object matching this schema — no markdown, no explanation:\n"
                    f"{schema}"
                ),
            }
        ],
    )


    text = response.choices[0].message.content.strip()
    
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        
    return QuerySpec.model_validate_json(text)