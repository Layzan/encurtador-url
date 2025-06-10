from pydantic import BaseModel

class URL(BaseModel):
    original_url: str
