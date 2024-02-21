from autogen import code_utils
from pydantic import BaseModel, create_model, Json
from fastapi import APIRouter, File, UploadFile, Depends, Request, FastAPI
import inspect

from hashlib import md5
from typing import Dict, List
from utils.log import logging_middleware

import logging

logger = logging.getLogger(__name__)

from autogen import oai

try:
    import docker
except ImportError:
    docker = None

class Source(BaseModel):
    language: str
    code_language: str
    framework: str
    source_code: str

class SourceFile(BaseModel):
    language: str
    code_language: str
    framework: str

class Target(BaseModel):
    language: str
    code_language: str
    framework: str

class TargetResponse(BaseModel):
    language: str
    code_language: str
    framework: str
    source_code: str

class LLMProvider(BaseModel):
    name: str
    model: str

class ConvertCodeRequest(BaseModel):
    source: Source
    target: Target
    llm_provider: LLMProvider
    compile: bool = True

class ConvertCodeResponse(BaseModel):
    source: Source
    target: TargetResponse
    llm_provider: LLMProvider
    compile: bool 
    result: str

class ConvertFileRequest(BaseModel):
    source: SourceFile
    target: Target
    llm_provider: LLMProvider
    compile: bool = True

class ConvertFileResponse(BaseModel):
    source: SourceFile
    target: TargetResponse
    llm_provider: LLMProvider
    compile: bool


name = "compiler"
system_message = """Your job is to compile the code given to you."""
human_input_mode = "ALWAYS"
terminate_message = "exitcode: 0 (execution succeeded) language: (['python'])"
terminate_message_java = "exitcode: 0 (execution succeeded)"

"""
    Override Python pyautogen
"""
def _cmd(lang):
    if lang.startswith("python") or lang in ["bash", "sh", "powershell"]:
        return lang
    if lang in ["shell"]:
        return "sh"
    if lang in ["ps1"]:
        return "powershell"
    """
        Ashok
    """
    if lang in ["java"]:
        return "javac"
    raise NotImplementedError(f"{lang} not recognized in code execution")

code_utils._cmd = _cmd

from autogen_interface.autogen.agentchat.user_proxy_agent import UserProxyAgent

# Terminate function. 
def termination_function(content):
    print("termination_func()")
    print("Requirement: ", terminate_message_java)
    have_content = content.get("content", None) is not None
    if have_content:
        print("Content:     ", content["content"])
        content = content["content"]
        
        if terminate_message_java in content: # TODO
            print("---------- Completed  my job -----------")
            return True
        else:
            print("---------- Reworking  -----------")
    return False  

# Define Application
def get_application() -> FastAPI:
    application = FastAPI(
        title="Fast API",
        description="Fast API for GEN AI",
        version="0.0.1"
    )
    return application

# Initialize Application
app = get_application()

app.middleware('http')(logging_middleware)


"""
Sample Request: Compile Pass
{
    "source": {
        "language": "java",
        "code_language": "string",
        "framework": "string",
        "source_code": "class HelloWorld{public static void main(String[] args){System.out.println(\"Hello, World!\");}}"
    },
    "target": {
        "language": "string",
        "code_language": "string",
        "framework": "string"
    },
    "llm_provider": {
        "name": "string",
        "model": "string"
    },
    "compile": true
}

Sample Request: Compile Failed
{
    "source": {
        "language": "java",
        "code_language": "string",
        "framework": "string",
        "source_code": "public class MainClass { public static void main(String[] args) { HelperClass helper = new HelperClass(); helper.find_my_string(\"Hello from MainClass!\"); } }\n"
    },
    "target": {
        "language": "string",
        "code_language": "string",
        "framework": "string"
    },
    "llm_provider": {
        "name": "string",
        "model": "string"
    },
    "compile": true
}
    """

@app.post("/v1/compile/", 
                tags=["Convert Code"], 
                response_model=ConvertCodeResponse
            )
async def convert_code(request_params: ConvertCodeRequest, request = Request) -> dict:
    
    logger.info(f'Entring API method: {inspect.currentframe().f_code.co_name}')

    autogen_user_proxy = UserProxyAgent(
                            name=name,
                            system_message=system_message,
                            human_input_mode=human_input_mode,
                            is_termination_msg=termination_function,
                            code_execution_config={"use_docker": False}
                        )

    
    code = [
        {
            "content": f"""```java
// filename: MainClass.java
{request_params.source.source_code}
```"""
        },
    ]

    logger.info(f"------code-------- {code}")
    result = autogen_user_proxy.generate_code_execution_reply(code)
    logger.info(f"------result-------- {result}")

    response = {
        "source": {
            "language": request_params.source.language,
            "code_language": request_params.source.code_language,
            "framework": request_params.source.framework,
            "source_code": request_params.source.source_code,
        },
        "target": {
            "language": request_params.target.language,
            "code_language": request_params.target.code_language,
            "framework": request_params.target.framework,
            "source_code": request_params.source.source_code,
        },
        "llm_provider": {
            "name": request_params.llm_provider.name,
            "model": request_params.llm_provider.model,
        },
        "compile": request_params.compile,
        "result": result[1]
    }

    logger.info(f'Returning from API method: {inspect.currentframe().f_code.co_name}')

    return response
