import logging
import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
client = AsyncIOMotorClient(DATABASE_URL)
db = client[os.getenv("DATABASE_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

async def update_content_status(document_id: str, status: str):
    """
    Updates a document's status field.
    status must be one of: 'BLOCKED', 'SUSPICIOUS', 'PUBLISHED'.
    """
    try:
        result = await collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": {"status": status}}
        )
        if result.modified_count:
            logger.info("Document %s status set to %s.", document_id, status)
        else:
            logger.warning("Document %s not found or already at status %s.", document_id, status)
    except Exception as e:
        logger.error("Database error for document %s: %s", document_id, e, exc_info=True)

# Convenience helpers kept for backward compatibility
async def block_content_in_db(document_id: str):
    await update_content_status(document_id, "BLOCKED")

async def publish_content_in_db(document_id: str):
    await update_content_status(document_id, "PUBLISHED")