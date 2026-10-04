# SaleGoodman Backend

FastAPI backend for the SaleGoodman autonomous AI sales platform.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and fill in environment variables
cp .env.example .env

# 3. Set up Supabase
#    - Create a project at supabase.com
#    - Run supabase/migrations/001_initial.sql in the SQL Editor
#    - Run supabase/seed.sql for demo data
#    - Copy the project URL and keys to .env

# 4. Run the dev server
uvicorn app.main:app --reload --port 8000
```

## API Docs

Once running, visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

## Architecture

- **FastAPI** — REST API framework
- **Supabase** — PostgreSQL + Auth + Realtime + Storage
- **5 Agent Services** — Contact Finder, Outreach, Follow-Up, Closing, Orchestrator
- **Voice Pipeline** — Groq STT → Gemini LLM → Gemini TTS

## Deployment

Deploy to Railway:

```bash
railway up
```

Requires Railway CLI and a linked project. See `railway.toml` for config.
