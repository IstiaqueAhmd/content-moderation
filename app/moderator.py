import asyncio

async def analyze_content(description: str, image_url: str) -> bool:
    """
    Pass the description and image to your AI model here.
    Returns True if flagged, False if clean.
    """
    # TODO: Insert your actual AI provider SDK code here (OpenAI, Gemini, etc.)
    # Example mock delay to simulate AI processing:
    await asyncio.sleep(2) 
    
    # Mock logic: flag if the word "bad" is in the description
    if "bad" in description.lower():
        return True
    
    return False