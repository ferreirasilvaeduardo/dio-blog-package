from datetime import datetime

from pydantic import BaseModel


class PostOut(BaseModel):  # Out - > Response
    id: int
    title: str
    content: str
    published_at: datetime | None
