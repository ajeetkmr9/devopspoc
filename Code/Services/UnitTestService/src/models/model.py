from pydantic import BaseModel


class UnitRequest(BaseModel):
    source_language: str
    target_testframework: str
    provider: str
    model: str
    code: str
