from fastapi import Request

from src.utils import constants
from src.models.model import LanguageConfig
from src.services.core.logging_service import LoggingService
from src.services.core.config_middleware import LoadFile

import json

class ConfigMiddleware:
    language_config = LanguageConfig({})
    version_config = {}

    def __init__(self, name: str):
        self.name = name

    async def load_config(self) -> True:
        return LoadFile().load_config_file(constants.LANGUAGE_METADATA_JSON_FILE_PATH)

    async def load_version_json(self) -> True:
        return LoadFile().load_version_json_file(constants.VERSION_JSON_FILE_PATH)

    async def __call__(self, request: Request, call_next):
        request.state.language_config = self.language_config
        request.state.meta_service_version = self.version_config
        response = await call_next(request)
        return response