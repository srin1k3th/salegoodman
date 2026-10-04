"""Agent config schemas."""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class AgentConfigResponse(BaseModel):
    id: UUID
    agent_type: str
    config: dict
    workspace_id: UUID
    updated_at: datetime

    model_config = {"from_attributes": True}


class AgentConfigUpdate(BaseModel):
    config: dict
