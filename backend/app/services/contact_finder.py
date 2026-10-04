"""
Contact Finder Agent — discovers and enriches lead profiles.

Scans LinkedIn/Apollo (simulated), evaluates fit scores against configured
thresholds, and auto-queues or escalates based on AgentConfig.
"""

from uuid import uuid4
from datetime import datetime, timezone
from app.database import supabase_admin


class ContactFinderAgent:
    """Autonomous contact discovery and enrichment."""

    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load agent config from DB."""
        result = supabase_admin.table("agent_config").select("config") \
            .eq("workspace_id", self.workspace_id) \
            .eq("agent_type", "contact_finder") \
            .single().execute()
        return result.data["config"] if result.data else {}

    async def evaluate_contact(self, contact_data: dict) -> dict:
        """
        Evaluate a discovered contact against configured thresholds.

        Returns:
            {action: "auto_queue" | "escalate" | "watchlist", contact_id, reason}
        """
        fit_score = contact_data.get("relevance_score", 0)
        min_score = self.config.get("min_fit_score", 85)
        escalate_enterprise = self.config.get("escalate_enterprise", True)

        # Check if enterprise account (simulated check)
        is_enterprise = contact_data.get("company_size", 0) > 500

        if is_enterprise and escalate_enterprise:
            action = "escalate"
            reason = "Enterprise account flagged for strategy review before first contact."
        elif fit_score >= min_score:
            action = "auto_queue"
            reason = f"Fit score {fit_score} exceeds threshold {min_score}. Auto-enriching and queuing."
        else:
            action = "watchlist"
            reason = f"Fit score {fit_score} below threshold {min_score}. Added to watchlist."

        return {"action": action, "reason": reason}

    async def discover_and_store(self, contact_data: dict) -> dict:
        """
        Process a discovered contact: store, evaluate, and take action.
        """
        # Store contact
        contact_data["workspace_id"] = self.workspace_id
        contact_data["source"] = "agent"
        result = supabase_admin.table("contact").insert(contact_data).execute()
        contact = result.data[0]

        # Evaluate
        evaluation = await self.evaluate_contact(contact_data)

        # Auto-enrich if configured
        if self.config.get("auto_enrich", True) and evaluation["action"] == "auto_queue":
            contact = await self._enrich_contact(contact["id"])

        # Log activity
        supabase_admin.table("activity_log").insert({
            "lead_id": None,
            "agent_name": "Contact Finder",
            "description": f"Found {contact_data.get('name', 'contact')} at {contact_data.get('company', '')}. {evaluation['reason']}",
            "initials": contact_data.get("initials"),
            "tone": contact_data.get("tone"),
            "workspace_id": self.workspace_id,
        }).execute()

        # If auto-queue, create a lead
        if evaluation["action"] == "auto_queue":
            supabase_admin.table("lead").insert({
                "contact_id": contact["id"],
                "stage": "Found",
                "company": contact_data.get("company"),
                "initials": contact_data.get("initials"),
                "tone": contact_data.get("tone"),
                "workspace_id": self.workspace_id,
            }).execute()

        # If escalate, create an escalation
        elif evaluation["action"] == "escalate":
            supabase_admin.table("escalation").insert({
                "title": f"Enterprise account: {contact_data.get('company', '')}",
                "source_agent": "contact_finder",
                "contact_info": f"{contact_data.get('name', '')} · {contact_data.get('company', '')}",
                "summary": evaluation["reason"],
                "workspace_id": self.workspace_id,
            }).execute()

        return {**contact, "evaluation": evaluation}

    async def _enrich_contact(self, contact_id: str) -> dict:
        """
        Simulate contact enrichment (LinkedIn/Apollo lookup).
        In production, this would call real APIs.
        """
        # Simulated enrichment — mark as enriched
        result = supabase_admin.table("contact").update({
            "enriched": True,
        }).eq("id", contact_id).execute()

        return result.data[0] if result.data else {}

    async def check_daily_quota(self) -> dict:
        """Check how many contacts have been discovered today vs. quota."""
        today = datetime.now(timezone.utc).date().isoformat()
        result = supabase_admin.table("contact").select("id") \
            .eq("workspace_id", self.workspace_id) \
            .gte("created_at", f"{today}T00:00:00") \
            .execute()

        quota = self.config.get("daily_quota", 50)
        discovered = len(result.data)

        return {
            "quota": quota,
            "discovered_today": discovered,
            "remaining": max(0, quota - discovered),
            "at_limit": discovered >= quota,
        }
