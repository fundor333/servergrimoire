import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="DEBUG")
