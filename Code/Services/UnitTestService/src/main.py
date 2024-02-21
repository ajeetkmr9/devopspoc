from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.server.middlewares.exception_middleware import ExceptionMiddleware
from src.server.middlewares.auth_middleware import AuthMiddleware
from src.server.middlewares.config_middleware import ConfigMiddleware
from src.server.middlewares.logging_middleware import LoggingMiddleware

from src.controllers.unitcontroller import router as unit_router
from src.controllers.version_controller import router as version_router

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
app.include_router(unit_router)
app.include_router(version_router)

#####################
# Include Middlewares
#####################
app.add_middleware(BaseHTTPMiddleware, dispatch=AuthMiddleware("AuthMiddleware"))
app.add_middleware(BaseHTTPMiddleware, dispatch=ExceptionMiddleware("ExceptionHandler"))
app.add_middleware(BaseHTTPMiddleware, dispatch=LoggingMiddleware("LoggingMiddleware"))
app.add_middleware(BaseHTTPMiddleware, dispatch=ConfigMiddleware("ConfigMiddleware"))
    
