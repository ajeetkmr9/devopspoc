from typing import Dict

from fastapi import APIRouter
from src.models.proxy_model import ProxyRequest
from src.services.domain.proxy_service import ProxyService


router = APIRouter()


@router.post("/genai/convert_code", tags=["Convert Code"])
async def get_converted_code(request: ProxyRequest,) -> Dict:
    """
    API to GET converted code.

    Param:-
        request: ProxyRequest .

    Return:-
        Return a str of code conversion.
    """

    #TODO: chuncking and merging and prompt handler

    return ProxyService().get_converted_code(request)
