"""ActivityLog model — every agent action, powering the live activity feed."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.models.user import Base


class ActivityLog(Base):
    __tablename__ = "activity_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("lead.id"), nullable=True)
    agent_name = Column(String, nullable=False)               # "Contact Finder", "Outreach Agent", etc.
    description = Column(String, nullable=False)              # "Found a high-fit contact at Northstar Labs"
    initials = Column(String)                                 # Lead's initials for avatar
    tone = Column(String)                                     # Lead's tone for avatar color
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
