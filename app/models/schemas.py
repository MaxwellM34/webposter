from datetime import datetime
from pydantic import BaseModel


class postCreate(BaseModel):
    caption: str
    content: str


class postResponse(BaseModel):
    caption: str
    content: str
    created_at: datetime

class userCreate(BaseModel):
    email: str
    firstname: str
    lastname: str