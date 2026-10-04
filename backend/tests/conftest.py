"""Pytest fixtures and configuration."""

import os
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

# Set test env variables before loading settings
os.environ["SUPABASE_URL"] = "https://fake-test-project.supabase.co"
os.environ["SUPABASE_KEY"] = "fake-anon-key"
os.environ["SUPABASE_SERVICE_KEY"] = "fake-service-key"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

from app.main import app
from app.api.deps import get_current_user


@pytest.fixture
def client():
    """FastAPI TestClient with overridden auth dependency for authenticated requests."""
    return TestClient(app)


@pytest.fixture
def mock_user():
    return {
        "user_id": "test-user-uuid",
        "email": "alex@startup.io",
        "name": "Alex Founder",
        "role": "founder",
        "workspace_id": "test-workspace-uuid",
    }


@pytest.fixture
def auth_client(mock_user):
    """Client with authenticated user dependency override."""
    app.dependency_overrides[get_current_user] = lambda: mock_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
