import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from src.application.services.ai_engine_service import AIAnalysisResult
from src.infrastructure.ai_engine.ollama_adapter import OllamaAIEngine
from src.presentation.api.dependencies import get_ai_engine
from src.presentation.api.main import app


@pytest.fixture(autouse=True)
def mock_ai_engine_dep():
    mock_ai = AsyncMock(spec=OllamaAIEngine)
    mock_ai.analyze_case.return_value = AIAnalysisResult(
        summary="Automated analysis",
        threat_level="medium",
        confidence_score=0.7,
        recommended_actions=["Investigate"],
        similar_cases=[],
    )
    app.dependency_overrides[get_ai_engine] = lambda: mock_ai
    yield mock_ai
    app.dependency_overrides.pop(get_ai_engine, None)


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_create_case(client):
    tenant_id = str(uuid4())
    payload = {
        "title": "SQL Injection Attack",
        "description": "Detected SQL injection in web app",
        "priority": "high",
        "client_tenant_id": tenant_id,
    }
    response = await client.post("/api/v1/cases/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "SQL Injection Attack"
    assert data["status"] == "open"
    assert data["priority"] == "high"
    assert data["client_tenant_id"] == tenant_id


@pytest.mark.asyncio
async def test_get_case_not_found(client):
    response = await client.get(f"/api/v1/cases/{uuid4()}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_and_get_case(client):
    tenant_id = str(uuid4())
    payload = {
        "title": "Phishing Email Detected",
        "description": "User received phishing email",
        "priority": "medium",
        "client_tenant_id": tenant_id,
    }
    create_response = await client.post("/api/v1/cases/", json=payload)
    assert create_response.status_code == 201
    case_id = create_response.json()["id"]

    get_response = await client.get(f"/api/v1/cases/{case_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == case_id
    assert get_response.json()["title"] == "Phishing Email Detected"


@pytest.mark.asyncio
async def test_close_case(client):
    tenant_id = str(uuid4())
    payload = {
        "title": "DDoS Attack",
        "description": "High traffic detected",
        "priority": "critical",
        "client_tenant_id": tenant_id,
    }
    create_response = await client.post("/api/v1/cases/", json=payload)
    case_id = create_response.json()["id"]

    close_response = await client.post(f"/api/v1/cases/{case_id}/close")
    assert close_response.status_code == 200
    assert close_response.json()["status"] == "closed"


@pytest.mark.asyncio
async def test_list_cases(client):
    tenant_id = str(uuid4())
    for i in range(3):
        await client.post(
            "/api/v1/cases/",
            json={
                "title": f"Case {i}",
                "description": f"Description {i}",
                "priority": "low",
                "client_tenant_id": tenant_id,
            },
        )
    response = await client.get(f"/api/v1/cases/?tenant_id={tenant_id}")
    assert response.status_code == 200
    assert len(response.json()) == 3
