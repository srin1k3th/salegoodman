"""
Outreach Agent — manages call queue and voice call orchestration.

Applies tone/formality settings from config, integrates with the voice
pipeline, and detects buying signals from transcripts.
"""

from datetime import datetime, timezone
from app.database import supabase_admin


class OutreachAgent:
    """Autonomous outreach calling agent."""

    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self._config: dict | None = None  # lazy-loaded on first access

    @property
    def config(self) -> dict:
        """Lazy-load config from Supabase on first access."""
        if self._config is None:
            self._config = self._load_config()
        return self._config

    @config.setter
    def config(self, value: dict):
        """Allow tests and eval harness to inject config directly."""
        self._config = value

    def _load_config(self) -> dict:
        try:
            result = supabase_admin.table("agent_config").select("config") \
                .eq("workspace_id", self.workspace_id) \
                .eq("agent_type", "outreach") \
                .single().execute()
            return result.data["config"] if result.data else {}
        except Exception:
            return {}

    def generate_call_opening(self, prospect_name: str, company: str) -> str:
        """
        Generate a call opening based on formality and directness settings.
        These match the Live Call Opening Simulation in the frontend Settings.
        """
        formality = self.config.get("formality", 2)
        directness = self.config.get("directness", 4)
        voice = self.config.get("voice_profile", "Sarah").split(" ")[0]

        if formality <= 2 and directness >= 3:
            return (
                f"Hey {prospect_name}, {voice} from SaleGoodman here! "
                f"I was reading about {company}'s revenue push this quarter — "
                f"sounds like you guys are moving fast. Quick question: are your "
                f"account execs spending too much time hunting contacts instead of closing?"
            )
        elif formality >= 4 and directness <= 2:
            return (
                f"Good afternoon. I am calling from SaleGoodman on behalf of "
                f"Sarah Goodman. We track pipeline throughput for venture-backed "
                f"B2B firms. Specifically, we help eliminate inbound routing "
                f"bottlenecks. Would 15 minutes this Thursday make sense to discuss "
                f"your quarterly targets?"
            )
        else:
            return (
                f"Hi {prospect_name}, this is {voice} with SaleGoodman. I saw "
                f"{company} is expanding your sales team. We help revenue leaders "
                f"qualify high-fit prospects without bogging down account executives. "
                f"Do you have a quick moment to chat about how you're handling inbound demand?"
            )

    async def process_call_result(self, call_id: str, transcript: list[dict]) -> dict:
        """
        Analyze a completed call transcript for buying signals and next steps.

        Returns a notes_summary dict and determines if escalation is needed.
        """
        # Detect buying signals (simplified NLP — in production use LLM)
        buying_signals = []
        competitor_mentioned = False
        security_query = False
        negative_sentiment = False

        for entry in transcript:
            text = entry.get("text", "").lower()

            # Buying signals
            if any(phrase in text for phrase in ["implementation timeline", "pricing", "how soon", "get started", "next steps"]):
                buying_signals.append(entry["text"])

            # Competitor detection
            if any(comp in text for comp in ["outreach", "apollo", "salesloft", "hubspot"]):
                competitor_mentioned = True

            # Security/architecture queries
            if any(q in text for q in ["security", "soc 2", "api", "integration", "architecture"]):
                security_query = True

            # Negative sentiment
            if any(neg in text for neg in ["not interested", "don't call", "annoyed", "busy"]):
                negative_sentiment = True

        # Determine interest level
        if buying_signals:
            interest_level = "warm" if len(buying_signals) < 3 else "hot"
        elif negative_sentiment:
            interest_level = "cold"
        else:
            interest_level = "neutral"

        notes_summary = {
            "interest_level": interest_level,
            "buying_signals": buying_signals,
            "next_step": "Send proposal" if interest_level in ("warm", "hot") else "Schedule follow-up",
            "competitor_mentioned": competitor_mentioned,
            "security_query": security_query,
        }

        # Update call record
        supabase_admin.table("call").update({
            "notes_summary": notes_summary,
            "interest_level": interest_level,
            "next_step": notes_summary["next_step"],
        }).eq("id", call_id).execute()

        # Check escalation triggers
        escalation_reasons = []
        if competitor_mentioned and self.config.get("escalate_competitor", True):
            escalation_reasons.append("Direct competitor mentioned during call")
        if security_query and self.config.get("escalate_integration", True):
            escalation_reasons.append("Custom security/architecture query raised")
        if negative_sentiment and self.config.get("sentiment_guardrail", True):
            escalation_reasons.append("Negative sentiment detected (>50% friction)")

        return {
            "notes_summary": notes_summary,
            "escalation_needed": bool(escalation_reasons),
            "escalation_reasons": escalation_reasons,
        }

    async def check_daily_limit(self) -> dict:
        """Check calls made today vs. daily limit."""
        today = datetime.now(timezone.utc).date().isoformat()
        result = supabase_admin.table("call").select("id") \
            .eq("workspace_id", self.workspace_id) \
            .gte("scheduled_at", f"{today}T00:00:00") \
            .execute()

        limit = self.config.get("daily_limit", 25)
        made = len(result.data)

        return {
            "limit": limit,
            "calls_today": made,
            "remaining": max(0, limit - made),
            "at_limit": made >= limit,
        }
