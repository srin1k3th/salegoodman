"""
Follow-Up Agent — cadence engine for scheduled multi-channel touches.

Tracks response patterns, auto-pauses on inbound activity, and escalates
after N unanswered touches.
"""

from datetime import datetime, timezone, timedelta
from app.database import supabase_admin


class FollowUpAgent:
    """Autonomous follow-up cadence engine."""

    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.config = self._load_config()

    def _load_config(self) -> dict:
        result = supabase_admin.table("agent_config").select("config") \
            .eq("workspace_id", self.workspace_id) \
            .eq("agent_type", "follow_up") \
            .single().execute()
        return result.data["config"] if result.data else {}

    async def schedule_cadence(self, lead_id: str, initial_call_date: datetime) -> list[dict]:
        """
        Schedule the full follow-up cadence for a lead based on configured touch_days.

        Returns a list of created follow-up records.
        """
        touch_days = self.config.get("touch_days", [1, 4, 8, 14])
        max_touches = self.config.get("max_touches", 4)
        formality = self.config.get("formality", 3)

        follow_ups = []
        for i, days in enumerate(touch_days[:max_touches]):
            scheduled = initial_call_date + timedelta(days=days)

            # Generate message based on touch number and formality
            subject, body = self._generate_touch_message(i + 1, formality)

            data = {
                "lead_id": lead_id,
                "touch_number": i + 1,
                "type": "email",
                "message_subject": subject,
                "message_body": body,
                "temperature": "warm" if i < 2 else "cold",
                "scheduled_at": scheduled.isoformat(),
                "status": "scheduled",
                "workspace_id": self.workspace_id,
            }

            result = supabase_admin.table("follow_up").insert(data).execute()
            follow_ups.append(result.data[0])

        # Log activity
        supabase_admin.table("activity_log").insert({
            "lead_id": lead_id,
            "agent_name": "Follow-Up Agent",
            "description": f"Scheduled {len(follow_ups)}-touch cadence (Days {', '.join(str(d) for d in touch_days[:max_touches])})",
            "workspace_id": self.workspace_id,
        }).execute()

        return follow_ups

    def _generate_touch_message(self, touch_number: int, formality: int) -> tuple[str, str]:
        """Generate message subject and body based on touch number and formality."""
        if formality <= 2:
            messages = {
                1: ("Quick recap from our call", "Hey — just sending over a quick summary of what we discussed. Excited to explore this further!"),
                2: ("Quick thought + customer story", "Hope your week is off to a great start! Sending over a 2-page recap of how one of our customers accelerated their sales cycle by 34%."),
                3: ("Checking in on the proposal", "Just wanted to circle back on the proposal we sent over. Any questions I can help with?"),
                4: ("Last check-in from us", "I know you're busy — just wanted to leave the door open. If timing isn't right, no worries at all."),
            }
        else:
            messages = {
                1: ("Follow-up: Implementation timeline discussion", "Dear colleague, following our discussion, I wanted to share the enclosed summary and proposed implementation timeline."),
                2: ("Relevant benchmark: Customer implementation case study", "I wanted to share a relevant case study documenting significant improvements in qualification cycle times."),
                3: ("Proposal review follow-up", "I hope this message finds you well. I wanted to follow up on the proposal we submitted for your review."),
                4: ("Final correspondence regarding our proposal", "This will be our final outreach regarding the current proposal. Please don't hesitate to reach out if circumstances change."),
            }

        subject, body = messages.get(touch_number, ("Follow-up", "Following up on our previous conversation."))
        return subject, body

    async def check_for_escalation(self, lead_id: str) -> dict:
        """
        Check if a lead has exceeded the unanswered touch threshold
        and should be escalated.
        """
        threshold = self.config.get("escalate_unanswered", 3)

        result = supabase_admin.table("follow_up").select("*") \
            .eq("lead_id", lead_id) \
            .eq("workspace_id", self.workspace_id) \
            .eq("status", "sent") \
            .order("touch_number") \
            .execute()

        unanswered_count = len(result.data)
        should_escalate = unanswered_count >= threshold

        return {
            "unanswered_count": unanswered_count,
            "threshold": threshold,
            "should_escalate": should_escalate,
        }

    async def pause_on_inbound(self, lead_id: str) -> int:
        """
        Auto-pause all scheduled follow-ups for a lead when inbound
        activity is detected (reply, meeting booked, etc).
        """
        if not self.config.get("auto_pause", True):
            return 0

        result = supabase_admin.table("follow_up").update({"status": "paused"}) \
            .eq("lead_id", lead_id) \
            .eq("workspace_id", self.workspace_id) \
            .eq("status", "scheduled") \
            .execute()

        paused_count = len(result.data)

        if paused_count:
            supabase_admin.table("activity_log").insert({
                "lead_id": lead_id,
                "agent_name": "Follow-Up Agent",
                "description": f"Auto-paused {paused_count} scheduled follow-ups (inbound activity detected)",
                "workspace_id": self.workspace_id,
            }).execute()

        return paused_count
