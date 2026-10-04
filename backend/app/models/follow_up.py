"""FollowUp model — scheduled touches on the cadence engine."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.models.user import Base


class FollowUp(Base):
    __tablename__ = "follow_up"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("lead.id"))
    touch_number = Column(Integer, nullable=False)         # 1, 2, 3, 4
    type = Column(String, default="email")                  # "email", "call", "linkedin"
    message_subject = Column(String)
    message_body = Column(String)
    temperature = Column(String, nullable=False, default="warm")  # "warm", "cold", "escalated"
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="scheduled")            # "scheduled", "sent", "replied", "paused", "escalated"
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
