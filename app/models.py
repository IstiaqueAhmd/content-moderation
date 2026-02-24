from pydantic import BaseModel

class ModerationRequest(BaseModel):
    description: str
    image: str
    id: str 