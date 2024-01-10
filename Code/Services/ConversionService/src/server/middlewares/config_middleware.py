from fastapi import Request, FastAPI

from src.models.model import LanguageConfig

import json

class ConfigMiddleware:
    language_config = None

    def __init__(self, name: str):
        self.name = name
        self.load_config()

    def load_config(self) -> LanguageConfig:
        with open("src/data_adapter/languages_conversion.json", "r") as file:
            lang_config_data = json.load(file)
        self.language_config = LanguageConfig(language_json_data=lang_config_data)

    async def __call__(self, request: Request, call_next):
        request.state.language_config = self.language_config
        response = await call_next(request)
        return response
    
    def set_test_config(self, config: LanguageConfig):
        self.language_config = config