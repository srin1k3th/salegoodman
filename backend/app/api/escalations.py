"""Escalation inbox routes."""

from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.database import supabase_admin
from app.schemas.escalation import EscalationResponse, EscalationAction

router = APIRouter()


@router.get("", response_model=list[EscalationResponse])
@router.get("/", include_in_schema=False, response_model=list[EscalationResponse])
async def list_escalations(user: dict = Depends(get_current_user), status: str = "pending"):
    """List escalations, defaulting to pending."""
    ws = user["workspace_id"]
    q = supabase_admin.table("escalation").select("*").eq("workspace_id", ws)

    if status != "all":
        q = q.eq("status", status)

    result = q.order("created_at", desc=True).execute()
    return result.data


@router.post("/{escalation_id}/approve", response_model=EscalationResponse)
async def approve_escalation(escalation_id: UUID, action: EscalationAction, user: dict = Depends(get_current_user)):
    """Approve an escalation — agent proceeds with recommended action."""
    return await _resolve_escalation(escalation_id, "approved", action, user)


@router.post("/{escalation_id}/reject", response_model=EscalationResponse)
async def reject_escalation(escalation_id: UUID, action: EscalationAction, user: dict = Depends(get_current_user)):
    """Reject an escalation — agent's recommendation is overridden."""
    return await _resolve_escalation(escalation_id, "rejected", action, user)


@router.post("/{escalation_id}/takeover", response_model=EscalationResponse)
async def takeover_escalation(escalation_id: UUID, action: EscalationAction, user: dict = Depends(get_current_user)):
    """Take over — founder handles this lead personally."""
    return await _resolve_escalation(escalation_id, "taken_over", action, user)


async def _resolve_escalation(escalation_id: UUID, status: str, action: EscalationAction, user: dict):
    """Shared resolution logic."""
    ws = user["workspace_id"]
    now = datetime.now(timezone.utc).isoformat()

    result = supabase_admin.table("escalation").update({
        "status": status,
        "resolution": action.resolution or action.notes or f"{status} by {user['name']}",
        "resolved_by": user["user_id"],
        "resolved_at": now,
    }).eq("id", str(escalation_id)).eq("workspace_id", ws).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Escalation not found")

    # Log activity
    esc = result.data[0]
    supabase_admin.table("activity_log").insert({
        "lead_id": esc.get("lead_id"),
        "agent_name": "Orchestrator",
        "description": f"Escalation {status}: {esc.get('title', '')}",
        "workspace_id": ws,
    }).execute()

    return result.data[0]
