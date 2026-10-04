"""Contacts CRUD routes."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.deps import get_current_user
from app.database import supabase_admin
from app.schemas.contact import ContactCreate, ContactUpdate, ContactResponse

router = APIRouter()


@router.get("", response_model=list[ContactResponse])
@router.get("/", include_in_schema=False, response_model=list[ContactResponse])
async def list_contacts(
    user: dict = Depends(get_current_user),
    query: str = "",
    min_score: int | None = None,
    status: str | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
):
    """List contacts with optional search and filters."""
    ws = user["workspace_id"]
    q = supabase_admin.table("contact").select("*").eq("workspace_id", ws)

    if query:
        q = q.or_(f"name.ilike.%{query}%,company.ilike.%{query}%,role.ilike.%{query}%")
    if min_score is not None:
        q = q.gte("relevance_score", min_score)
    if status:
        q = q.eq("status", status)

    result = q.order("relevance_score", desc=True).range(offset, offset + limit - 1).execute()
    return result.data


@router.post("", response_model=ContactResponse, status_code=201)
@router.post("/", include_in_schema=False, response_model=ContactResponse, status_code=201)
async def create_contact(contact: ContactCreate, user: dict = Depends(get_current_user)):
    """Create a new contact."""
    ws = user["workspace_id"]
    data = contact.model_dump()
    data["workspace_id"] = ws

    result = supabase_admin.table("contact").insert(data).execute()
    return result.data[0]


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: UUID, user: dict = Depends(get_current_user)):
    """Get a single contact by ID."""
    ws = user["workspace_id"]
    result = supabase_admin.table("contact").select("*") \
        .eq("id", str(contact_id)).eq("workspace_id", ws).single().execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Contact not found")
    return result.data


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: UUID, update: ContactUpdate, user: dict = Depends(get_current_user)):
    """Update a contact."""
    ws = user["workspace_id"]
    data = update.model_dump(exclude_unset=True)

    result = supabase_admin.table("contact").update(data) \
        .eq("id", str(contact_id)).eq("workspace_id", ws).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Contact not found")
    return result.data[0]


@router.delete("/{contact_id}", status_code=204)
async def delete_contact(contact_id: UUID, user: dict = Depends(get_current_user)):
    """Delete a contact."""
    ws = user["workspace_id"]
    supabase_admin.table("contact").delete() \
        .eq("id", str(contact_id)).eq("workspace_id", ws).execute()
