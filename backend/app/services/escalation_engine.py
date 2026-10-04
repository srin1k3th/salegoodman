"""
Escalation Engine — classifies and scores escalation urgency.

Evaluates negotiation signals, lead value, and response history to
determine escalation priority.
"""

from app.database import supabase_admin


class EscalationEngine:
    """Scores and classifies escalation urgency."""

    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id

    async def create_escalation(
        self,
        lead_id: str | None,
        title: str,
        source_agent: str,
        contact_info: str,
        summary: str,
    ) -> dict:
        """Create a new escalation and score its urgency."""
        urgency = await self._score_urgency(lead_id, source_agent, title)

        result = supabase_admin.table("escalation").insert({
            "lead_id": lead_id,
            "title": title,
            "source_agent": source_agent,
            "contact_info": contact_info,
            "summary": f"[Priority: {urgency['level']}] {summary}",
            "workspace_id": self.workspace_id,
        }).execute()

        # Log activity
        supabase_admin.table("activity_log").insert({
            "lead_id": lead_id,
            "agent_name": "Escalation Engine",
            "description": f"New escalation ({urgency['level']}): {title}",
            "workspace_id": self.workspace_id,
        }).execute()

        return {**result.data[0], "urgency": urgency}

    async def _score_urgency(self, lead_id: str | None, source_agent: str, title: str) -> dict:
        """
        Score escalation urgency based on multiple signals.

        Factors:
        - Deal value (higher = more urgent)
        - Source agent (closing > outreach > follow_up > contact_finder)
        - Keywords in title (pricing, legal, competitor = higher)
        """
        score = 50  # Base score

        # Agent priority weighting
        agent_weights = {
            "closing_agent": 30,
            "outreach_agent": 20,
            "follow_up_agent": 15,
            "contact_finder": 10,
        }
        score += agent_weights.get(source_agent, 10)

        # Keyword signals
        title_lower = title.lower()
        if any(kw in title_lower for kw in ["pricing", "discount", "negotiation"]):
            score += 15
        if any(kw in title_lower for kw in ["legal", "contract", "clause", "redline"]):
            score += 20
        if any(kw in title_lower for kw in ["competitor", "incumbent"]):
            score += 10
        if any(kw in title_lower for kw in ["enterprise", "vip", "high-value"]):
            score += 15

        # Check deal value if we have a lead
        if lead_id:
            deal = supabase_admin.table("deal").select("value") \
                .eq("lead_id", lead_id).eq("workspace_id", self.workspace_id) \
                .limit(1).execute()
            if deal.data:
                try:
                    value = int(deal.data[0]["value"].replace("$", "").replace(",", ""))
                    if value >= 50000:
                        score += 25
                    elif value >= 25000:
                        score += 15
                except (ValueError, AttributeError, KeyError):
                    pass

        # Determine level
        if score >= 90:
            level = "critical"
        elif score >= 70:
            level = "high"
        elif score >= 50:
            level = "medium"
        else:
            level = "low"

        return {"score": min(score, 100), "level": level}
