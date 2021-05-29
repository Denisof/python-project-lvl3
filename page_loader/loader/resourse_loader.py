"""Resourse loader."""
import logging

import requests
from validators import url as urlvalidate
from validators.utils import ValidationFailure

from page_loader.loader.progress import download_bar

HTTP_RESPONSE_OK = 200

logger = logging.getLogger(__name__)


@download_bar
def download(page_url: str) -> str:
    """Download specified resource.

    Args:
        page_url (str): Page location.

    Raises:
        ValueError: Error description

    Returns:
        str: Content.
    """
    logger.info('Loading %s', page_url)
    try:
        urlvalidate(page_url)
    except ValidationFailure:
        logger.error('Url %s is not valid', page_url)
        raise ValueError('The url {0} is not valid '.format(page_url))
    target_resource = requests.get(page_url)
    if target_resource.status_code != HTTP_RESPONSE_OK:
        logger.error(
            'Got %s respone code is not valid',
            target_resource.status_code,
        )
        raise ValueError('Target page {0} is not available '.format(page_url))
    return target_resource.text
