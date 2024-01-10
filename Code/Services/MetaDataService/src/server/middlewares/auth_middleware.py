from fastapi import Request
from src.services.core.logging_service import LoggingService

class AuthMiddleware:
    def __init__(self,name: str):
        self.name = name

    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        return response