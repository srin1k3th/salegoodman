"""Contact schemas."""

from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel


class ContactBase(BaseModel):
    name: str
    role: str | None = None
    company: str | None = None
    location: str | None = None
    relevance_score: int = 0
    initials: str | None = None
    tone: str = "blue"
    source: str = "agent"
    status: str = "new"
    email: str | None = None
    phone: str | None = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    company: str | None = None
    location: str | None = None
    relevance_score: int | None = None
    status: str | None = None
    email: str | None = None
    phone: str | None = None


class ContactResponse(ContactBase):
    id: UUID
    last_contacted: date | None = None
    enriched: bool = False
    workspace_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class ContactSearchParams(BaseModel):
    query: str = ""
    min_score: int | None = None
    status: str | None = None
    source: str | None = None
    limit: int = 50
    offset: int = 0
