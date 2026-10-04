"""
SaleGoodman Backend — Supabase Client

Provides both a public client (anon key) and an admin client (service-role key).
The admin client bypasses Row Level Security and is used by agent services.
"""

from supabase import create_client, Client
from app.config import settings


def get_supabase_client() -> Client:
    """Public Supabase client using the anon key. Respects RLS."""
    return create_client(settings.supabase_url, settings.supabase_key)


def get_supabase_admin() -> Client:
    """Admin Supabase client using the service-role key. Bypasses RLS."""
    return create_client(settings.supabase_url, settings.supabase_service_key)


# Singleton instances
supabase: Client = get_supabase_client() if settings.supabase_url else None  # type: ignore
supabase_admin: Client = get_supabase_admin() if settings.supabase_service_key else None  # type: ignore
