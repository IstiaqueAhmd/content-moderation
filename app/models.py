from pydantic import BaseModel
from typing import List, Optional

class ModerationRequest(BaseModel):
    description: str
    image: Optional[str] = None
    media: Optional[List[str]] = None
    id: str