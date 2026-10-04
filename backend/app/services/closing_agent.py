"""
Closing Agent — negotiates deals within founder-defined guardrails.

Enforces max discount, term extensions, and payment terms as hard constraints.
Generates counter-offers within limits and escalates when exceeded.
"""

from app.database import supabase_admin


class ClosingAgent:
    """Autonomous closing negotiation agent."""

    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.config = self._load_config()

    def _load_config(self) -> dict:
        result = supabase_admin.table("agent_config").select("config") \
            .eq("workspace_id", self.workspace_id) \
            .eq("agent_type", "closing") \
            .single().execute()
        return result.data["config"] if result.data else {}

    async def evaluate_request(self, deal_id: str, request: dict) -> dict:
        """
        Evaluate a prospect's negotiation request against guardrails.

        Args:
            deal_id: The deal being negotiated
            request: {
                "requested_discount_pct": 20,
                "requested_term_extension_days": 45,
                "requested_payment_terms": "Net 60",
                "custom_legal_clause": "..."
            }

        Returns:
            {
                "can_approve": bool,
                "counter_offer": str,
                "escalation_needed": bool,
                "escalation_reasons": list
            }
        """
        max_discount = self.config.get("max_discount_pct", 15)
        max_term = self.config.get("max_term_extension_days", 30)
        allowed_payment = self.config.get("payment_terms", "Allow Net 45 without approval")
        strict_redlines = self.config.get("strict_redlines", True)

        requested_discount = request.get("requested_discount_pct", 0)
        requested_term = request.get("requested_term_extension_days", 0)
        requested_payment = request.get("requested_payment_terms", "Net 30")
        has_legal_clause = bool(request.get("custom_legal_clause"))

        escalation_reasons = []
        can_approve = True

        # Check discount
        if requested_discount > max_discount:
            can_approve = False
            escalation_reasons.append(
                f"Requested {requested_discount}% discount exceeds {max_discount}% limit"
            )

        # Check term extension
        if requested_term > max_term:
            can_approve = False
            escalation_reasons.append(
                f"Requested {requested_term}-day extension exceeds {max_term}-day limit"
            )

        # Check payment terms
        if requested_payment == "Net 60" and "Net 60" not in allowed_payment:
            can_approve = False
            escalation_reasons.append("Net 60 payment terms not authorized")

        # Check legal redlines
        if has_legal_clause and strict_redlines:
            can_approve = False
            escalation_reasons.append("Custom legal clause requires human review")

        # Generate counter-offer
        counter_discount = min(requested_discount, max_discount)
        counter_offer = self._generate_counter_offer(
            counter_discount, max_term, requested_payment, request
        )

        # Update deal with offered terms
        supabase_admin.table("deal").update({
            "discount_offered": counter_discount,
            "term_extension_days": min(requested_term, max_term),
            "payment_terms": requested_payment if can_approve else "Net 30",
        }).eq("id", deal_id).execute()

        return {
            "can_approve": can_approve,
            "counter_offer": counter_offer,
            "escalation_needed": not can_approve,
            "escalation_reasons": escalation_reasons,
            "offered_discount": counter_discount,
            "offered_term": min(requested_term, max_term),
        }

    def _generate_counter_offer(self, discount: float, max_term: int, payment: str, request: dict) -> str:
        """Generate a diplomatic counter-offer within guardrails."""
        formality = self.config.get("formality", 4)
        prospect_name = request.get("prospect_name", "the prospect")

        offered_savings = f"{discount}%"

        if formality >= 4:
            return (
                f"I can honor an annual commitment incentive of {offered_savings} "
                f"along with {payment} invoicing. For the additional requested discount, "
                f"I've flagged this directly to Sarah Goodman for executive review."
            )
        else:
            return (
                f"Here's what I can do right now: {offered_savings} off with "
                f"{payment}. For anything beyond that, I'll loop in Sarah to "
                f"see what we can work out."
            )

    async def create_escalation_for_deal(self, deal_id: str, reasons: list[str]) -> dict:
        """Create an escalation when negotiation exceeds guardrails."""
        deal = supabase_admin.table("deal").select("*") \
            .eq("id", deal_id).single().execute()

        if not deal.data:
            return {"error": "Deal not found"}

        d = deal.data
        escalation = supabase_admin.table("escalation").insert({
            "lead_id": d.get("lead_id"),
            "title": f"Negotiation guardrail exceeded: {d.get('company', '')}",
            "source_agent": "closing_agent",
            "contact_info": f"{d.get('contact_name', '')} · {d.get('company', '')}",
            "summary": ". ".join(reasons),
            "workspace_id": self.workspace_id,
        }).execute()

        # Log activity
        supabase_admin.table("activity_log").insert({
            "lead_id": d.get("lead_id"),
            "agent_name": "Closing Agent",
            "description": f"Escalated: {reasons[0] if reasons else 'Guardrail exceeded'}",
            "workspace_id": self.workspace_id,
        }).execute()

        return escalation.data[0]
