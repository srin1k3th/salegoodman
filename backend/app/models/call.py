"""Call model — outreach call records with transcripts and AI notes."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, ForeignKey, DateTime, Date, JSON
from sqlalchemy.dialects.postgresql import UUID

from app.models.user import Base


class Call(Base):
    __tablename__ = "call"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("lead.id"))
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False, default="pending")  # "pending", "completed", "no_answer", "cancelled"
    duration = Column(String)                                     # "8m 24s"
    transcript = Column(JSON)                                     # [{speaker, text, ts}]
    notes_summary = Column(JSON)                                  # {interest_level, next_step, buying_signals}
    interest_level = Column(String)                               # "warm", "cold", "hot"
    next_step = Column(String)                                    # "Send proposal"
    follow_up_date = Column(Date)
    voice_profile = Column(String, default="Sarah (Warm Consultative)")
    recording_url = Column(String)                                # Supabase Storage URL
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
