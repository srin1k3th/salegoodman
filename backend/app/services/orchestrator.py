"""
Orchestrator — the central brain that coordinates all agents.

Routes leads between agents based on confidence threshold, classifies events
as routine vs. needs-human, and manages pipeline stage transitions.
"""

from datetime import datetime, timezone
from app.database import supabase_admin
from app.services.contact_finder import ContactFinderAgent
from app.services.outreach_agent import OutreachAgent
from app.services.follow_up_agent import FollowUpAgent
from app.services.closing_agent import ClosingAgent


class Orchestrator:
    """Central orchestrator brain — coordinates all agent handoffs."""

    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.config = self._load_config()

        # Initialize sub-agents
        self.contact_finder = ContactFinderAgent(workspace_id)
        self.outreach_agent = OutreachAgent(workspace_id)
        self.follow_up_agent = FollowUpAgent(workspace_id)
        self.closing_agent = ClosingAgent(workspace_id)

    def _load_config(self) -> dict:
        result = supabase_admin.table("agent_config").select("config") \
            .eq("workspace_id", self.workspace_id) \
            .eq("agent_type", "orchestrator") \
            .single().execute()
        return result.data["config"] if result.data else {}

    async def process_event(self, event_type: str, event_data: dict) -> dict:
        """
        Process an incoming event and route to the appropriate agent.

        Event types:
            - "contact_found": New contact discovered → evaluate and queue
            - "call_completed": Outreach call finished → analyze and route
            - "follow_up_reply": Prospect replied → pause cadence, route to closing
            - "negotiation_request": Prospect made a request → evaluate guardrails
            - "manual_override": Founder takes over a lead
        """
        confidence = self.config.get("confidence_threshold", 90)
        coordination_mode = self.config.get("coordination_mode", "Adaptive Parallel Hand-off")
        safety_switch = self.config.get("safety_switch", False)

        if safety_switch:
            return {
                "action": "paused",
                "reason": "Emergency safety killswitch is active. All outbound operations paused.",
            }

        handler = {
            "contact_found": self._handle_contact_found,
            "call_completed": self._handle_call_completed,
            "follow_up_reply": self._handle_follow_up_reply,
            "negotiation_request": self._handle_negotiation_request,
        }.get(event_type)

        if not handler:
            return {"action": "unknown", "reason": f"Unknown event type: {event_type}"}

        result = await handler(event_data, confidence)

        # Log the orchestrator's decision
        supabase_admin.table("activity_log").insert({
            "lead_id": event_data.get("lead_id"),
            "agent_name": "Orchestrator",
            "description": f"[{event_type}] {result.get('action', 'processed')}: {result.get('reason', '')}",
            "workspace_id": self.workspace_id,
        }).execute()

        return result

    async def _handle_contact_found(self, data: dict, confidence: int) -> dict:
        """Route: Contact Found → evaluate → queue for outreach or escalate."""
        evaluation = await self.contact_finder.evaluate_contact(data)

        if evaluation["action"] == "auto_queue":
            return {
                "action": "queued_for_outreach",
                "reason": evaluation["reason"],
                "next_agent": "outreach",
            }
        elif evaluation["action"] == "escalate":
            return {
                "action": "escalated",
                "reason": evaluation["reason"],
                "next_agent": "human",
            }
        else:
            return {
                "action": "watchlisted",
                "reason": evaluation["reason"],
                "next_agent": None,
            }

    async def _handle_call_completed(self, data: dict, confidence: int) -> dict:
        """Route: Call completed → analyze → schedule follow-up or move to closing."""
        call_id = data.get("call_id")
        lead_id = data.get("lead_id")
        transcript = data.get("transcript", [])

        # Analyze the call
        analysis = await self.outreach_agent.process_call_result(call_id, transcript)

        # Handle escalations from the call
        if analysis["escalation_needed"]:
            return {
                "action": "escalated",
                "reason": "; ".join(analysis["escalation_reasons"]),
                "next_agent": "human",
            }

        interest = analysis["notes_summary"].get("interest_level", "neutral")

        if interest in ("warm", "hot"):
            # Schedule follow-up cadence
            now = datetime.now(timezone.utc)
            await self.follow_up_agent.schedule_cadence(lead_id, now)

            # Update lead stage
            supabase_admin.table("lead").update({
                "stage": "Following Up" if interest == "warm" else "Closing",
                "last_touched": now.isoformat(),
            }).eq("id", lead_id).execute()

            return {
                "action": "follow_up_scheduled",
                "reason": f"Interest level: {interest}. Follow-up cadence initiated.",
                "next_agent": "follow_up",
            }
        else:
            return {
                "action": "archived",
                "reason": "Low interest. Lead archived for future outreach.",
                "next_agent": None,
            }

    async def _handle_follow_up_reply(self, data: dict, confidence: int) -> dict:
        """Route: Prospect replied → pause cadence → move to closing."""
        lead_id = data.get("lead_id")

        # Pause remaining follow-ups
        paused = await self.follow_up_agent.pause_on_inbound(lead_id)

        # Move to closing stage
        supabase_admin.table("lead").update({
            "stage": "Closing",
            "last_touched": datetime.now(timezone.utc).isoformat(),
        }).eq("id", lead_id).execute()

        return {
            "action": "moved_to_closing",
            "reason": f"Prospect replied. Paused {paused} follow-ups. Moving to closing.",
            "next_agent": "closing",
        }

    async def _handle_negotiation_request(self, data: dict, confidence: int) -> dict:
        """Route: Negotiation request → evaluate guardrails → approve or escalate."""
        deal_id = data.get("deal_id")
        request = data.get("request", {})

        result = await self.closing_agent.evaluate_request(deal_id, request)

        if result["escalation_needed"]:
            await self.closing_agent.create_escalation_for_deal(
                deal_id, result["escalation_reasons"]
            )
            return {
                "action": "escalated",
                "reason": "; ".join(result["escalation_reasons"]),
                "counter_offer": result["counter_offer"],
                "next_agent": "human",
            }
        else:
            return {
                "action": "approved",
                "reason": "Within guardrails. Counter-offer generated.",
                "counter_offer": result["counter_offer"],
                "next_agent": "closing",
            }

    async def get_system_status(self) -> dict:
        """Get overall orchestrator system status."""
        safety = self.config.get("safety_switch", False)

        return {
            "status": "paused" if safety else "operational",
            "confidence_threshold": self.config.get("confidence_threshold", 90),
            "coordination_mode": self.config.get("coordination_mode", "Adaptive Parallel Hand-off"),
            "safety_switch": safety,
            "agents": {
                "contact_finder": await self.contact_finder.check_daily_quota(),
                "outreach": await self.outreach_agent.check_daily_limit(),
            },
        }
