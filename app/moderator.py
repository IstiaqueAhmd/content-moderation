import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_content(description: str, image_url: str) -> bool:
    """
    Sends description text and image URL to OpenAI's omni-moderation-latest model.
    Returns True if any content is flagged, False if clean.
    """
    response = await client.moderations.create(
        model="omni-moderation-latest",
        input=[
            {"type": "text", "text": description},
            {
                "type": "image_url",
                "image_url": {"url": image_url},
            },
        ],
    )

    result = response.results[0]
    return result.flagged