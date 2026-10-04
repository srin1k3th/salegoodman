"""Tests for system endpoints and API specs."""

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "salegoodman-api"


def test_openapi_schema(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "SaleGoodman API"
    # Verify all expected route paths exist in the spec
    paths = schema["paths"]
    assert "/health" in paths
    assert "/auth/login" in paths
    assert "/dashboard/metrics" in paths
    assert "/contacts" in paths
    assert "/leads" in paths
    assert "/calls" in paths
    assert "/follow-ups" in paths
    assert "/deals" in paths
    assert "/escalations" in paths
    assert "/settings/workspace" in paths
