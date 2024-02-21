from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/", tags=["Root"])
async def root(request: Request):
    """
        Root
    """
    return request.state.proxy_service_version

@router.get("/version", tags=["API Version"])
async def version(request: Request):
    """
        Application version
    """
    return request.state.proxy_service_version
