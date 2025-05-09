from pydantic import AwareDatetime, BaseModel


class PostIn(BaseModel):  # In - > Request
    title: str
    content: str
    published_at: AwareDatetime | None = None
    published: bool | None = None


class PostUpdateIn(BaseModel):
    title: str | None = None  # or Optional[str] = None
    content: str | None = None
    published_at: AwareDatetime | None = None
    published: bool | None = None
