import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logging(level: Optional[str] = None) -> None:
    """Configure logging for the application."""
    log_level = getattr(logging, level or "INFO")

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root_logger.addHandler(console)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        "faa_sc_filler.log", maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
