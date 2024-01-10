from pydantic import BaseModel


class ProxyRequest(BaseModel):
    source_language: str
    target_language: str
    source_framework: str
    target_framework: str
    provider: str
    model: str
    code: str

