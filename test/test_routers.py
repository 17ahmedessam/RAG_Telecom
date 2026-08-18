from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

def test_health_check_endpoint():
    """INTEGRATION TEST: Verifies root health check GET endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "/docs" in response.json()["docs_url"]

@patch("src.routers.query_router.rag_service.answer_ticket")
def test_query_endpoint_success(mock_answer_ticket):
    """INTEGRATION TEST: Verifies /api/v1/query POST endpoint with valid payload and token usage."""
    mock_answer_ticket.return_value = {
        "ticket": "النت فاصل",
        "response": "أهلاً بك، سنتأكد من الخط.",
        "sources_count": 3,
        "execution_time_seconds": 0.45,
        "prompt_tokens": 120,
        "completion_tokens": 30,
        "total_tokens": 150
    }
    
    payload = {"ticket": "النت فاصل"}
    response = client.post("/api/v1/query", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["ticket"] == "النت فاصل"
    assert data["sources_count"] == 3
    assert data["prompt_tokens"] == 120
    assert data["completion_tokens"] == 30
    assert data["total_tokens"] == 150

def test_query_endpoint_empty_validation():
    """INTEGRATION TEST: Verifies Pydantic/HTTP 400 validation on empty payload."""
    payload = {"ticket": "   "}
    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 400
