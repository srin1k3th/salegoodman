"""Unit tests for agent services and rule engines."""

import pytest
from unittest.mock import patch, MagicMock
from app.services.contact_finder import ContactFinderAgent
from app.services.outreach_agent import OutreachAgent
from app.services.follow_up_agent import FollowUpAgent
from app.services.closing_agent import ClosingAgent
from app.services.escalation_engine import EscalationEngine
from app.services.orchestrator import Orchestrator


@pytest.fixture(autouse=True)
def mock_supabase_db():
    """Mock supabase_admin calls in services."""
    with patch("app.services.contact_finder.supabase_admin") as mock_cf_db, \
         patch("app.services.outreach_agent.supabase_admin") as mock_oa_db, \
         patch("app.services.follow_up_agent.supabase_admin") as mock_fu_db, \
         patch("app.services.closing_agent.supabase_admin") as mock_cl_db, \
         patch("app.services.escalation_engine.supabase_admin") as mock_ee_db, \
         patch("app.services.orchestrator.supabase_admin") as mock_orc_db:

        # Default query mock returning empty config so defaults are used
        for mock_db in [mock_cf_db, mock_oa_db, mock_fu_db, mock_cl_db, mock_ee_db, mock_orc_db]:
            mock_query = MagicMock()
            mock_query.select.return_value = mock_query
            mock_query.eq.return_value = mock_query
            mock_query.single.return_value = mock_query
            mock_query.execute.return_value = MagicMock(data=None)
            mock_db.table.return_value = mock_query

        yield


@pytest.mark.asyncio
async def test_contact_finder_evaluation():
    agent = ContactFinderAgent("test-workspace")
    agent.config = {"min_fit_score": 85, "escalate_enterprise": True}

    # 1. High fit score (>= 85) -> auto_queue
    res_queue = await agent.evaluate_contact({
        "name": "Sarah Chen",
        "company": "TechFlow",
        "company_size": 120,
        "relevance_score": 92
    })
    assert res_queue["action"] == "auto_queue"
    assert "auto-enriching" in res_queue["reason"].lower()

    # 2. Low fit score (< 85) -> watchlist
    res_watch = await agent.evaluate_contact({
        "name": "Bob Small",
        "company": "Corner Shop",
        "company_size": 5,
        "relevance_score": 60
    })
    assert res_watch["action"] == "watchlist"
    assert "below threshold" in res_watch["reason"].lower()

    # 3. Enterprise company (> 500) -> escalate
    res_ent = await agent.evaluate_contact({
        "name": "Alice Enterprise",
        "company": "Global MegaCorp",
        "company_size": 1500,
        "relevance_score": 95
    })
    assert res_ent["action"] == "escalate"
    assert "enterprise account" in res_ent["reason"].lower()


def test_outreach_agent_call_opening():
    agent = OutreachAgent("test-workspace")
    
    # Casual / direct
    agent.config = {"formality": 1, "directness": 5, "voice_profile": "Sarah (Warm & Confident)"}
    opening_casual = agent.generate_call_opening("John Doe", "Acme Corp")
    assert "Hey John Doe" in opening_casual
    assert "Acme Corp" in opening_casual

    # Formal / consultative
    agent.config = {"formality": 5, "directness": 1, "voice_profile": "David (Authoritative)"}
    opening_formal = agent.generate_call_opening("Dr. Smith", "Biotech Inc")
    assert "Good afternoon" in opening_formal
    assert "discuss your quarterly targets" in opening_formal


@pytest.mark.asyncio
async def test_outreach_agent_transcript_analysis():
    agent = OutreachAgent("test-workspace")
    agent.config = {
        "escalate_competitor": True,
        "escalate_integration": True,
        "sentiment_guardrail": True,
    }

    # Buying signals + competitor mention
    transcript = [
        {"speaker": "agent", "text": "How can we help your team?"},
        {"speaker": "prospect", "text": "We are currently using Outreach, but your pricing looks interesting."},
    ]

    with patch("app.services.outreach_agent.supabase_admin") as mock_db:
        mock_db.table.return_value.update.return_value.eq.return_value.execute.return_value = MagicMock()
        result = await agent.process_call_result("call-123", transcript)

    assert result["notes_summary"]["interest_level"] == "warm"
    assert result["notes_summary"]["competitor_mentioned"] is True
    assert result["escalation_needed"] is True
    assert any("competitor" in r.lower() for r in result["escalation_reasons"])


@pytest.mark.asyncio
async def test_closing_agent_guardrails():
    agent = ClosingAgent("test-workspace")
    agent.config = {
        "max_discount_pct": 15,
        "max_term_extension_days": 30,
        "payment_terms": "Allow Net 45 without approval",
        "strict_redlines": True,
        "formality": 4,
    }

    with patch("app.services.closing_agent.supabase_admin") as mock_db:
        mock_db.table.return_value.update.return_value.eq.return_value.execute.return_value = MagicMock()

        # 1. Request within guardrails: 10% discount, Net 30
        res_ok = await agent.evaluate_request("deal-1", {
            "requested_discount_pct": 10,
            "requested_term_extension_days": 15,
            "requested_payment_terms": "Net 30",
        })
        assert res_ok["can_approve"] is True
        assert res_ok["escalation_needed"] is False
        assert res_ok["offered_discount"] == 10

        # 2. Request exceeds discount: 30% requested vs 15% limit
        res_disc = await agent.evaluate_request("deal-2", {
            "requested_discount_pct": 30,
            "requested_term_extension_days": 10,
            "requested_payment_terms": "Net 30",
        })
        assert res_disc["can_approve"] is False
        assert res_disc["escalation_needed"] is True
        assert any("30% discount exceeds 15% limit" in r for r in res_disc["escalation_reasons"])
        # Counter-offer must be capped at 15%
        assert res_disc["offered_discount"] == 15

        # 3. Custom legal redline clause
        res_legal = await agent.evaluate_request("deal-3", {
            "requested_discount_pct": 5,
            "custom_legal_clause": "Vendor assumes uncapped consequential liability.",
        })
        assert res_legal["can_approve"] is False
        assert res_legal["escalation_needed"] is True
        assert any("legal clause" in r.lower() for r in res_legal["escalation_reasons"])


def test_follow_up_touch_messages():
    agent = FollowUpAgent("test-workspace")
    
    # Check messages generated for touches 1 through 4
    for touch in [1, 2, 3, 4]:
        sub, body = agent._generate_touch_message(touch, formality=2)
        assert len(sub) > 0
        assert len(body) > 0


@pytest.mark.asyncio
async def test_escalation_engine_urgency():
    engine = EscalationEngine("test-workspace")

    # High priority: closing agent + legal terms
    urgency_high = await engine._score_urgency(
        lead_id=None,
        source_agent="closing_agent",
        title="Custom legal redline requested on annual contract"
    )
    # base 50 + closing_agent 30 + legal 20 = 100 -> critical
    assert urgency_high["score"] >= 90
    assert urgency_high["level"] == "critical"

    # Lower priority: routine inquiry
    urgency_low = await engine._score_urgency(
        lead_id=None,
        source_agent="contact_finder",
        title="Discovered new startup lead"
    )
    assert urgency_low["score"] < 70
    assert urgency_low["level"] in ["medium", "low"]


@pytest.mark.asyncio
async def test_orchestrator_safety_switch():
    orchestrator = Orchestrator("test-workspace")
    orchestrator.config = {"safety_switch": True}

    result = await orchestrator.process_event("contact_found", {"relevance_score": 90})
    assert result["action"] == "paused"
    assert "killswitch is active" in result["reason"]
