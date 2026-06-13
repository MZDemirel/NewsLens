from datetime import datetime

from pydantic import BaseModel, EmailStr


# --- Auth ---

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- News ---

class NewsOut(BaseModel):
    id: int
    source: str
    title: str
    summary: str | None
    url: str
    category: str | None
    published_at: datetime | None
    fetched_at: datetime

    model_config = {"from_attributes": True}


class NewsDetail(NewsOut):
    full_text: str | None


# --- Interactions ---

class InteractionCreate(BaseModel):
    news_id: int
    action: str
    dwell_time_sec: int | None = None


class InteractionOut(BaseModel):
    id: int
    user_id: int
    news_id: int
    action: str
    dwell_time_sec: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
