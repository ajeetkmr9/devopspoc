from src.models.model import LanguageConfig
from src.services.core.logging_service import LoggingService
import json

class LoadFile:
    async def load_config_file(self,file_path) -> True:
        try:
            with open(file_path, "r") as file:
                lang_config_data = json.load(file)
            self.language_config = LanguageConfig(language_json_data=lang_config_data)
        except FileNotFoundError:
            await LoggingService.error(f"{file_path} file not found in MetaDataService!")
        except Exception as e:
            await LoggingService.error(f"An unexpected error occurred during JSON file \"{file_path}\" read operation in MetaDataService: {e}")
        return True
