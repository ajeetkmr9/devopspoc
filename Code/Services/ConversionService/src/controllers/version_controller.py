from fastapi import APIRouter

router = APIRouter()

@router.get("/version", tags=["Get Version"])
async def getVersion():
    return "v1.0.0"