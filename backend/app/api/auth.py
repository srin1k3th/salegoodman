"""
Auth routes — proxy to Supabase Auth.

Supabase handles all the heavy lifting (password hashing, JWT minting,
Google OAuth). We just proxy the calls and create our user/workspace records.
"""

from fastapi import APIRouter, HTTPException
from app.database import supabase, supabase_admin
from app.schemas.auth import LoginRequest, SignupRequest, AuthResponse
from app.models.agent_config import DEFAULT_CONFIGS

router = APIRouter()


@router.post("/signup", response_model=AuthResponse)
async def signup(req: SignupRequest):
    """Register a new user + workspace via Supabase Auth."""
    try:
        # 1. Create auth user in Supabase
        auth_response = supabase.auth.sign_up({
            "email": req.email,
            "password": req.password,
        })

        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Signup failed")

        user_id = str(auth_response.user.id)

        # 2. Create workspace
        ws_result = supabase_admin.table("workspace").insert({
            "name": req.workspace_name,
            "timezone": "America/Chicago",
            "notification_prefs": {
                "instant_escalations": True,
                "daily_briefing": True,
                "weekly_summary": True,
                "high_value_alerts": True,
            },
        }).execute()

        workspace_id = ws_result.data[0]["id"]

        # 3. Create user profile linked to workspace
        initials = "".join(word[0].upper() for word in req.name.split()[:2])
        supabase_admin.table("user").insert({
            "id": user_id,
            "email": req.email,
            "name": req.name,
            "role": "Owner / Admin",
            "initials": initials,
            "tone": "coral",
            "workspace_id": workspace_id,
        }).execute()

        # 4. Create default agent configs for the workspace
        for agent_type, config in DEFAULT_CONFIGS.items():
            supabase_admin.table("agent_config").insert({
                "agent_type": agent_type,
                "config": config,
                "workspace_id": workspace_id,
            }).execute()

        return AuthResponse(
            access_token=auth_response.session.access_token if auth_response.session else "",
            refresh_token=auth_response.session.refresh_token if auth_response.session else "",
            user_id=user_id,
            email=req.email,
            name=req.name,
            workspace_id=workspace_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signup error: {str(e)}")


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest):
    """Log in via Supabase Auth (email/password)."""
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password,
        })

        if not auth_response.user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user_id = str(auth_response.user.id)

        # Fetch user profile
        result = supabase_admin.table("user").select("*").eq("id", user_id).single().execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="User profile not found")

        return AuthResponse(
            access_token=auth_response.session.access_token,
            refresh_token=auth_response.session.refresh_token,
            user_id=user_id,
            email=req.email,
            name=result.data["name"],
            workspace_id=result.data["workspace_id"],
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")


@router.post("/google")
async def google_auth():
    """
    Google OAuth — the frontend handles the OAuth flow via Supabase JS client.
    This endpoint is a placeholder for any server-side Google auth processing.
    """
    return {
        "message": "Google OAuth is handled client-side via Supabase JS. "
                   "Use supabase.auth.signInWithOAuth({ provider: 'google' }) in the frontend."
    }
