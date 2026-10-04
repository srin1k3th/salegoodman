"""
SaleGoodman Backend — Configuration

Loads all settings from environment variables via pydantic-settings.
Copy .env.example to .env and fill in your keys.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Supabase ──────────────────────────────────────────────
    supabase_url: str = ""
    supabase_key: str = ""              # anon / public key
    supabase_service_key: str = ""      # service-role key (backend only)

    # ── Database (direct PG connection for Alembic) ───────────
    database_url: str = ""

    # ── AI / Voice Pipeline ───────────────────────────────────
    # One key powers everything: LLM (2.5-flash), STT (3.5-transcribe), TTS (3.8-flash-tts)
    gemini_api_key: str = ""

    # ── CORS ──────────────────────────────────────────────────
    cors_origins: str = "http://localhost:3000"

    # ── App ───────────────────────────────────────────────────
    secret_key: str = "change-this-to-a-random-secret"
    debug: bool = True

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
