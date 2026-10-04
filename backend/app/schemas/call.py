"""Call schemas."""

from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel


class CallBase(BaseModel):
    lead_id: UUID
    scheduled_at: datetime
    voice_profile: str = "Sarah (Warm Consultative)"


class CallCreate(CallBase):
    pass


class CallResponse(BaseModel):
    id: UUID
    lead_id: UUID
    scheduled_at: datetime
    status: str
    duration: str | None = None
    transcript: list[dict] | None = None
    notes_summary: dict | None = None
    interest_level: str | None = None
    next_step: str | None = None
    follow_up_date: date | None = None
    voice_profile: str | None = None
    recording_url: str | None = None
    workspace_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class CallQueueResponse(BaseModel):
    """Today's call queue."""
    date: str
    calls: list[CallResponse]
    total: int
    completed: int
    pending: int
