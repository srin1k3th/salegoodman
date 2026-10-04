"""Contact model — prospects discovered by the Contact Finding agent."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.models.user import Base


class Contact(Base):
    __tablename__ = "contact"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    role = Column(String)
    company = Column(String)
    location = Column(String)
    relevance_score = Column(Integer, default=0)
    initials = Column(String)
    tone = Column(String, default="blue")
    source = Column(String, default="agent")           # "agent", "manual", "import"
    status = Column(String, default="new")             # "new", "warm", "cold", "archived"
    email = Column(String)
    phone = Column(String)
    last_contacted = Column(Date)
    enriched = Column(Boolean, default=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
