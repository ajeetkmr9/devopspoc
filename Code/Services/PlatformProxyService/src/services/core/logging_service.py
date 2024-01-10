
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


class LoggingService:
        
    @staticmethod
    async def info(msg):
        logging.info(msg) 

    @staticmethod
    async def error(msg):
        logging.error(msg) 

    @staticmethod
    async def debug(msg, modified_msg=None):
        if modified_msg:
            logging.debug(modified_msg)
        else:
            logging.debug(msg)
