import logging
import sys
from app.core.config import settings

# Define log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging() -> logging.Logger:
    log_level = logging.DEBUG if settings.ENVIRONMENT == "development" else logging.INFO

    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(settings.PROJECT_NAME)
    logger.setLevel(log_level)
    return logger


logger = setup_logging()
