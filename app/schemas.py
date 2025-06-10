from pydantic import BaseModel

class URLResponse(BaseModel):
    original_url: str
    short_url: str

    class Config:
        orm_mode = True
