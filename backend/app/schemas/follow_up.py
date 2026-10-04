"""Follow-up schemas."""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class FollowUpBase(BaseModel):
    lead_id: UUID
    touch_number: int
    type: str = "email"
    message_subject: str | None = None
    message_body: str | None = None
    temperature: str = "warm"
    scheduled_at: datetime


class FollowUpCreate(FollowUpBase):
    pass


class FollowUpResponse(FollowUpBase):
    id: UUID
    status: str
    workspace_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class FollowUpStatusUpdate(BaseModel):
    status: str  # "scheduled", "sent", "replied", "paused", "escalated"


class CalendarResponse(BaseModel):
    """Calendar view of follow-ups grouped by date."""
    date: str
    items: list[FollowUpResponse]
