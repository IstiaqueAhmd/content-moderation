import logging
from fastapi import FastAPI, BackgroundTasks
from app.models import ModerationRequest
from app.database import block_content_in_db
from app.moderator import analyze_content

logger = logging.getLogger(__name__)

app = FastAPI(title="AI Moderation Microservice")

async def moderation_workflow(data: ModerationRequest):
    """Background job: calls OpenAI moderation and updates the DB status."""
    logger.info("Starting moderation analysis for content id=%s", data.id)
    is_flagged = await analyze_content(data.description, data.image, data.media)

    if is_flagged:
        logger.warning("Content id=%s flagged by moderation — blocking.", data.id)
        await block_content_in_db(data.id)
    else:
        logger.info("Content id=%s passed moderation.", data.id)

@app.post("/webhook/moderate", status_code=202)
async def moderate_content(request: ModerationRequest, background_tasks: BackgroundTasks):
    """
    Receives the payload from the main backend and queues the moderation task.
    Immediately returns 202 Accepted while the AI analysis runs in the background.
    """
    logger.info("Moderation request received for content id=%s", request.id)
    background_tasks.add_task(moderation_workflow, request)
    return {"message": "Moderation queued", "id": request.id}