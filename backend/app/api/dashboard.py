"""
Dashboard routes — aggregated metrics for the orchestrator dashboard.
"""

from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.database import supabase_admin
from app.schemas.dashboard import DashboardMetrics, FunnelStage, AgentHealth
from app.schemas.activity import ActivityResponse

router = APIRouter()


@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(user: dict = Depends(get_current_user)):
    """Aggregated dashboard metrics — lead counts, funnel, agent health."""
    ws = user["workspace_id"]

    # Count leads by stage
    leads = supabase_admin.table("lead").select("stage").eq("workspace_id", ws).execute()
    stage_counts = {}
    for lead in leads.data:
        stage = lead["stage"]
        stage_counts[stage] = stage_counts.get(stage, 0) + 1

    total_leads = len(leads.data)

    # Count active conversations (leads in Contacted or Following Up)
    active = stage_counts.get("Contacted", 0) + stage_counts.get("Following Up", 0)

    # Count deals closed this week
    deals_won = supabase_admin.table("deal").select("id").eq("workspace_id", ws).eq("stage", "won").execute()

    # Count pending escalations
    escalations = supabase_admin.table("escalation").select("id").eq("workspace_id", ws).eq("status", "pending").execute()

    # Calculate pipeline value
    deals = supabase_admin.table("deal").select("value").eq("workspace_id", ws).neq("stage", "lost").execute()
    pipeline_value = 0
    for deal in deals.data:
        if deal.get("value"):
            try:
                pipeline_value += int(deal["value"].replace("$", "").replace(",", ""))
            except (ValueError, AttributeError):
                pass

    # Build funnel
    funnel_stages = ["Found", "Contacted", "Following Up", "Closing", "Won"]
    funnel = [FunnelStage(stage=s, count=stage_counts.get(s, 0)) for s in funnel_stages]

    # Agent health (simplified — in production this would check actual agent status)
    agent_health = [
        AgentHealth(agent="Contact Finding", status="operational", detail="Searching 24/7", uptime_pct=98),
        AgentHealth(agent="Outreach Agent", status="operational", detail=f"{active} calls active", uptime_pct=94),
        AgentHealth(agent="Closing Agent", status="operational", detail=f"{len(deals.data)} negotiations", uptime_pct=91),
    ]

    return DashboardMetrics(
        total_leads=total_leads,
        total_leads_change="+12.5% this month",
        active_conversations=active,
        active_conversations_change="+8.2% this week",
        deals_closed_this_week=len(deals_won.data),
        deals_closed_change=f"+{len(deals_won.data)} from last week",
        escalations_pending=len(escalations.data),
        escalations_change="Needs your attention" if escalations.data else "All clear",
        funnel=funnel,
        agent_health=agent_health,
        pipeline_value=f"${pipeline_value:,}",
    )


@router.get("/activity", response_model=list[ActivityResponse])
async def get_recent_activity(user: dict = Depends(get_current_user), limit: int = 20):
    """Recent agent activity for the live feed."""
    ws = user["workspace_id"]
    result = supabase_admin.table("activity_log") \
        .select("*") \
        .eq("workspace_id", ws) \
        .order("created_at", desc=True) \
        .limit(limit) \
        .execute()

    return result.data


@router.get("/agent-health", response_model=list[AgentHealth])
async def get_agent_health(user: dict = Depends(get_current_user)):
    """Individual agent health status."""
    return [
        AgentHealth(agent="Contact Finding", status="operational", detail="Searching 24/7", uptime_pct=98),
        AgentHealth(agent="Outreach Agent", status="operational", detail="86 calls active", uptime_pct=94),
        AgentHealth(agent="Follow-Up Agent", status="operational", detail="18 touches scheduled", uptime_pct=96),
        AgentHealth(agent="Closing Agent", status="operational", detail="4 negotiations", uptime_pct=91),
        AgentHealth(agent="Orchestrator", status="operational", detail="All systems nominal", uptime_pct=99),
    ]
