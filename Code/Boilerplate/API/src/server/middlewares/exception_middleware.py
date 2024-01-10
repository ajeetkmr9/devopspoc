from fastapi import Request
from exceptions.exception_handler import ExceptionHandler

class ExceptionMiddleware:
    def __init__(self, name: str):
        self.name = name

    async def __call__(self, request: Request, call_next):
        try:         
            # process the request and get the response    
            response = await call_next(request)
        except Exception as e:	
            return { "error": ExceptionHandler().handle_exception(e)}
        return response