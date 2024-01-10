
from fastapi import Request, HTTPException

import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    handlers=[
        logging.StreamHandler(stream=sys.stdout) 
    ],
)

async def logging_middleware(request: Request, call_next):
    logging.info(f"Received request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logging.info(f"Completed request: {request.method} {request.url} - Status Code: {response.status_code}")
        return response
    except HTTPException as e:
        logging.error(f"Error in request: {request.method} {request.url} - Status Code: {e.status_code}")
        raise e

class LoggingService:
        
    @staticmethod
    async def info(msg):
        logging.info(msg) 

    @staticmethod
    async def error(msg):
        logging.error(msg) 

    @staticmethod
    async def debug(msg):
        logging.debug(msg) 