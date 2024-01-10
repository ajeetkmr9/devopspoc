from fastapi import APIRouter, Request, Query
from src.services.domain.metadata_service import MetadataService
from typing import List
from typing import Dict, Any

router = APIRouter()


@router.get(
    "/metadata/source_code",
    tags=["Source Code Languages"],
)
async def get_metadata_source_lang(request: Request) -> List[str]:
    """
    Description:-
        API to GET all the Source languages whose source framework is not False.

    Args:
        request: Fast API Request Object

    Returns:
        List[str]: A list of source languages. Returns an empty list if not found.

    Raises: None
    """
    data = MetadataService().get_metadata_source_lang(
        lang_config=request.state.language_config
    )
    return data


@router.get("/metadata/target_code", tags=["Target Code Supported Languages"])
async def get_metadata_target_lang(
    request: Request, language: str = Query(..., description="Source Language")
) -> List[str]:
    """
    Description:-
        API to GET all the target languages which belongs to "language" "coverts" & these "converts"
        langauges target framework is not False.

    Param:-
        request: Fast API Request Object
        language: Target code language

    Return:-
        Return a List of target code language

    Raise:-
        HttpExceptionError: If the specified language or target framework is not found in the metadata.
    """
    data = MetadataService().get_metadata_target_lang(
        lang=language.lower(), lang_config=request.state.language_config
    )
    return data


@router.get(
    "/metadata/source_frameworks", tags=["Source Frameworks for Target Language"]
)
async def get_source_frameworks(
    request: Request,
    target_language: str = Query(..., description="Target Language"),
) -> List[str]:
    """
    Description:-
        API to GET all the source frameworks for a given target language.

    Parameters:
        request: Fast API Request Object
        target_language: Target language for which source frameworks are requested.

    Returns:
        List[str]: A list of source frameworks for the specified target language.
    """
    data = MetadataService().get_source_frameworks(
        target_language=target_language.lower(),
        lang_config=request.state.language_config,
    )
    return data


@router.get(
    "/metadata/target_frameworks", tags=["Target Frameworks for Target Language"]
)
async def get_target_frameworks(request: Request, target_code_lang: str) -> List[str]:
    """
    Description:-
        Get Target Frameworks

    Param:
        request: Fast API Request Object
        target_code_lang: Target code language

    Return:
        Return a List of target code language

    Raise:
        HttpExceptionError: If error occur while handling request
    """
    data = MetadataService().get_metadata_target_frameworks(
        target_code_lang.lower(), request.state.language_config
    )
    return data


@router.get(
    "/metadata/accessible_features",
    tags=["Source Code Feature"],
)
async def get_metadata_accessible_features(
    request: Request,
) -> Dict[str, Dict[str, Any]]:
    """
    Description:-
        API to GET all the accessible feature.

    Param:
        request: Fast API Request Object

    Return:
        Dict[Dict[str, Any]]: A list of dict containing all accessible features.

    Raise:
        HttpExceptionError: if error occur while handling request
    """
    data = MetadataService().accessible_features(
        lang_config=request.state.language_config
    )
    return data


@router.get("/metadata/file_extension", tags=["Target Supported Extension"])
async def get_metadata_file_extension(
    request: Request,
    source_code_lang: str = Query(..., description="The source code language"),
    target_code_lang: str = Query(..., description="The target code language"),
    source_framework: str = Query(..., description="The source code framework"),
    target_framework: str = Query(..., description="The target code framework"),
) -> List[dict]:
    """
    Description:-
        API to GET all the target extention which belongs to "extension" these "extension"
        langauges target framework is not False.

    Param:-
        request: Fast API Request Object
        source_code_lang: Source code language.
        target_code_lang: Target code language.
        source_framework: Source code farmework.
        target_framework: Target code framework.

    Return:-
        List[dict]: A list of target language and frameworks for the specified extension and returns an empty list if not found.

    Raise:-
        HttpExceptionError: If error occur while handling request.
    """
    data = MetadataService().get_metadata_file_extension(
        source_code_lang=source_code_lang.lower(),
        source_framework=source_framework.lower(),
        target_code_lang=target_code_lang.lower(),
        target_framework=target_framework.lower(),
        lang_config=request.state.language_config,
    )
    return data


@router.get(
    "/metadata/ai_provider",
    tags=["Source Code Feature"],
)
async def get_metadata_ai_provider(
    request: Request,
) -> list[str]:
    """
    Description:-
        Api To Get All AI Provider.

    Param:
        request: Fast API Request Object

    Return:
        Dict[str,]: A List Of Str Containing All Ai Providers

    Raise:
        HttpExceptionError: if error occur while handling request
    """

    data = MetadataService().get_ai_provider(lang_config=request.state.language_config)
    return data
