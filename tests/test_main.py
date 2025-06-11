import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_shorten_url():
    payload = {"original_url": "https://www.google.com"}
    response = client.post("/shorten/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "original_url" in data
    assert "short_url" in data
    assert data["original_url"] == payload["original_url"]
    assert len(data["short_url"]) <= 8
