from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError
from pydantic import BaseModel

import pytest

from src.models.model import UnitRequest
from src.services.domain.unittest_service import UnitTestGenerationService


class TestUnitService:

    @pytest.fixture
    def unit_request_default(self):
        return {
            'source_language':'cobol',
            'target_testframework':'cobol 85',
            'provider':"fastapi",
            'model':"123",
            'code':"print('Hello, World!')"
        }

    @pytest.fixture
    def missing_unit_request(self):
        return {
            'source_language':'cobol',
            'target_testframework':'cobol 85',
            'provider':"fastapi",
            'code':"print('Hello, World!')"
        }

    @pytest.fixture
    def invalid_unit_empty_request(self):
        return  {
            "source_language": 123,
            "target_testframework":"pytest",
            "provider":"fastapi",
            "model":"123",  # Intentionally set an invalid value
            "code":"print('Hello, World!')"
        }

    def test_get_unit_cases(self, unit_request_default):
        request = UnitRequest(**unit_request_default)
        expected_result = {"Unit_test_case_generted": "cobol_cobol 85_fastapi_123_print('Hello, World!')"}
        result = UnitTestGenerationService().get_unit_cases(request)
        assert result == expected_result

    def test_get_converted_code_validation_error(self, missing_unit_request):
        with pytest.raises(ValidationError) as exc_info:
            UnitRequest(**missing_unit_request)
        assert "Field required" in str(exc_info.value)

    def test_get_converted_code_missing_field(self, invalid_unit_empty_request):
        with pytest.raises(ValidationError) as exc_info:
            UnitRequest(**invalid_unit_empty_request)
        assert "Input should be a valid string" in str(exc_info.value)
