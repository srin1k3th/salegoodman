"""
SaleGoodman — SQLAlchemy ORM Models

All models are defined here for Alembic migrations and type reference.
The actual data access goes through the Supabase client, but these models
serve as the canonical schema definition.
"""

from app.models.user import User, Workspace
from app.models.contact import Contact
from app.models.lead import Lead
from app.models.call import Call
from app.models.follow_up import FollowUp
from app.models.deal import Deal
from app.models.escalation import Escalation
from app.models.activity import ActivityLog
from app.models.agent_config import AgentConfig

__all__ = [
    "User",
    "Workspace",
    "Contact",
    "Lead",
    "Call",
    "FollowUp",
    "Deal",
    "Escalation",
    "ActivityLog",
    "AgentConfig",
]
