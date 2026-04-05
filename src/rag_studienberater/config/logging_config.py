# Imports
import logging
import sys


def setup_logging(level: str = 'INFO') -> None:
    logger = logging.getLogger()

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(getattr(logging, level.upper()))

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(levelname)s]: %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logging.getLogger('qdrant_client').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('pdfminer').setLevel(logging.WARNING)
