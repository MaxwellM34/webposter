from pydantic import BaseModel


class postCreate(BaseModel):
    title: str
    content: str

class postResponse(BaseModel):
    title: str
    content: str