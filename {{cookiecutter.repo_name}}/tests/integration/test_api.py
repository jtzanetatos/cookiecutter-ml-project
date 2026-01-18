import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add deployment/api to path so we can import 'app'
# This simulates how the Docker container works or how a dev would run it
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "deployment" / "api"))

from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Verify the health endpoint returns 200/ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_endpoint():
    """Verify the root metadata endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "docs" in data
