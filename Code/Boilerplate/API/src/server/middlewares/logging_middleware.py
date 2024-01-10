
from fastapi import Request

from services.core.logging_service import LoggingService

class LoggingMiddleware:
    def __init__(self, name: str):
        self.name = name
    
    async def __call__(self, request: Request, call_next):
        await LoggingService.debug(request.json)
        # process the request and get the response    
        response = await call_next(request)
        await LoggingService.debug(response)
        return response