from fastapi import APIRouter, Request

from src.services.core.logging_service import LoggingService

router = APIRouter()

@router.get("/", tags=["Root"])
async def root(request: Request):
    """
        Root
    """
    return request.state.meta_service_version

@router.get("/version", tags=["API Version"])
async def version(request: Request):
    """
        Application version
    """
    return request.state.meta_service_version