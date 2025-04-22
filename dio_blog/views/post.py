from pydantic import AwareDatetime, BaseModel, NaiveDatetime


class PostOut(BaseModel):  # Out - > Response
    id: int
    title: str
    content: str
    published_at: AwareDatetime | NaiveDatetime | None
