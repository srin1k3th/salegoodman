"""Activity log schemas."""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class ActivityBase(BaseModel):
    agent_name: str
    description: str
    lead_id: UUID | None = None
    initials: str | None = None
    tone: str | None = None


class ActivityCreate(ActivityBase):
    pass


class ActivityResponse(ActivityBase):
    id: UUID
    workspace_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}
