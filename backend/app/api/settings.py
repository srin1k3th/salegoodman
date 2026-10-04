"""Settings routes — workspace config + per-agent guardrails."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.database import supabase_admin
from app.schemas.agent_config import AgentConfigResponse, AgentConfigUpdate

router = APIRouter()

VALID_AGENT_TYPES = {"contact_finder", "outreach", "follow_up", "closing", "orchestrator"}


# ── Workspace Settings ────────────────────────────────────────

@router.get("/workspace")
async def get_workspace_settings(user: dict = Depends(get_current_user)):
    """Get workspace profile and notification settings."""
    ws = user["workspace_id"]
    result = supabase_admin.table("workspace").select("*").eq("id", ws).single().execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return result.data


@router.put("/workspace")
async def update_workspace_settings(update: dict, user: dict = Depends(get_current_user)):
    """Update workspace name, timezone, notification prefs, etc."""
    ws = user["workspace_id"]

    # Only allow certain fields
    allowed = {"name", "domain", "timezone", "notification_prefs", "safety_killswitch"}
    filtered = {k: v for k, v in update.items() if k in allowed}

    result = supabase_admin.table("workspace").update(filtered).eq("id", ws).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return result.data[0]


# ── Agent Config ──────────────────────────────────────────────

@router.get("/agents/{agent_type}", response_model=AgentConfigResponse)
async def get_agent_config(agent_type: str, user: dict = Depends(get_current_user)):
    """Get configuration for a specific agent."""
    if agent_type not in VALID_AGENT_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid agent type. Must be one of: {VALID_AGENT_TYPES}")

    ws = user["workspace_id"]
    result = supabase_admin.table("agent_config").select("*") \
        .eq("workspace_id", ws).eq("agent_type", agent_type).single().execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Agent config not found")
    return result.data


@router.put("/agents/{agent_type}", response_model=AgentConfigResponse)
async def update_agent_config(agent_type: str, update: AgentConfigUpdate, user: dict = Depends(get_current_user)):
    """Update agent guardrails and settings."""
    if agent_type not in VALID_AGENT_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid agent type. Must be one of: {VALID_AGENT_TYPES}")

    ws = user["workspace_id"]
    result = supabase_admin.table("agent_config").update({"config": update.config}) \
        .eq("workspace_id", ws).eq("agent_type", agent_type).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Agent config not found")

    # Log activity
    supabase_admin.table("activity_log").insert({
        "agent_name": "Orchestrator",
        "description": f"Agent config updated: {agent_type}",
        "workspace_id": ws,
    }).execute()

    return result.data[0]


# ── Team Management ───────────────────────────────────────────

@router.get("/team")
async def list_team(user: dict = Depends(get_current_user)):
    """List all team members in the workspace."""
    ws = user["workspace_id"]
    result = supabase_admin.table("user").select("*").eq("workspace_id", ws).execute()
    return result.data


@router.post("/team/invite")
async def invite_team_member(invite: dict, user: dict = Depends(get_current_user)):
    """Invite a team member (creates a placeholder user)."""
    ws = user["workspace_id"]
    email = invite.get("email", "")
    role = invite.get("role", "Sales Representative")

    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    prefix = email.split("@")[0]
    name = prefix.capitalize()
    initials = prefix[:2].upper()

    result = supabase_admin.table("user").insert({
        "email": email,
        "name": name,
        "role": role,
        "initials": initials,
        "tone": "green",
        "workspace_id": ws,
    }).execute()

    return {"message": f"Invitation sent to {email}", "user": result.data[0]}


@router.delete("/team/{member_id}", status_code=204)
async def remove_team_member(member_id: UUID, user: dict = Depends(get_current_user)):
    """Remove a team member from the workspace."""
    ws = user["workspace_id"]
    supabase_admin.table("user").delete() \
        .eq("id", str(member_id)).eq("workspace_id", ws).execute()
