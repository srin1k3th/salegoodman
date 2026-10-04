"""Call queue + transcript routes."""

from uuid import UUID
from datetime import datetime, timezone, date
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import get_current_user
from app.database import supabase_admin
from app.schemas.call import CallCreate, CallResponse, CallQueueResponse

router = APIRouter()


@router.get("", response_model=list[CallResponse])
@router.get("/", include_in_schema=False, response_model=list[CallResponse])
async def list_calls(
    user: dict = Depends(get_current_user),
    status: str | None = None,
    limit: int = Query(default=50, le=200),
):
    """List calls with optional status filter."""
    ws = user["workspace_id"]
    q = supabase_admin.table("call").select("*").eq("workspace_id", ws)

    if status:
        q = q.eq("status", status)

    result = q.order("scheduled_at", desc=True).limit(limit).execute()
    return result.data


@router.post("/", response_model=CallResponse, status_code=201)
async def create_call(call: CallCreate, user: dict = Depends(get_current_user)):
    """Schedule a new outreach call."""
    ws = user["workspace_id"]
    data = call.model_dump()
    data["workspace_id"] = ws
    data["lead_id"] = str(data["lead_id"])
    data["scheduled_at"] = data["scheduled_at"].isoformat()

    result = supabase_admin.table("call").insert(data).execute()

    # Log activity
    supabase_admin.table("activity_log").insert({
        "lead_id": str(call.lead_id),
        "agent_name": "Outreach Agent",
        "description": f"Call scheduled for {call.scheduled_at.strftime('%I:%M %p')}",
        "workspace_id": ws,
    }).execute()

    return result.data[0]


@router.get("/queue", response_model=CallQueueResponse)
async def get_call_queue(user: dict = Depends(get_current_user)):
    """Today's call queue."""
    ws = user["workspace_id"]
    today = date.today().isoformat()

    result = supabase_admin.table("call").select("*") \
        .eq("workspace_id", ws) \
        .gte("scheduled_at", f"{today}T00:00:00") \
        .lte("scheduled_at", f"{today}T23:59:59") \
        .order("scheduled_at") \
        .execute()

    calls = result.data
    completed = sum(1 for c in calls if c["status"] == "completed")
    pending = sum(1 for c in calls if c["status"] == "pending")

    return CallQueueResponse(
        date=today,
        calls=calls,
        total=len(calls),
        completed=completed,
        pending=pending,
    )


@router.get("/{call_id}", response_model=CallResponse)
async def get_call(call_id: UUID, user: dict = Depends(get_current_user)):
    """Get a single call with transcript."""
    ws = user["workspace_id"]
    result = supabase_admin.table("call").select("*") \
        .eq("id", str(call_id)).eq("workspace_id", ws).single().execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Call not found")
    return result.data
