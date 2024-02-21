from fastapi.testclient import TestClient
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from src.controllers.version_controller import router as version_router
from src.controllers.metadata import router as metadata_router
from src.server.middlewares.config_middleware import ConfigMiddleware

import pytest

version_client = TestClient(version_router)
metadata_client = TestClient(metadata_router)


class MockConfig:
    language_config = {
        "dependent_target_code_lang": {
            "cobol_test": {
                "source_frameworks": ["Cobol Test 85", "Cobol test 2002"],
                "target_frameworks": ["Fixed", "Free"],
                "converts": ["cobol_test", "java_test"],
            },
            "java_test": {
                "source_frameworks": [
                    "Java 17 Class Library using Java",
                    "Java 17 Console App using Java",
                ],
                "target_frameworks": [],
                "converts": ["cobol_test", "java_test"],
            },
        },
        "extension_map": {
            "cobol_test_85_java_test_8": [
                {"source": ".cbl", "target": ".java"},
                {"source": ".html", "target": ".js"},
            ]
        },
        "accessible_features": {
            "convertion": {},
            "documentation": {},
            "unit_testcase": {},
            "diagram": {},
        },
        "providers": [
            {
                "azure_openai": {
                    "models": [
                        {
                            "gpt-4": {
                                "token_limit": 1000,
                                "temperature": 0.7,
                                "top_p": 1,
                                "frequency_penalty": 1,
                                "presence_penalty": 1,
                            }
                        }
                    ]
                }
            },
        ],
    }


@pytest.fixture
def client(monkeypatch):
    config_middleware = ConfigMiddleware("ConfigMiddleware")
    config_middleware.language_config = MockConfig()

    app = FastAPI()
    app.include_router(metadata_router)
    app.include_router(version_router)

    app.add_middleware(BaseHTTPMiddleware, dispatch=config_middleware)
    return TestClient(app)

def test_version(client):
    response = client.get("/version")
    assert response.status_code == 200


def test_get_metadata_source_lang(client):
    response = client.get("/metadata/source_code")

    assert response.status_code == 200
    assert response.json() == ["cobol_test", "java_test"]


def test_get_metadata_target_lang(client):
    response = client.get(f'/metadata/target_code?language={"cobol_test"}')
    assert response.status_code == 200
    assert response.json() == ["cobol_test"]


def test_get_metadata_target_lang_invalid(client):
    response = client.get(f'/metadata/target_code?language={"cabol"}')

    assert response.status_code == 404
    assert response.json() == {"detail": "Source language not found!"}


def test_target_framework_positive(client):
    response = client.get("/metadata/target_frameworks?target_code_lang=cobol_test")
    assert response.status_code == 200
    assert response.json() == ["Fixed", "Free"]


def test_target_framework_negative(client):
    response = client.get("/metadata/target_frameworks?target_code_lang=cobal")
    assert response.status_code == 404
    assert response.json() == {"detail": "Provided language not found!"}


def test_target_framework_with_zero_frameworks(client):
    response = client.get("/metadata/target_frameworks?target_code_lang=java_test")
    assert response.status_code == 200
    assert response.json() == []


def test_target_src_framework_found(client):
    response = client.get(f"/metadata/source_frameworks?target_language=cobol_test")
    assert response.status_code == 200
    assert response.json() == ["Cobol Test 85", "Cobol test 2002"]


def test_source_framework_errorChcek(client):
    response = client.get("/metadata/source_frameworks?target_language=cabol")
    assert response.status_code == 404
    assert response.json() == {"detail": "Target language 'cabol' not found!"}


def test_target_srs_framework(client):
    response = client.get("/metadata/source_frameworks")
    assert response.status_code == 422
    assert "Field required" in response.text


def test_target_extension(client):
    expected_response = [
        {"source": ".cbl", "target": ".java"},
        {"source": ".html", "target": ".js"},
    ]
    response = client.get(
        "/metadata/file_extension?source_code_lang=cobol_test&target_code_lang=java_test&source_framework=85&target_framework=8"
    )
    assert response.status_code == 200
    assert response.json() == expected_response


def test_target_extension_with_invalid_value(client):
    expected_response = {
        "detail": "Source extension 'cobo_xxx_test_85_java_test_8' not found in metadata!"
    }
    response = client.get(
        "/metadata/file_extension?source_code_lang=cobo_xxx_test&target_code_lang=java_test&source_framework=85&target_framework=8"
    )
    assert response.status_code == 404
    assert response.json() == expected_response


def test_metadata_accessible_features(client):
    expected_response = {
        "convertion": {},
        "documentation": {},
        "unit_testcase": {},
        "diagram": {},
    }
    response = client.get("/metadata/accessible_features")
    assert response.status_code == 200
    assert response.json() == expected_response


def test_metadata_ai_provider(client):
    expected_response = [
        "azure_openai",
    ]
    response = client.get("/metadata/ai_provider")
    assert response.status_code == 200
    assert response.json() == expected_response
