import time
import logging
from fastapi import FastAPI, Request

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("app_logger")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    formatted_time = f"{process_time:.4f}s"

    logger.info(
        f"PATH: {request.url.path} | "
        f"METHOD: {request.method} | "
        f"STATUS: {response.status_code} | "
        f"TIME: {formatted_time}"
    )

    return response

@app.get('/')
def greet():
    return "hello"

@app.get('/books')
def books():
    return "books will show here"

