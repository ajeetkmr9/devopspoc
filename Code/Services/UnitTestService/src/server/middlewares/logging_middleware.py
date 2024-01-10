from fastapi import Request

from src.services.core.logging_service import LoggingService

class LoggingMiddleware:
    def __init__(self, name: str):
        self.name = name
    
    async def __call__(self, request: Request, call_next):
        route = LoggingMiddleware.endpoint(request)
        x_correlation_id = request.headers.get('X-Correlation-ID', 'None')
        request_info = {
            "method": request.method,
            "query_params": dict(request.query_params),
            "body": await request.body(),
            "x-correlation-id": x_correlation_id
        }
        if route:
            request_info.update({
                "path":route[0].path,
                "endpoint": route[0].name
            })
        await LoggingService.debug(request, f"Received request: {request_info}")

        response = await call_next(request)
        response_info = {
            "status_code":response.status_code,
            "x-correlation-id": x_correlation_id
        }
        if route:
            response_info.update({
                "path":route[0].path,
                "endpoint": route[0].name
            })
        await LoggingService.debug(response, f"Response for request: {response_info}")
        return response

    @staticmethod
    def endpoint(request: Request):
        return list(filter(lambda route: route.path == request.url.path, request.app.routes))
