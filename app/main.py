from fastapi import FastAPI, BackgroundTasks
from app.models import ModerationRequest
from app.database import block_content_in_db
from app.moderator import analyze_content

app = FastAPI(title="AI Moderation Microservice")

async def moderation_workflow(data: ModerationRequest):
    """The background job that runs the AI and updates the DB."""
    is_flagged = await analyze_content(data.description, data.image)
    
    if is_flagged:
        await block_content_in_db(data.id)

@app.post("/webhook/moderate", status_code=202)
async def moderate_content(request: ModerationRequest, background_tasks: BackgroundTasks):
    """
    Receives the payload from the main backend and queues the moderation task.
    """
    # Add the workflow to background tasks
    background_tasks.add_task(moderation_workflow, request)
    
    # Immediately return success to the main backend
    return {"message": "Moderation queued", "id": request.id}