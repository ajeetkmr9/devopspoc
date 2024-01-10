import pytest
from pydantic import ValidationError
from src.models.proxy_model import ProxyRequest
from src.services.domain.proxy_service import ProxyService


class TestProxyService():

    @pytest.fixture
    def proxy_request_data_default(self):
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
    def proxy_request_missing_data(self):
        return {
            'source_language':'cobol',
            'target_language':'cobol',
            'source_framework':'cobol',
            'target_framework':'cobol',
            'provider':'cobol',
            'model':'2002',
        }

    @pytest.fixture
    def proxy_request_invalid_data(self):
        return {
            'source_language':'cobol',
            'target_language':'cobol',
            'source_framework':'cobol',
            'target_framework':85,
            'provider':'cobol',
            'model':'2002',
            'code':'xxx'
        }

    def test_get_converted_code(self, proxy_request_data_default):
        request = ProxyRequest(**proxy_request_data_default)
        expected_result = {'converted_code': 'cobol_cobol_cobol_85_cobol_2002_xxx'}
        result = ProxyService().get_converted_code(request)
        assert result == expected_result

    def test_get_converted_code_validation_error(self, proxy_request_invalid_data):
        with pytest.raises(ValidationError) as exc_info:
            ProxyRequest(**proxy_request_invalid_data)
        assert "Input should be a valid string" in str(exc_info.value)

    def test_get_converted_code_missing_field(self, proxy_request_missing_data):
        with pytest.raises(ValidationError) as exc_info:
            ProxyRequest(**proxy_request_missing_data)
        assert "Field required" in str(exc_info.value)

