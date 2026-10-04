"""Leads CRUD + pipeline routes."""

from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import get_current_user
from app.database import supabase_admin
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse, LeadStageUpdate, PipelineResponse

router = APIRouter()


@router.get("", response_model=list[LeadResponse])
@router.get("/", include_in_schema=False, response_model=list[LeadResponse])
async def list_leads(
    user: dict = Depends(get_current_user),
    stage: str | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
):
    """List leads with optional stage filter."""
    ws = user["workspace_id"]
    q = supabase_admin.table("lead").select("*").eq("workspace_id", ws)

    if stage:
        q = q.eq("stage", stage)

    result = q.order("last_touched", desc=True).range(offset, offset + limit - 1).execute()
    return result.data


@router.post("", response_model=LeadResponse, status_code=201)
@router.post("/", include_in_schema=False, response_model=LeadResponse, status_code=201)
async def create_lead(lead: LeadCreate, user: dict = Depends(get_current_user)):
    """Create a new lead from a contact."""
    ws = user["workspace_id"]
    data = lead.model_dump()
    data["workspace_id"] = ws
    if data.get("contact_id"):
        data["contact_id"] = str(data["contact_id"])

    result = supabase_admin.table("lead").insert(data).execute()
    return result.data[0]


@router.get("/pipeline", response_model=PipelineResponse)
async def get_pipeline(user: dict = Depends(get_current_user)):
    """Kanban-style pipeline view grouped by stage."""
    ws = user["workspace_id"]
    result = supabase_admin.table("lead").select("*") \
        .eq("workspace_id", ws) \
        .order("last_touched", desc=True) \
        .execute()

    pipeline = PipelineResponse()
    for lead in result.data:
        stage = lead["stage"]
        if stage == "Found":
            pipeline.found.append(lead)
        elif stage == "Contacted":
            pipeline.contacted.append(lead)
        elif stage == "Following Up":
            pipeline.following_up.append(lead)
        elif stage == "Closing":
            pipeline.closing.append(lead)
        elif stage == "Won":
            pipeline.won.append(lead)
        elif stage == "Lost":
            pipeline.lost.append(lead)

    return pipeline


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: UUID, user: dict = Depends(get_current_user)):
    """Get a single lead by ID."""
    ws = user["workspace_id"]
    result = supabase_admin.table("lead").select("*") \
        .eq("id", str(lead_id)).eq("workspace_id", ws).single().execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Lead not found")
    return result.data


@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(lead_id: UUID, update: LeadUpdate, user: dict = Depends(get_current_user)):
    """Update a lead."""
    ws = user["workspace_id"]
    data = update.model_dump(exclude_unset=True)
    data["last_touched"] = datetime.now(timezone.utc).isoformat()

    result = supabase_admin.table("lead").update(data) \
        .eq("id", str(lead_id)).eq("workspace_id", ws).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Lead not found")
    return result.data[0]


@router.patch("/{lead_id}/stage", response_model=LeadResponse)
async def update_lead_stage(lead_id: UUID, stage_update: LeadStageUpdate, user: dict = Depends(get_current_user)):
    """Transition a lead to a new pipeline stage."""
    valid_stages = {"Found", "Contacted", "Following Up", "Closing", "Won", "Lost"}
    if stage_update.stage not in valid_stages:
        raise HTTPException(status_code=400, detail=f"Invalid stage. Must be one of: {valid_stages}")

    ws = user["workspace_id"]
    result = supabase_admin.table("lead").update({
        "stage": stage_update.stage,
        "last_touched": datetime.now(timezone.utc).isoformat(),
    }).eq("id", str(lead_id)).eq("workspace_id", ws).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Lead not found")

    # Log activity
    lead = result.data[0]
    supabase_admin.table("activity_log").insert({
        "lead_id": str(lead_id),
        "agent_name": "Orchestrator",
        "description": f"Lead moved to {stage_update.stage}",
        "initials": lead.get("initials"),
        "tone": lead.get("tone"),
        "workspace_id": ws,
    }).execute()

    return result.data[0]
