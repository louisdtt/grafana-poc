from fastapi import FastAPI, Request
import logging
import random
import time
from pythonjsonlogger import jsonlogger

# Initialize FastAPI app
app = FastAPI()

# Configure logging in JSON format
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()

# Define JSON log format fields as needed
json_formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s %(status_code)d %(request_path)s"
)

logHandler.setFormatter(json_formatter)
logger.addHandler(logHandler)


# Middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Log the request details in JSON
    logger.info(
        "Request processed",
        extra={
            "request_method": request.method,
            "request_path": request.url.path,
            "process_time": round(process_time, 2),
            "status_code": response.status_code,
        },
    )
    return response


@app.get("/")
def get_random_number():
    """
    Generate and return a random number between 1 and 100.
    """
    random_number = random.randint(1, 100)
    return {"number": random_number}

@app.get("/login")
def login():
    """
    Simulate a login request.
    """
    return {"message": "Login successful"}
