import pytest

from fastapi import HTTPException
from src.models.model import LanguageConfig
from src.services.domain.metadata_service import MetadataService


class TestMetadataService:
    @pytest.fixture
    def language_json_data_default(self):
        return LanguageConfig(
            language_json_data={
                "dependent_target_code_lang": {
                    "cobol": {
                        "source_frameworks": ["Cobol 85", "Cobol 2002"],
                        "target_frameworks": ["Fixed", "Free"],
                        "converts": ["cobol", "java"],
                    },
                    "java": {
                        "source_frameworks": [
                            "Java 17 Class Library using Java",
                            "Java 17 Console App using Java",
                        ],
                        "target_frameworks": [],
                        "converts": ["cobol", "java"],
                    },
                },
                "extension_map": {
                    "cobol_java_85_8": [
                        {"source": ".cbl", "target": ".java"},
                        {"source": ".html", "target": ".jscript"},
                        {"source": ".html", "target": ""},
                    ]
                },
                "providers": [
                    {
                        "azure_openai": {
                            "models": [
                                {
                                    "gpt-4": {
                                        "token_limit": 1000,
                                        "temperature": 0.7,
                                        "top_p": 1,
                                        "frequency_penalty": 1,
                                        "presence_penalty": 1,
                                    }
                                }
                            ]
                        }
                    }
                ],
            }
        )

    @pytest.fixture
    def language_json_with_two_valid_frameworks(self):
        return LanguageConfig(
            language_json_data={
                "dependent_target_code_lang": {
                    "cobol": {
                        "source_frameworks": ["Cobol 85", "Cobol 2002"],
                        "target_frameworks": ["Fixed", "Free"],
                        "converts": ["cobol", "java"],
                    },
                    "java": {
                        "source_frameworks": [
                            "Java 17 Class Library using Java",
                            "Java 17 Console App using Java",
                        ],
                        "target_frameworks": ["Fixed", "Free"],
                        "converts": ["cobol", "java"],
                    },
                }
            }
        )

    @pytest.fixture
    def invalid_misspelled_language_json_data(self):
        return LanguageConfig(
            language_json_data={
                "dependent_target_code_lang": {
                    "coboll": {
                        "source_frameworks": ["Cobol 85", "Cobol 2002"],
                        "target_frameworks": ["Fixed", "Free"],
                        "converts": ["cobol", "java"],
                    },
                    "java": {
                        "source_frameworks": [
                            "Java 17 Class Library using Java",
                            "Java 17 Console App using Java",
                        ],
                        "target_frameworks": [],
                        "converts": ["cobol", "java"],
                    },
                }
            }
        )

    def test_valid_source_languages(self, language_json_data_default):
        """
        Passed Test case for source languages whose source_frameworks is not false.
        """

        expected_source_languages = ["cobol", "java"]
        result = MetadataService().get_metadata_source_lang(language_json_data_default)
        assert result == expected_source_languages

    def test_get_metadata_target_lang(self, language_json_data_default):
        """
        Passed target frameworks for only cobol.

        """
        expected_target_languages = ["cobol"]
        result = MetadataService().get_metadata_target_lang(
            "java", language_json_data_default
        )
        assert result == expected_target_languages

    def test_get_metadata_target_lang_with_two_valid_framework(
        self, language_json_with_two_valid_frameworks
    ):
        """
        Passed target_framework value for cobol & java language both.

        """
        expected_target_languages = ["cobol", "java"]
        result = MetadataService().get_metadata_target_lang(
            "java", language_json_with_two_valid_frameworks
        )
        assert result == expected_target_languages

    def test_get_metadata_target_lang_misspelled_with_source_language(
        self, invalid_misspelled_language_json_data
    ):
        """
        Test case for misspelled language

        """
        with pytest.raises(HTTPException) as exc_info:
            MetadataService().get_metadata_target_lang(
                "cobol", invalid_misspelled_language_json_data
            )
        assert exc_info.value.status_code == 404

    def test_valid_target_languages(self, language_json_data_default):
        """
        Passed target framework for only cobol.

        """
        expected_target_languages = ["cobol"]
        result = MetadataService().get_metadata_target_lang(
            "java", language_json_data_default
        )
        assert result == expected_target_languages

    def test_valid_target_languages_two(self, language_json_with_two_valid_frameworks):
        """
        Passed target_framework value for cobol & java language both.

        """
        expected_target_languages = ["cobol", "java"]
        result = MetadataService().get_metadata_target_lang(
            "java", language_json_with_two_valid_frameworks
        )
        assert result == expected_target_languages

    def test_valid_target_languages_three(self, invalid_misspelled_language_json_data):
        """
        Test case for misspelled language

        """
        with pytest.raises(HTTPException) as exc_info:
            MetadataService().get_metadata_target_lang(
                "cobol", invalid_misspelled_language_json_data
            )
        assert exc_info.value.status_code == 404

    def test_valid_target_frameworks(self, language_json_data_default):
        """
        Test case for target frameworks

        """
        expected_target_languages = ["Fixed", "Free"]
        result = MetadataService().get_metadata_target_frameworks(
            "cobol", language_json_data_default
        )
        assert result == expected_target_languages

    def test_valid_target_empty_frameworks(self, language_json_data_default):
        """
        Test case for empty target frameworks

        """
        result = MetadataService().get_metadata_target_frameworks(
            "java", language_json_data_default
        )
        assert result == []

    def test_invalid_target_empty_frameworks(
        self, invalid_misspelled_language_json_data
    ):
        """
        Test case for invalid target frameworks

        """
        with pytest.raises(HTTPException) as exc_info:
            MetadataService().get_metadata_target_frameworks(
                "cobol", invalid_misspelled_language_json_data
            )
        assert exc_info.value.status_code == 404

    def test_valid_source_frameworks(self, language_json_data_default):
        """
        Test case for Source frameworks

        """
        expected_target_languages = ["Cobol 85", "Cobol 2002"]
        result = MetadataService().get_source_frameworks(
            "cobol", language_json_data_default
        )
        assert result == expected_target_languages

    def test_valid_source_frameworks1(self, language_json_data_default):
        """
        Test case for Source frameworks

        """
        expected_target_languages = [
            "Java 17 Class Library using Java",
            "Java 17 Console App using Java",
        ]
        result = MetadataService().get_source_frameworks(
            "java", language_json_data_default
        )
        assert result == expected_target_languages

    def test_invalid_target_empty_frameworks(
        self, invalid_misspelled_language_json_data
    ):
        """
        Test case for invalid Source frameworks

        """
        with pytest.raises(HTTPException) as raised_excep_info:
            MetadataService().get_source_frameworks(
                "invalid source frameworks", invalid_misspelled_language_json_data
            )
        assert raised_excep_info.value.status_code == 404

    def test_valid_target_extension(self, language_json_data_default):
        """
        Passed source_code_lang, target_code_lang, src_framework, trg_framework value to get extension.

        """
        expected_target_extension = [
            {"source": ".cbl", "target": ".java"},
            {"source": ".html", "target": ".jscript"},
            {"source": ".html", "target": ""},
        ]
        result = MetadataService().get_metadata_file_extension(
            "cobol", "java", "85", "8", language_json_data_default
        )
        assert result == expected_target_extension

    def test_Ivalid_target_extension(self, invalid_misspelled_language_json_data):
        """
        Test case for invalid target extension

        """
        with pytest.raises(HTTPException) as exc_info:
            MetadataService().get_metadata_file_extension(
                "cobol", "java", "XXX", "XXX", invalid_misspelled_language_json_data
            )
        assert exc_info.value.status_code == 404

    def test_ai_provider(self, language_json_data_default):
        """
        Passed Lang_config Get Ai Provider .

        """
        expected_target_extension = [
            "azure_openai",
        ]
        result = MetadataService().get_ai_provider(
            lang_config=language_json_data_default
        )
        assert result == expected_target_extension
