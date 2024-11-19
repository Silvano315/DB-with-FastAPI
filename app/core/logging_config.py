import logging
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path

class LogConfig:
    """
    Configuration class for application logging.
    
    This class sets up structured logging with different handlers
    for different severity levels.
    """
    
    def __init__(
        self,
        log_path: Optional[Path] = None,
        log_level: int = logging.INFO
    ) -> None:
        """
        Initialize logging configuration.
        
        Args:
            log_path: Optional custom path for log files
            log_level: The minimum logging level to record
        """
        self.log_path = log_path or Path("logs")
        self.log_level = log_level
        self.setup_logging()
    
    def setup_logging(self) -> None:
        """Configure logging handlers and formatters."""
        self.log_path.mkdir(exist_ok=True)
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler = logging.FileHandler(
            self.log_path / f"{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setFormatter(file_formatter)
        
        logging.root.setLevel(self.log_level)
        logging.root.addHandler(file_handler)