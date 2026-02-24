import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

DATABASE_URL = os.getenv("DATABASE_URL")
client = AsyncIOMotorClient(DATABASE_URL)
db = client["jurnee-app"]
collection = db["posts"]

async def update_content_status(document_id: str, status: str):
    """
    Updates a document's status field.
    status must be one of: 'BLOCKED', 'PENDING', 'PUBLISHED'.
    """
    try:
        result = await collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": {"status": status}}
        )
        if result.modified_count:
            print(f"Document {document_id} status set to {status}.")
        else:
            print(f"Document {document_id} not found or already at status {status}.")
    except Exception as e:
        print(f"Database error for {document_id}: {e}")

async def block_content_in_db(document_id: str):
    await update_content_status(document_id, "BLOCKED")