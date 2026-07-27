import logging
import os

LOG_DIRECTORY = "logs"

os.makedirs(LOG_DIRECTORY, exist_ok=True)

logger = logging.getLogger("AIResearchAssistant")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler = logging.FileHandler(
    os.path.join(LOG_DIRECTORY, "app.log"),
    encoding="utf-8",
)

console_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logger.propagate = False