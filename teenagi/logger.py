"""
Logging functionality for TeenAGI.
"""

import logging
import os
import sys
from typing import Optional, Union, Dict, Any

# Define log levels
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# Create a custom formatter for the logs
class ColoredFormatter(logging.Formatter):
    """Formatter that adds color to the logs."""
    
    COLORS = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',   # Green
        'WARNING': '\033[33m', # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[41m\033[37m', # White on Red
        'RESET': '\033[0m'    # Reset
    }
    
    def format(self, record):
        """Format the log record with colors."""
        log_message = super().format(record)
        
        # Add color based on log level
        if record.levelname in self.COLORS:
            log_message = f"{self.COLORS[record.levelname]}{log_message}{self.COLORS['RESET']}"
        
        return log_message


class Logger:
    """Configurable logger for TeenAGI."""
    
    def __init__(self, name: str = "teenagi", level: str = "INFO", 
                 to_file: bool = False, log_file: str = "teenagi.log"):
        """
        Initialize the logger.
        
        Args:
            name: Name of the logger
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            to_file: Whether to log to a file
            log_file: Path to the log file
        """
        self.logger = logging.getLogger(name)
        self.set_level(level)
        
        # Clear any existing handlers
        self.logger.handlers = []
        
        # Always log to console
        self._add_console_handler()
        
        # Add file handler if requested
        if to_file:
            self._add_file_handler(log_file)
        
        # Prevent propagation to the root logger
        self.logger.propagate = False
    
    def set_level(self, level: str) -> None:
        """
        Set the logging level.
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        level = level.upper()
        if level not in LOG_LEVELS:
            level = "INFO"
        
        self.logger.setLevel(LOG_LEVELS[level])
    
    def _add_console_handler(self) -> None:
        """Add a console handler to the logger."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredFormatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(console_handler)
    
    def _add_file_handler(self, log_file: str) -> None:
        """
        Add a file handler to the logger.
        
        Args:
            log_file: Path to the log file
        """
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log a debug message."""
        self._log_with_context(self.logger.debug, message, **kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log an info message."""
        self._log_with_context(self.logger.info, message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log a warning message."""
        self._log_with_context(self.logger.warning, message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log an error message."""
        self._log_with_context(self.logger.error, message, **kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log a critical message."""
        self._log_with_context(self.logger.critical, message, **kwargs)
    
    def _log_with_context(self, log_func, message: str, **kwargs) -> None:
        """
        Log a message with optional context data.
        
        Args:
            log_func: The logging function to use
            message: The message to log
            **kwargs: Additional context data to include in the log
        """
        if kwargs:
            context = ' '.join([f"{k}={v}" for k, v in kwargs.items()])
            message = f"{message} [{context}]"
        
        log_func(message)


# Create a default logger
logger = Logger()

# Function to configure the logger
def configure_logger(name: str = "teenagi", level: str = "INFO", 
                     to_file: bool = False, log_file: str = "teenagi.log") -> Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Name of the logger
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        to_file: Whether to log to a file
        log_file: Path to the log file
        
    Returns:
        Configured logger instance
    """
    global logger
    logger = Logger(name=name, level=level, to_file=to_file, log_file=log_file)
    return logger 