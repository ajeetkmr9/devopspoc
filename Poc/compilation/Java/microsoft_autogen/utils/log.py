from fastapi import Request, HTTPException
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    handlers=[
        logging.StreamHandler() 
    ],
)

# Custom logging middleware
async def logging_middleware(request: Request, call_next):
    logging.info(f"Received request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        # Log information about the response
        logging.info(f"Completed request: {request.method} {request.url} - Status Code: {response.status_code}")
        return response
    except HTTPException as e:
        # Log information about errors
        logging.error(f"Error in request: {request.method} {request.url} - Status Code: {e.status_code}")
        raise e