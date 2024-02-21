from fastapi import FastAPI, HTTPException, APIRouter, Request
from pydantic import BaseModel
from typing import Dict
from src.services.domain.unittest_service import UnitTestGenerationService
from src.models.model import UnitRequest


router = APIRouter()
@router.post("/unittest/generate", tags=["Unit Test Cases"])
async def get_unit_cases(request: UnitRequest,) -> Dict:
    """
    API to GET Generate cases.

    Return:-
        Return a str .
    """
    return UnitTestGenerationService().get_unit_cases(request)