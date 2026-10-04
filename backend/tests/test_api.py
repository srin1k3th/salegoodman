"""Tests for FastAPI endpoints."""

from unittest.mock import patch, MagicMock

VALID_UUID = "11111111-2222-3333-4444-555555555555"
WORKSPACE_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"


def test_get_dashboard_metrics(auth_client):
    with patch("app.api.dashboard.supabase_admin") as mock_db:
        query_mock = MagicMock()
        query_mock.select.return_value = query_mock
        query_mock.eq.return_value = query_mock
        query_mock.neq.return_value = query_mock
        query_mock.execute.return_value = MagicMock(data=[
            {"id": VALID_UUID, "stage": "Closing", "value": "$12,000"},
            {"id": VALID_UUID, "stage": "Won", "value": "$18,000"},
        ])
        mock_db.table.return_value = query_mock

        response = auth_client.get(
            "/dashboard/metrics",
            headers={"Authorization": "Bearer fake-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "pipeline_value" in data
        assert "total_leads" in data
        assert "funnel" in data
        assert "agent_health" in data


def test_get_contacts_list(auth_client):
    with patch("app.api.contacts.supabase_admin") as mock_db:
        query_mock = MagicMock()
        query_mock.select.return_value = query_mock
        query_mock.eq.return_value = query_mock
        query_mock.order.return_value = query_mock
        query_mock.range.return_value = query_mock
        query_mock.execute.return_value = MagicMock(data=[
            {
                "id": VALID_UUID,
                "name": "Sarah Chen",
                "role": "VP Sales",
                "company": "TechFlow",
                "email": "sarah@techflow.io",
                "phone": "+1 (555) 019-2834",
                "enriched": True,
                "relevance_score": 94,
                "source": "Apollo",
                "tags": ["SaaS", "Enterprise"],
                "initials": "SC",
                "tone": "Warm & Consultative",
                "workspace_id": WORKSPACE_UUID,
                "created_at": "2026-03-01T10:00:00Z"
            }
        ])
        mock_db.table.return_value = query_mock

        response = auth_client.get(
            "/contacts",
            headers={"Authorization": "Bearer fake-token"}
        )
        assert response.status_code == 200
        contacts = response.json()
        assert len(contacts) == 1
        assert contacts[0]["name"] == "Sarah Chen"


def test_get_agent_settings(auth_client):
    with patch("app.api.settings.supabase_admin") as mock_db:
        query_mock = MagicMock()
        query_mock.select.return_value = query_mock
        query_mock.eq.return_value = query_mock
        query_mock.single.return_value = query_mock
        query_mock.execute.return_value = MagicMock(data={
            "id": VALID_UUID,
            "agent_type": "closing",
            "workspace_id": WORKSPACE_UUID,
            "updated_at": "2026-03-01T10:00:00Z",
            "config": {"max_discount_pct": 15, "strict_redlines": True}
        })
        mock_db.table.return_value = query_mock

        response = auth_client.get(
            "/settings/agents/closing",
            headers={"Authorization": "Bearer fake-token"}
        )
        assert response.status_code == 200
        config = response.json()
        assert config["agent_type"] == "closing"
        assert config["config"]["max_discount_pct"] == 15
