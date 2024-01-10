from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return "Hello"

@router.get("/version")
async def getVersion():
    return "v1.0.0"