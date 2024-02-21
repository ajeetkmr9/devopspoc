import pytest

from fastapi import HTTPException
from src.models.model import LanguageConfig
from src.services.domain.conversion_service import ConversionService
from src.models.conversion_schema import Conversion

class TestConversionService():    
    def test_get_converted_code(self):        
        request = Conversion(sourceLanguage='cobol', targetLanguage='cobol',sourceFramework='cobol', targetFramework='85', provider='cobol', model='2002',code='xxx')
        expected_result = 'cobol_cobol_cobol_85_cobol_2002_xxx' 
        result = ConversionService._get_converted_code(request)
        assert result == expected_result