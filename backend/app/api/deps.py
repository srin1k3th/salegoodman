"""
Auth dependency — verifies Supabase JWT and resolves workspace.

Usage in route handlers:
    @router.get("/example")
    async def example(user: dict = Depends(get_current_user)):
        workspace_id = user["workspace_id"]
"""

from fastapi import Depends, HTTPException, Header
from app.database import supabase_admin


async def get_current_user(authorization: str = Header(...)) -> dict:
    """
    Extract and verify the Supabase JWT from the Authorization header.
    Returns a dict with user_id, email, workspace_id.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        # Verify JWT with Supabase
        user_response = supabase_admin.auth.get_user(token)
        supabase_user = user_response.user

        if not supabase_user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Fetch workspace association from our user table
        result = supabase_admin.table("user").select("*").eq("id", supabase_user.id).single().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="User profile not found")

        return {
            "user_id": str(supabase_user.id),
            "email": supabase_user.email,
            "name": result.data.get("name", ""),
            "role": result.data.get("role", ""),
            "workspace_id": result.data.get("workspace_id"),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")
