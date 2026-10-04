"""Deal / closing routes."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.database import supabase_admin
from app.schemas.deal import DealCreate, DealResponse, DealChecklistUpdate, DealFlagReview

router = APIRouter()


@router.get("", response_model=list[DealResponse])
@router.get("/", include_in_schema=False, response_model=list[DealResponse])
async def list_deals(user: dict = Depends(get_current_user), stage: str | None = None):
    """List all deals, optionally filtered by stage."""
    ws = user["workspace_id"]
    q = supabase_admin.table("deal").select("*").eq("workspace_id", ws)

    if stage:
        q = q.eq("stage", stage)

    result = q.order("created_at", desc=True).execute()
    return result.data


@router.post("", response_model=DealResponse, status_code=201)
@router.post("/", include_in_schema=False, response_model=DealResponse, status_code=201)
async def create_deal(deal: DealCreate, user: dict = Depends(get_current_user)):
    """Create a new deal."""
    ws = user["workspace_id"]
    data = deal.model_dump()
    data["workspace_id"] = ws
    data["lead_id"] = str(data["lead_id"])

    result = supabase_admin.table("deal").insert(data).execute()
    return result.data[0]


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(deal_id: UUID, user: dict = Depends(get_current_user)):
    """Get a single deal."""
    ws = user["workspace_id"]
    result = supabase_admin.table("deal").select("*") \
        .eq("id", str(deal_id)).eq("workspace_id", ws).single().execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Deal not found")
    return result.data


@router.patch("/{deal_id}/checklist", response_model=DealResponse)
async def update_deal_checklist(deal_id: UUID, update: DealChecklistUpdate, user: dict = Depends(get_current_user)):
    """Update deal checklist items."""
    ws = user["workspace_id"]
    result = supabase_admin.table("deal").update({"checklist": update.checklist}) \
        .eq("id", str(deal_id)).eq("workspace_id", ws).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Deal not found")
    return result.data[0]


@router.post("/{deal_id}/flag-review")
async def flag_deal_for_review(deal_id: UUID, review: DealFlagReview, user: dict = Depends(get_current_user)):
    """Flag a deal for human review — creates an escalation."""
    ws = user["workspace_id"]

    # Fetch deal details
    deal = supabase_admin.table("deal").select("*") \
        .eq("id", str(deal_id)).eq("workspace_id", ws).single().execute()

    if not deal.data:
        raise HTTPException(status_code=404, detail="Deal not found")

    # Create escalation
    supabase_admin.table("escalation").insert({
        "lead_id": deal.data["lead_id"],
        "title": review.reason,
        "source_agent": "closing_agent",
        "contact_info": f"{deal.data.get('contact_name', '')} · {deal.data.get('company', '')}",
        "summary": review.agent_recommendation or review.reason,
        "workspace_id": ws,
    }).execute()

    # Log activity
    supabase_admin.table("activity_log").insert({
        "lead_id": deal.data["lead_id"],
        "agent_name": "Closing Agent",
        "description": f"Flagged {deal.data.get('company', 'deal')} for human review: {review.reason}",
        "workspace_id": ws,
    }).execute()

    return {"message": "Deal flagged for review", "escalation_created": True}
