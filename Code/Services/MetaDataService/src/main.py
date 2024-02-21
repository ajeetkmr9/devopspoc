from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.server.middlewares.exception_middleware import ExceptionMiddleware
from src.server.middlewares.auth_middleware import AuthMiddleware
from src.server.middlewares.config_middleware import ConfigMiddleware
from src.server.middlewares.logging_middleware import LoggingMiddleware

from src.controllers.metadata import router as metadata_router
from src.controllers.version_controller import router as version_router

import asyncio

def get_application() -> FastAPI:
    application = FastAPI(
        title="Service API",
        description="Fast API for MetaData Service",
        version="0.0.1"
    )
    return application

app = get_application()

# Include Routers
app.include_router(metadata_router)
app.include_router(version_router)

#####################
# Include Middlewares
#####################
configuration_middleware = ConfigMiddleware("ConfigMiddleware")
app.add_middleware(BaseHTTPMiddleware, dispatch=LoggingMiddleware("LoggingMiddleware"))
app.add_middleware(BaseHTTPMiddleware, dispatch=AuthMiddleware("AuthMiddleware"))
app.add_middleware(BaseHTTPMiddleware, dispatch=ExceptionMiddleware("ExceptionHandler"))
app.add_middleware(BaseHTTPMiddleware, dispatch=configuration_middleware)

async def load_config_files(configuration_middleware):
    await configuration_middleware.load_config()
    await configuration_middleware.load_version_json()

loop = asyncio.get_event_loop()
task = asyncio.create_task(load_config_files(configuration_middleware))