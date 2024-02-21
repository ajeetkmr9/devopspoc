from typing import List
from typing import Dict, Any

from fastapi import HTTPException
from src.models.model import LanguageConfig
from src.utils import constants


class MetadataService:
    def get_metadata_source_lang(self, lang_config: LanguageConfig) -> List[str]:
        """
        Gets the list of all source languages whose source framework is not false.

        Args:
            lang_config: Class LanguageConfig object

        Returns:
            List[str]: A list of source languages whose source framework is not false. Returns an empty list if not found.

        Raises: None
        """
        source_languages = []
        metadata = lang_config.language_config

        if not metadata:
            return source_languages

        source_code_language_meta = metadata.get(
            constants.DEPENDENT_TARGET_CODE_LANGUAGE
        )
        for key, value in source_code_language_meta.items():
            if value[constants.SOURCE_FRAMEWORKS]:
                source_languages.append(key)

        return source_languages

    def get_metadata_target_lang(
        self, lang: str, lang_config: LanguageConfig
    ) -> List[str]:
        """
                Description:-
                    Get the list of target frameworks for a given language from the metadata.

                Args:-
                    language (str): The programming language for which to retrieve target frameworks.
                    lang_config: Class LanguageConfig object

                Returns:-
                    List[str]: A list of target frameworks for the specified language and returns an empty list if not found.

                Raises:-
                    KeyError: If the specified language or target framework is not found in the metadata.
        l
        """
        target_languages = []
        metadata = lang_config.language_config

        if not metadata:
            return target_languages

        source_code_language_meta = metadata.get(
            constants.DEPENDENT_TARGET_CODE_LANGUAGE, {}
        )

        if lang not in source_code_language_meta:
            raise HTTPException(status_code=404, detail="Source language not found!")

        possible_target_languages = source_code_language_meta.get(lang, {}).get(
            "converts", []
        )

        for lang in possible_target_languages:
            if source_code_language_meta.get(lang, {}).get(constants.TARGET_FRAMEWORKS):
                target_languages.append(lang)

        return target_languages

    def get_source_frameworks(
        self, target_language: str, lang_config: LanguageConfig
    ) -> List[str]:
        """
        Args:-
            target_language: The programming language for which to retrieve target frameworks.
            lang_config: Class LanguageConfig object

        Returns:List[str]: A list of source code frameworks for the specified target language.

        This method relies on the presence of language configurations, and it raises HTTPExceptions for error handling.

        Raises:
            HTTPException:
            - status_code 404: If the target language is not found in the language configuration.
            - status_code 500: If the language configuration is not available."""

        source_frameworks = []
        metadata = lang_config.language_config

        if not metadata:
            return source_frameworks

        source_code_language_meta = metadata.get(
            constants.DEPENDENT_TARGET_CODE_LANGUAGE, {}
        )

        if target_language not in source_code_language_meta:
            raise HTTPException(
                status_code=404,
                detail=f"Target language '{target_language}' not found!",
            )

        source_frameworks = source_code_language_meta.get(target_language, {}).get(
            constants.SOURCE_FRAMEWORKS, []
        )

        return source_frameworks

    def get_metadata_target_frameworks(
        self, language: str, lang_config: LanguageConfig
    ) -> List[str]:
        """
        Get the list of target frameworks for a given language from the metadata.

        Args:
            language: The programming language for which to retrieve target frameworks.
            lang_config: Class LanguageConfig object

        Returns:
            List[str]: A list of target frameworks for the specified language. Returns an empty list if not found.

        Raises:
            HTTPException 404: If the specified language or target framework is not found in the metadata.
        """
        target_frameworks = []
        metadata = lang_config.language_config

        if not metadata:
            return target_frameworks

        if constants.DEPENDENT_TARGET_CODE_LANGUAGE in metadata:
            language_data = metadata[constants.DEPENDENT_TARGET_CODE_LANGUAGE].get(
                language, {}
            )

            if not language_data:
                raise HTTPException(
                    status_code=404, detail="Provided language not found!"
                )

            target_frameworks = language_data.get(constants.TARGET_FRAMEWORKS, [])

        return target_frameworks

    def accessible_features(
        self, lang_config: LanguageConfig
    ) -> Dict[str, Dict[str, Any]]:
        """
        Description:-
            Get the list of accessible features from the language metadata.

        Args:-
            lang_config: Dict containing language metadata information

        Returns:-
            List[Dict[str, Any]]: A list of dict containing all accessible features.

        Raises:-
            None
        """
        accessible_features = []
        metadata = lang_config.language_config

        if not metadata:
            return accessible_features

        return lang_config.language_config.get("accessible_features", [])

    def get_metadata_file_extension(
        self,
        source_code_lang: str,
        source_framework: str,
        target_code_lang: str,
        target_framework: str,
        lang_config: LanguageConfig,
    ) -> List[dict]:
        """
        Description:-
            Get the list of target extension for the given parameters from the metadata.

        Args:-
            Extension (str): The source code language, target code, source code framework and target code framework for which to retrieve target extension.
            lang_config: Dict containing language metadata information

        Returns:-
            List[dict]: A list of target language and frameworks for the specified extension and returns an empty list if not found.

        Raises:-
            HTTPException 404: If the specified extension or target framework is not found in the metadata.

        """
        extension = f"{source_code_lang}_{source_framework}_{target_code_lang}_{target_framework}"
        target_extension = []
        metadata = lang_config.language_config

        if not metadata:
            return target_extension

        extension_map = metadata.get("extension_map", {})
        if extension not in extension_map:
            raise HTTPException(
                status_code=404,
                detail=f"Source extension '{extension}' not found in metadata!",
            )

        target_extension.extend(extension_map[extension])

        return target_extension

    def get_ai_provider(self, lang_config: LanguageConfig) -> list[str]:
        """
        Description:-
            Get The List Of All Ai Providers From The Language Metadata.

        Args:-
            lang_config: Dict containing language metadata information

        Returns:-
            List[str,]: A list of str containing all Ai Providers .

        Raises:-
            None
        """
        providers = []
        metadata = lang_config.language_config
        if not metadata:
            return providers
        providers = [
            list(item.keys())[0]
            for item in lang_config.language_config.get("providers", [])
        ]
        return providers
