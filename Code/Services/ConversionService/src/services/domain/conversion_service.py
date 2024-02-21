from typing import List
from src.models.conversion_schema import Conversion

class ConversionService: 
    def _get_converted_code(request: Conversion) -> str:        
        data = f"{request.sourceLanguage}_{request.targetLanguage}_{request.sourceFramework}_{request.targetFramework}_{request.provider}_{request.model}_{request.code}"
        return data    
           
            