"""Lead schemas."""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class LeadBase(BaseModel):
    contact_id: UUID | None = None
    stage: str = "Found"
    value: str | None = None
    company: str | None = None
    initials: str | None = None
    tone: str | None = None
    agent_notes: dict | None = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    stage: str | None = None
    value: str | None = None
    agent_notes: dict | None = None


class LeadResponse(LeadBase):
    id: UUID
    last_touched: datetime
    workspace_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class LeadStageUpdate(BaseModel):
    stage: str  # "Found", "Contacted", "Following Up", "Closing", "Won", "Lost"


class PipelineResponse(BaseModel):
    """Kanban-style pipeline view grouped by stage."""
    found: list[LeadResponse] = []
    contacted: list[LeadResponse] = []
    following_up: list[LeadResponse] = []
    closing: list[LeadResponse] = []
    won: list[LeadResponse] = []
    lost: list[LeadResponse] = []
