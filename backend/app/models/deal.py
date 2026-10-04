"""Deal model — active negotiations managed by the Closing agent."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID

from app.models.user import Base


class Deal(Base):
    __tablename__ = "deal"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("lead.id"))
    company = Column(String, nullable=False)
    contact_name = Column(String)
    value = Column(String)                                      # "$48,000"
    stage = Column(String, nullable=False, default="proposal_sent")  # "proposal_sent", "in_negotiation", "contract_review", "won", "lost"
    checklist = Column(JSON, default=list)                       # [{item, completed}]
    discount_offered = Column(Numeric(5, 2))                     # Percentage
    term_extension_days = Column(Integer)
    payment_terms = Column(String)                               # "Net 30", "Net 45"
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
