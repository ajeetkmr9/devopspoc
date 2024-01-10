from autogen import code_utils
from pydantic import BaseModel, create_model, Json
from fastapi import APIRouter, File, UploadFile, Depends, Request, FastAPI
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from hashlib import md5
from typing import Callable, Dict, List, Optional, Tuple, Union

from utils.log import logging_middleware

import inspect
import sys
import os
import pathlib
import re
import subprocess
import time

import logging

logger = logging.getLogger(__name__)

from autogen import oai

try:
    import docker
except ImportError:
    docker = None

CODE_BLOCK_PATTERN = r"```[ \t]*(\w+)?[ \t]*\r?\n(.*?)\r?\n[ \t]*```"
WORKING_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "extensions")
UNKNOWN = "unknown"
TIMEOUT_MSG = "Timeout"
DEFAULT_TIMEOUT = 600
WIN32 = sys.platform == "win32"
PATH_SEPARATOR = WIN32 and "\\" or "/"

name = "compiler"
system_message = """Your job is to compile the code given to you."""
human_input_mode = "ALWAYS"
terminate_message = "exitcode: 0 (execution succeeded) language: (['python'])"
terminate_message_java = "exitcode: 0 (execution succeeded)"

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

def execute_code(
    code: Optional[str] = None,
    timeout: Optional[int] = None,
    filename: Optional[str] = None,
    work_dir: Optional[str] = None,
    use_docker: Optional[Union[List[str], str, bool]] = None,
    lang: Optional[str] = "python",
) -> Tuple[int, str, str]:
    
    """Execute code in a docker container.
    This function is not tested on MacOS.

    Args:
        code (Optional, str): The code to execute.
            If None, the code from the file specified by filename will be executed.
            Either code or filename must be provided.
        timeout (Optional, int): The maximum execution time in seconds.
            If None, a default timeout will be used. The default timeout is 600 seconds. On Windows, the timeout is not enforced when use_docker=False.
        filename (Optional, str): The file name to save the code or where the code is stored when `code` is None.
            If None, a file with a randomly generated name will be created.
            The randomly generated file will be deleted after execution.
            The file name must be a relative path. Relative paths are relative to the working directory.
        work_dir (Optional, str): The working directory for the code execution.
            If None, a default working directory will be used.
            The default working directory is the "extensions" directory under
            "path_to_autogen".
        use_docker (Optional, list, str or bool): The docker image to use for code execution.
            If a list or a str of image name(s) is provided, the code will be executed in a docker container
            with the first image successfully pulled.
            If None, False or empty, the code will be executed in the current environment.
            Default is None, which will be converted into an empty list when docker package is available.
            Expected behaviour:
                - If `use_docker` is explicitly set to True and the docker package is available, the code will run in a Docker container.
                - If `use_docker` is explicitly set to True but the Docker package is missing, an error will be raised.
                - If `use_docker` is not set (i.e., left default to None) and the Docker package is not available, a warning will be displayed, but the code will run natively.
            If the code is executed in the current environment,
            the code must be trusted.
        lang (Optional, str): The language of the code. Default is "python".

    Returns:
        int: 0 if the code executes successfully.
        str: The error message if the code fails to execute; the stdout otherwise.
        image: The docker image name after container run when docker is used.
    """
    if all((code is None, filename is None)):
        error_msg = f"Either {code=} or {filename=} must be provided."
        logger.error(error_msg)
        raise AssertionError(error_msg)

    # Warn if use_docker was unspecified (or None), and cannot be provided (the default).
    # In this case the current behavior is to fall back to run natively, but this behavior
    # is subject to change.
    if use_docker is None:
        if docker is None:
            use_docker = False
            logger.warning(
                "execute_code was called without specifying a value for use_docker. Since the python docker package is not available, code will be run natively. Note: this fallback behavior is subject to change"
            )
        else:
            # Default to true
            use_docker = True

    timeout = timeout or DEFAULT_TIMEOUT
    original_filename = filename
    if WIN32 and lang in ["sh", "shell"] and (not use_docker):
        lang = "ps1"
    if filename is None:
        code_hash = md5(code.encode()).hexdigest()
        # create a file with a automatically generated name
        filename = f"tmp_code_{code_hash}.{'py' if lang.startswith('python') else lang}"
    if work_dir is None:
        work_dir = WORKING_DIR
    filepath = os.path.join(work_dir, filename)
    file_dir = os.path.dirname(filepath)
    os.makedirs(file_dir, exist_ok=True)
    if code is not None:
        with open(filepath, "w", encoding="utf-8") as fout:
            fout.write(code)
    # check if already running in a docker container
    in_docker_container = os.path.exists("/.dockerenv")
    if not use_docker or in_docker_container:
        # already running in a docker container
        """
        Ashok: Update.
        """
        if lang.lower() == "cobol":
            cmd = [
                _cmd(lang),
                f".\\{filename}" if WIN32 else filename,
            ]
        else:
            cmd = [
                sys.executable if lang.startswith("python") else _cmd(lang),
                f".\\{filename}" if WIN32 else filename,
            ]
        if WIN32:
            logger.warning("SIGALRM is not supported on Windows. No timeout will be enforced.")
            result = subprocess.run(
                cmd,
                cwd=work_dir,
                capture_output=True,
                text=True,
            )
        else:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    subprocess.run,
                    cmd,
                    cwd=work_dir,
                    capture_output=True,
                    text=True,
                )
                try:
                    result = future.result(timeout=timeout)
                except TimeoutError:
                    if original_filename is None:
                        os.remove(filepath)
                    return 1, TIMEOUT_MSG, None
        if original_filename is None:
            os.remove(filepath)
        if result.returncode:
            logs = result.stderr
            if original_filename is None:
                abs_path = str(pathlib.Path(filepath).absolute())
                logs = logs.replace(str(abs_path), "").replace(filename, "")
            else:
                abs_path = str(pathlib.Path(work_dir).absolute()) + PATH_SEPARATOR
                logs = logs.replace(str(abs_path), "")
        else:
            logs = result.stdout
        return result.returncode, logs, None

    # create a docker client
    client = docker.from_env()
    image_list = (
        ["python:3-alpine", "python:3", "python:3-windowsservercore"]
        if use_docker is True
        else [use_docker]
        if isinstance(use_docker, str)
        else use_docker
    )
    for image in image_list:
        # check if the image exists
        try:
            client.images.get(image)
            break
        except docker.errors.ImageNotFound:
            # pull the image
            print("Pulling image", image)
            try:
                client.images.pull(image)
                break
            except docker.errors.DockerException:
                print("Failed to pull image", image)
    # get a randomized str based on current time to wrap the exit code
    exit_code_str = f"exitcode{time.time()}"
    abs_path = pathlib.Path(work_dir).absolute()
    cmd = [
        "sh",
        "-c",
        f"{_cmd(lang)} {filename}; exit_code=$?; echo -n {exit_code_str}; echo -n $exit_code; echo {exit_code_str}",
    ]
    # create a docker container
    container = client.containers.run(
        image,
        command=cmd,
        working_dir="/workspace",
        detach=True,
        # get absolute path to the working directory
        volumes={abs_path: {"bind": "/workspace", "mode": "rw"}},
    )
    start_time = time.time()
    while container.status != "exited" and time.time() - start_time < timeout:
        # Reload the container object
        container.reload()
    if container.status != "exited":
        container.stop()
        container.remove()
        if original_filename is None:
            os.remove(filepath)
        return 1, TIMEOUT_MSG, image
    # get the container logs
    logs = container.logs().decode("utf-8").rstrip()
    # commit the image
    tag = filename.replace("/", "")
    container.commit(repository="python", tag=tag)
    # remove the container
    container.remove()
    # check if the code executed successfully
    exit_code = container.attrs["State"]["ExitCode"]
    if exit_code == 0:
        # extract the exit code from the logs
        pattern = re.compile(f"{exit_code_str}(\\d+){exit_code_str}")
        match = pattern.search(logs)
        exit_code = 1 if match is None else int(match.group(1))
        # remove the exit code from the logs
        logs = logs if match is None else pattern.sub("", logs)

    if original_filename is None:
        os.remove(filepath)
    if exit_code:
        logs = logs.replace(f"/workspace/{filename if original_filename is None else ''}", "")
    # return the exit code, logs and image
    return exit_code, logs, f"python:{tag}"

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
    if lang in ["cobol"]:
        return "cobc"
    raise NotImplementedError(f"{lang} not recognized in code execution")

code_utils._cmd = _cmd
code_utils.execute_code = execute_code

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
Sample Code
Compliation Passed

{
    "source": {
        "language": "cobol",
        "code_language": "string",
        "framework": "string",
        "source_code": "IDENTIFICATION DIVISION. PROGRAM-ID. HelloWorld. PROCEDURE DIVISION. DISPLAY 'Hello, World!'. STOP RUN."
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
            "content": f"""```cobol
       * filename: Sample.cbl
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
        "result": result
    }

    logger.info(f'Returning from API method: {inspect.currentframe().f_code.co_name}')

    return response
