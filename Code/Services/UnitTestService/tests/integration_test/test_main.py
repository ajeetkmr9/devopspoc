import pytest
from fastapi import HTTPException, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.testclient import TestClient
from src.server.middlewares.config_middleware import ConfigMiddleware
from src.controllers.version_controller import router as version_router
from src.controllers.unitcontroller import router as unit_router


@pytest.fixture
def client():
    app = FastAPI()
    config_middleware = ConfigMiddleware("ConfigMiddleware")
    app.include_router(unit_router)
    app.include_router(version_router)
    app.add_middleware(BaseHTTPMiddleware, dispatch=config_middleware)
    return TestClient(app)

@pytest.fixture
def unit_request_default():
        return {
            'source_language':'cobol',
            'target_testframework':'cobol 85',
            'provider':"fastapi",
            'model':"123",
            'code':"print('Hello, World!')"
        }

@pytest.fixture
def missing_field_unit_request():
    return {
        'source_language':'cobol',
        'target_testframework':'cobol 85',
        'provider':"fastapi",
        'code':"print('Hello, World!')"
    }

@pytest.fixture
def invalid_unit_empty_request():
    return  {
        "source_language": 123,
        "target_testframework":"pytest",
        "provider":"fastapi",
        "model":"123",
        "code":"print('Hello, World!')"
    }

def test_version(client):
    response = client.get("/version")
    assert response.status_code == 200

def test_get_unit_cases(client,unit_request_default):
    response=client.post("/unittest/generate",json=unit_request_default)
    assert response.status_code==200
    assert response.json() == {"Unit_test_case_generted": "cobol_cobol 85_fastapi_123_print('Hello, World!')"}

def test_get_unit_cases_no_body(client):
    response=client.post("/unittest/generate")
    assert response.status_code == 422
    assert 'Field required' in response.text

def test_get_unit_cases_missing_filed(client,missing_field_unit_request):
    response = client.post("/unittest/generate")
    assert response.status_code == 422
    assert 'Field required' in response.text
