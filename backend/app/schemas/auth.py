"""Auth schemas."""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    email: str
    password: str
    name: str
    workspace_name: str = "My Workspace"


class GoogleAuthRequest(BaseModel):
    id_token: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    email: str
    name: str
    workspace_id: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str
