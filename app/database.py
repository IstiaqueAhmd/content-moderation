import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

DATABASE_URL = os.getenv("DATABASE_URL")
client = AsyncIOMotorClient(DATABASE_URL)
db = client["jurnee-app"]
collection = db["posts"]

async def block_content_in_db(document_id: ObjectId):
    """Updates the document status to BLOCKED."""
    try:
        await collection.update_one(
            {"_id": document_id},
            {"$set": {"status": "BLOCKED"}}
        )
        print(f"Document {document_id} blocked successfully.")
    except Exception as e:
        print(f"Database error for {document_id}: {e}")