"""AgentConfig model — per-agent settings and guardrails."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, ForeignKey, DateTime, JSON, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.user import Base


class AgentConfig(Base):
    __tablename__ = "agent_config"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_type = Column(String, nullable=False)  # "contact_finder", "outreach", "follow_up", "closing", "orchestrator"
    config = Column(JSON, nullable=False)         # Agent-specific config JSONB
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    workspace = relationship("Workspace", back_populates="agent_configs")

    __table_args__ = (
        UniqueConstraint("workspace_id", "agent_type", name="uq_workspace_agent"),
    )


# ── Default Agent Configurations ─────────────────────────────
# These match the frontend Settings page defaults exactly.

DEFAULT_CONFIGS = {
    "contact_finder": {
        "formality": 3,
        "directness": 4,
        "daily_quota": 50,
        "min_fit_score": 85,
        "auto_enrich": True,
        "escalate_enterprise": True,
    },
    "outreach": {
        "formality": 2,
        "directness": 4,
        "voice_profile": "Sarah (Warm Consultative)",
        "daily_limit": 25,
        "escalate_competitor": True,
        "escalate_integration": True,
        "sentiment_guardrail": True,
    },
    "follow_up": {
        "formality": 3,
        "directness": 4,
        "touch_days": [1, 4, 8, 14],
        "max_touches": 4,
        "auto_pause": True,
        "escalate_unanswered": 3,
    },
    "closing": {
        "formality": 4,
        "directness": 3,
        "max_discount_pct": 15,
        "max_term_extension_days": 30,
        "payment_terms": "Allow Net 45 without approval",
        "mutual_nda": True,
        "strict_redlines": True,
    },
    "orchestrator": {
        "confidence_threshold": 90,
        "coordination_mode": "Adaptive Parallel Hand-off",
        "briefing_time": "8:30 AM",
        "safety_switch": False,
    },
}
