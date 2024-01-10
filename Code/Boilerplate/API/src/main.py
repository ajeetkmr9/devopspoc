from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from server.middlewares.exception_middleware import ExceptionMiddleware
from server.middlewares.auth_middleware import AuthMiddleware
from server.middlewares.config_middleware import ConfigMiddleware
from server.middlewares.logging_middleware import LoggingMiddleware

from controllers.version_controller import router

import logging

logger = logging.getLogger(__name__)

def get_application() -> FastAPI:
    application = FastAPI(
        title="Service API",
        description="Fast API for GEN AI Services",
        version="0.0.1"
    )
    return application

app = get_application()

# Include Routers
app.include_router(router)

#####################
# Include Middlewares
#####################
app.add_middleware(BaseHTTPMiddleware, dispatch=ConfigMiddleware(name="ConfigMiddleware"))
app.add_middleware(BaseHTTPMiddleware, dispatch=AuthMiddleware("AuthMiddleware"))
app.add_middleware(BaseHTTPMiddleware, dispatch=LoggingMiddleware("LoggingMiddleware"))
app.add_middleware(BaseHTTPMiddleware, dispatch=ExceptionMiddleware("ExceptionHandler"))
    
