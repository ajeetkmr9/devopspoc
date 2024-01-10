import json

from fastapi import Request

from src.utils import constants

from src.services.core.logging_service import LoggingService


class ConfigMiddleware:
    version_config = {}

    def __init__(self, name: str):
        self.name = name

    async def load_version_json(self) -> True:
        try:
            with open(constants.VERSION_JSON_FILE_PATH, "r") as version_file:
                version = json.load(version_file)
            self.version_config = version
        except FileNotFoundError:
            await LoggingService.error(f"{constants.VERSION_JSON_FILE_PATH} file not found in ProxyService!")
        except Exception as e:
            await LoggingService.error(f"An unexpected error occurred during JSON file \"{constants.VERSION_JSON_FILE_PATH}\" read operation in ProxyService: {e}")
        return True

    async def __call__(self, request: Request, call_next):
        request.state.proxy_service_version = self.version_config
        response = await call_next(request)
        return response
