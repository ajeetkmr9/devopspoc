from fastapi.testclient import TestClient
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from src.controllers.version_controller import router as version_router
from src.controllers.conversion import router as conversion_router
from src.server.middlewares.config_middleware import ConfigMiddleware
from src.main import app

from unittest.mock import mock_open, patch
import pytest

version_client = TestClient(version_router)
conversion_client = TestClient(conversion_router)

def test_version():
    response = version_client.get("/version")
    assert response.status_code == 200
    
class MockConfig:
    def test_get_conversion():
        expected_response = {
            'cobol_cobol_cobol_85_cobol_2002_xxx',            
        }
        
        response = conversion_client.post("/conversion/convert")
        assert response.status_code == 200
        print(response)
        assert response.json() == expected_response