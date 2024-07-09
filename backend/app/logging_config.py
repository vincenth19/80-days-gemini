import sys
import os
from loguru import logger

os.makedirs('logs', exist_ok=True)

logger.remove(0)
logger.add(
    sys.stdout,
    format="{time:MMMM D, YYYY > HH:mm:ss!UTC} | {level} | {message}",
    serialize=True,
)
logger.info("Incoming API request: GET /api/users/123")