import logging
import sys
from typing import Optional

def setup_logging(level: Optional[str] = None) -> None:
    """Configure logging for the application."""
    log_level = getattr(logging, level or "INFO")
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    root_logger.addHandler(console)
    
    # File handler
    file_handler = logging.FileHandler("faa_sc_filler.log")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
