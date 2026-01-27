import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request
import time
import os

app = FastAPI()

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, "app.log")

handler = RotatingFileHandler(
    log_file,
    maxBytes=5 * 1024 * 1024,
    backupCount=3
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

handler.setFormatter(formatter)
handler.setLevel(logging.INFO)


root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)
root_logger.addHandler(console_handler)

logger = logging.getLogger("app")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
    except Exception:
        logger.error("Unhandled exception", exc_info=True)
        raise

    duration = round(time.time() - start_time, 3)

    logger.info(
        "%s %s | %s | %sms",
        request.method,
        request.url.path,
        response.status_code,
        duration
    )

    return response


@app.get("/health")
async def health():
    logger.info("Health check endpoint hit")
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI app starting")
    
    
    
    
import uvicorn
from app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=6969)