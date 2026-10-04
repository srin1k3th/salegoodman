"""Escalation model — items requiring human judgment."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.models.user import Base


class Escalation(Base):
    __tablename__ = "escalation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("lead.id"))
    title = Column(String, nullable=False)                    # "Pricing objection from Maya Chen"
    source_agent = Column(String, nullable=False)             # "closing_agent", "outreach_agent", etc.
    contact_info = Column(String)                             # "Maya Chen · Northstar Labs"
    summary = Column(String)                                  # Detailed explanation
    status = Column(String, default="pending")                # "pending", "approved", "rejected", "taken_over"
    resolution = Column(String)                               # Founder's notes
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    resolved_at = Column(DateTime(timezone=True))
