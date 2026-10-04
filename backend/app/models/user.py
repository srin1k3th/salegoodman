"""User and Workspace models."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class Workspace(Base):
    __tablename__ = "workspace"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    domain = Column(String)
    timezone = Column(String, nullable=False, default="America/Chicago")
    notification_prefs = Column(JSON, default=dict)
    safety_killswitch = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    users = relationship("User", back_populates="workspace")
    agent_configs = relationship("AgentConfig", back_populates="workspace")


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="Sales Representative")
    initials = Column(String)
    tone = Column(String, default="blue")
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    workspace = relationship("Workspace", back_populates="users")
