from fastapi import Request

class AuthMiddleware:
    def __init__(self,name: str):
        self.name = name

    async def __call__(self, request: Request, call_next):

        # process the request and get the response    
        response = await call_next(request)
        
        return response