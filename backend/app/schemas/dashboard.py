"""Dashboard schemas — aggregated metrics responses."""

from pydantic import BaseModel


class FunnelStage(BaseModel):
    stage: str
    count: int


class AgentHealth(BaseModel):
    agent: str
    status: str
    detail: str
    uptime_pct: int


class DashboardMetrics(BaseModel):
    total_leads: int
    total_leads_change: str
    active_conversations: int
    active_conversations_change: str
    deals_closed_this_week: int
    deals_closed_change: str
    escalations_pending: int
    escalations_change: str
    funnel: list[FunnelStage]
    agent_health: list[AgentHealth]
    pipeline_value: str
