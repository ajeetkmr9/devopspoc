from fastapi import Request
from fastapi.responses import JSONResponse
from src.exceptions.exception_handler import ExceptionHandler
from src.services.core.logging_service import LoggingService

import logging
logger = logging.getLogger()

class ExceptionMiddleware:
    def __init__(self, name: str):
        self.name = name

    async def __call__(self, request: Request, call_next):
        await LoggingService.debug(request)
        try:         
            response = await call_next(request)
        except Exception as e:
            return JSONResponse(
                content={"error":  ExceptionHandler().handle_exception(e)}, 
                status_code=500
            )
        return response