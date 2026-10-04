"""Follow-up cadence routes."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import get_current_user
from app.database import supabase_admin
from app.schemas.follow_up import FollowUpCreate, FollowUpResponse, FollowUpStatusUpdate, CalendarResponse

router = APIRouter()


@router.get("", response_model=list[FollowUpResponse])
@router.get("/", include_in_schema=False, response_model=list[FollowUpResponse])
async def list_follow_ups(
    user: dict = Depends(get_current_user),
    status: str | None = None,
    temperature: str | None = None,
    limit: int = Query(default=50, le=200),
):
    """List follow-ups with optional filters."""
    ws = user["workspace_id"]
    q = supabase_admin.table("follow_up").select("*").eq("workspace_id", ws)

    if status:
        q = q.eq("status", status)
    if temperature:
        q = q.eq("temperature", temperature)

    result = q.order("scheduled_at").limit(limit).execute()
    return result.data


@router.post("/", response_model=FollowUpResponse, status_code=201)
async def create_follow_up(follow_up: FollowUpCreate, user: dict = Depends(get_current_user)):
    """Schedule a new follow-up touch."""
    ws = user["workspace_id"]
    data = follow_up.model_dump()
    data["workspace_id"] = ws
    data["lead_id"] = str(data["lead_id"])
    data["scheduled_at"] = data["scheduled_at"].isoformat()

    result = supabase_admin.table("follow_up").insert(data).execute()
    return result.data[0]


@router.get("/calendar", response_model=list[CalendarResponse])
async def get_calendar(user: dict = Depends(get_current_user)):
    """Calendar view of follow-ups grouped by date."""
    ws = user["workspace_id"]
    result = supabase_admin.table("follow_up").select("*") \
        .eq("workspace_id", ws) \
        .in_("status", ["scheduled", "sent"]) \
        .order("scheduled_at") \
        .execute()

    # Group by date
    grouped: dict[str, list] = {}
    for item in result.data:
        date_key = item["scheduled_at"][:10]  # YYYY-MM-DD
        grouped.setdefault(date_key, []).append(item)

    return [CalendarResponse(date=date, items=items) for date, items in grouped.items()]


@router.patch("/{follow_up_id}/status", response_model=FollowUpResponse)
async def update_follow_up_status(
    follow_up_id: UUID,
    update: FollowUpStatusUpdate,
    user: dict = Depends(get_current_user),
):
    """Update follow-up status (sent, replied, paused, escalated)."""
    valid = {"scheduled", "sent", "replied", "paused", "escalated"}
    if update.status not in valid:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid}")

    ws = user["workspace_id"]
    result = supabase_admin.table("follow_up").update({"status": update.status}) \
        .eq("id", str(follow_up_id)).eq("workspace_id", ws).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return result.data[0]
