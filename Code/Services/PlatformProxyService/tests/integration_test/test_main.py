import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from src.controllers.proxy_controller import router as proxy_router
from src.controllers.version_controller import router as version_router

from src.server.middlewares.config_middleware import ConfigMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


@pytest.fixture
def client():
    app = FastAPI()
    config_middleware = ConfigMiddleware("ConfigMiddleware")
    app.include_router(proxy_router)
    app.include_router(version_router)
    app.add_middleware(BaseHTTPMiddleware, dispatch=config_middleware)
    return TestClient(app)


@pytest.fixture
def proxy_request():
    return {
            'source_language':'cobol',
            'target_language':'cobol',
            'source_framework':'cobol',
            'target_framework':'85',
            'provider':'cobol',
            'model':'2002',
            'code':'xxx'
        }

@pytest.fixture
def proxy_request_missing_data():
    return {
        'source_language':'cobol',
        'target_language':'cobol',
        'source_framework':'cobol',
        'target_framework':'cobol',
        'provider':'cobol',
        'model':'2002',
    }

@pytest.fixture
def proxy_request_invalid_data():
    return {
        'source_language':'cobol',
        'target_language':'cobol',
        'source_framework':'cobol',
        'target_framework':85,
        'provider':'cobol',
        'model':'2002',
        'code':'xxx'
    }


def test_version(client):
    response = client.get("/version")
    assert response.status_code == 200


def test_get_converted_code(client, proxy_request):
    response = client.post("/genai/convert_code", json=proxy_request)
    assert response.status_code == 200
    assert response.json() == {'converted_code': 'cobol_cobol_cobol_85_cobol_2002_xxx'}


def test_get_converted_code_no_body(client):
    response = client.post("/genai/convert_code")
    assert response.status_code == 422
    assert 'Field required' in response.text


def test_get_converted_code_missing_field(client, proxy_request_missing_data):
    response = client.post("/genai/convert_code", json=proxy_request_missing_data)
    assert response.status_code == 422
    assert "Field required" in str(response.text)


def test_get_converted_code_invalid_data(client, proxy_request_invalid_data):
    response = client.post("/genai/convert_code", json=proxy_request_invalid_data)
    assert response.status_code == 422
    assert "Input should be a valid string" in str(response.text)

