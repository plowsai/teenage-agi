"""
TeenAGI - A Python package for building AI agents capable of making multiple function calls in sequence.
"""

__version__ = "0.5.0"

from .core import TeenAGI, create_agent
from .function_registry import registry
from .logger import logger, configure_logger

__all__ = ["TeenAGI", "create_agent", "registry", "logger", "configure_logger", "__version__"] 