import os
import asyncio
from typing import Optional, List
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Extensions considered images (videos and other files are skipped)
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}

def _is_image_url(url: str) -> bool:
    """Returns True if the URL points to a recognised image format."""
    path = url.split("?")[0].lower()  # strip query params before checking ext
    return any(path.endswith(ext) for ext in IMAGE_EXTENSIONS)

async def _moderate(inputs: list) -> bool:
    """Run a single moderation request and return whether it was flagged."""
    response = await client.moderations.create(
        model="omni-moderation-latest",
        input=inputs,
    )
    return response.results[0].flagged

async def analyze_content(
    description: str,
    image: Optional[str],
    media: Optional[List[str]],
) -> bool:
    """
    Sends description text and image URLs to OpenAI's omni-moderation-latest.
    The API allows at most 1 image per request, so each image is checked in a
    separate call (paired with the description text).  A text-only call is
    always made as well.  Returns True if *any* call is flagged, False if clean.
    """
    # Collect all image URLs to check
    image_urls: List[str] = []
    if image:
        image_urls.append(image)
    if media:
        image_urls.extend(url for url in media if _is_image_url(url))

    # Build one task per image (each paired with the text) + a text-only task
    tasks: List[asyncio.Task] = []

    # Text-only moderation
    tasks.append(_moderate([{"type": "text", "text": description}]))

    # One call per image (API limit: 1 image per request)
    for url in image_urls:
        tasks.append(_moderate([
            {"type": "text", "text": description},
            {"type": "image_url", "image_url": {"url": url}},
        ]))

    results = await asyncio.gather(*tasks)
    return any(results)