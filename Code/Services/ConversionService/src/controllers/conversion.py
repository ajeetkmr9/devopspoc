from fastapi import APIRouter, Request, Query, HTTPException
from src.services.domain.conversion_service import ConversionService
from src.models.conversion_schema import Conversion
import inspect
import logging

logger = logging.getLogger("Conversion Service API Logs: ")

router = APIRouter()

@router.post("/conversion/convert", tags=["Target supported code conversion"])
async def get_conversion(request: Conversion) -> dict:
    """
    Description:
        API to get all the target conversion code for the specified languages and frameworks.
    Params:
        sourceLanguage: Source code language.
        targetLanguage: Target code language.
        sourceFramework: Source code framework.
        targetFramework: Target code framework.
        provider: Provider information.
        model: Model information.
        code: Code information.
    Returns:
        Dictionary with the key 'source_code' containing the converted code.
    Raises:
        HTTPException: If an error occurs while handling the request.
    """
    logger.debug(f'Entering API method: {inspect.currentframe().f_code.co_name}()')
             
    data = ConversionService._get_converted_code(request)
    logger.debug(f'Returning from API method: {inspect.currentframe().f_code.co_name}()')
    return {"source_code": data}
    