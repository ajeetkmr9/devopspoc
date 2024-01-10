from pydantic import BaseModel

class Conversion(BaseModel):        
        sourceLanguage: str
        targetLanguage: str
        sourceFramework: str
        targetFramework: str
        provider: str
        model: str
        code: str