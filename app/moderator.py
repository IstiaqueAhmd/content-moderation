import os
from typing import Optional, List
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Extensions considered images (videos and other files are skipped)
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}

def _is_image_url(url: str) -> bool:
    """Returns True if the URL points to a recognised image format."""
    path = url.split("?")[0].lower()  # strip query params before checking ext
    return any(path.endswith(ext) for ext in IMAGE_EXTENSIONS)

async def analyze_content(
    description: str,
    image: Optional[str],
    media: Optional[List[str]],
) -> bool:
    """
    Sends description text and all image URLs to OpenAI's omni-moderation-latest.
    - `image`  : single optional cover image URL
    - `media`  : optional list of mixed media URLs (videos are silently skipped)
    Returns True if any content is flagged, False if clean.
    """
    inputs = [{"type": "text", "text": description}]

    # Add the single cover image if provided
    if image:
        inputs.append({"type": "image_url", "image_url": {"url": image}})

    # Add only image URLs from the media list (skip videos and other types)
    if media:
        for url in media:
            if _is_image_url(url):
                inputs.append({"type": "image_url", "image_url": {"url": url}})

    response = await client.moderations.create(
        model="omni-moderation-latest",
        input=inputs,
    )

    return response.results[0].flagged