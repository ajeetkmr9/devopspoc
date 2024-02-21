from fastapi.testclient import TestClient

from src.controllers.metadata import router as metadata_router

metadata_client = TestClient(metadata_router)

def test_root():
    response = metadata_client.get("/")
    assert response.status_code == 200