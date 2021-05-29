"""init file."""
import logging
import os
import tempfile

from page_loader.loader.page import download

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
MAIN_LOG_FILE = 'page_loader.log'
log_file_path = os.path.join(tempfile.gettempdir(), MAIN_LOG_FILE)
formatter = logging.Formatter(
    fmt='%(asctime)s %(levelname)s %(message)s',  # noqa:WPS323
    datefmt='%m/%d/%Y %I:%M:%S %p',  # noqa:WPS323
)
file_handler = logging.FileHandler(filename=log_file_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.CRITICAL)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
__all__ = ['download']
