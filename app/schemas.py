from datetime import datetime

from pydantic import BaseModel

class PostRequest(BaseModel):
    name: str
    description: str


class PostResponse(BaseModel):
    name: str
    description: str
    created_at: datetime
    author: str

