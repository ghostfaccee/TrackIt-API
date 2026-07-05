import sys
from pathlib import Path
from loguru import logger

logger.remove() # removing the old handler to set everything up yourself

log_dir = Path('logs')
log_dir.mkdir(exist_ok = True)

log_format = (
    '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | '
    '<level>{level: <8}</level> | '
    '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - '
    '<level>{message}</level>'
)

logger.add(
    sys.stdout,
    format = log_format,
    level = "DEBUG",
    colorize = True
)

__all__ = ["logger"]