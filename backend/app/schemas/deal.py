"""Deal schemas."""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class DealBase(BaseModel):
    lead_id: UUID
    company: str
    contact_name: str | None = None
    value: str | None = None
    stage: str = "proposal_sent"
    checklist: list[dict] | None = None


class DealCreate(DealBase):
    pass


class DealResponse(DealBase):
    id: UUID
    discount_offered: float | None = None
    term_extension_days: int | None = None
    payment_terms: str | None = None
    workspace_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DealChecklistUpdate(BaseModel):
    checklist: list[dict]  # [{item: str, completed: bool}]


class DealFlagReview(BaseModel):
    reason: str
    agent_recommendation: str | None = None
