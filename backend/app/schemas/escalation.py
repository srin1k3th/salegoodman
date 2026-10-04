"""Escalation schemas."""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class EscalationBase(BaseModel):
    lead_id: UUID
    title: str
    source_agent: str
    contact_info: str | None = None
    summary: str | None = None


class EscalationCreate(EscalationBase):
    pass


class EscalationResponse(EscalationBase):
    id: UUID
    status: str
    resolution: str | None = None
    resolved_by: UUID | None = None
    workspace_id: UUID
    created_at: datetime
    resolved_at: datetime | None = None

    model_config = {"from_attributes": True}


class EscalationAction(BaseModel):
    """Action taken on an escalation (approve/reject/takeover)."""
    resolution: str | None = None
    notes: str | None = None
