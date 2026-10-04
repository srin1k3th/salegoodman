"""Lead model — the shared record traveling through the pipeline."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID

from app.models.user import Base


class Lead(Base):
    __tablename__ = "lead"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contact.id"))
    stage = Column(String, nullable=False, default="Found")  # Found → Contacted → Following Up → Closing → Won | Lost
    value = Column(String)                                     # "$48,000"
    company = Column(String)                                   # Denormalized for pipeline view
    initials = Column(String)
    tone = Column(String)
    agent_notes = Column(JSON, default=dict)
    last_touched = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
