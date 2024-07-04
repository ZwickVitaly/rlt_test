from sys import stdout
from os import getenv

from loguru import logger


DEBUG = getenv("DEBUG", "0") == "1"
DOCKER = getenv("DOCKER_ENV", "0") == "1"

DB_HOST = "mongo" if DOCKER else "localhost"

MONGO_USER = getenv("MONGO_USER")
MONGO_PASSWORD = getenv("MONGO_PASSWORD")

logger.remove()
logger.add(
    "logs/debug_logs.log" if DEBUG else "logs/bot.log",
    rotation="00:00:00",
    level="DEBUG" if DEBUG else "INFO",
)
if DEBUG:
    logger.add(stdout, level="DEBUG")

BOT_TOKEN = getenv("BOT_TOKEN")

LOOKUP_DATE_UNITS = ("day", "month", "hour", "year")
