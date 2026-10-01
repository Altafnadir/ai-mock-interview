import sys
import os
import pytest
from fastapi.testclient import TestClient

# Anchor backend path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "project_id" in data
    assert data["project_id"] == "GIMS-BSSE-F202206"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "metrics" in data
    assert data["metrics"]["total_users"] >= 2  # Admin + Demo candidate
    assert data["metrics"]["total_questions"] >= 120
    assert data["storage"]["status"] == "ready"
