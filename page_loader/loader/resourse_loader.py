"""Resourse loader."""
import logging
from typing import Optional

import requests
from validators import url as urlvalidate
from validators.utils import ValidationFailure

from page_loader.loader.progress import download_bar

HTTP_RESPONSE_OK = 200

logger = logging.getLogger(__name__)


@download_bar
def download(page_url: str, stream: Optional[bool] = True) -> str:
    """Download specified resource.

    Args:
        page_url (str): [description]
        stream (Optional[bool], optional): [description]. Defaults to True.

    Raises:
        ValueError: [description]
        ValueError: [description]

    Returns:
        str: [description]
    """
    logger.info('Loading %s', page_url)
    try:
        urlvalidate(page_url)
    except ValidationFailure:
        logger.error('Url %s is not valid', page_url)
        raise ValueError('The url {0} is not valid '.format(page_url))
    target_resource = requests.get(page_url, stream=stream)
    if target_resource.status_code != HTTP_RESPONSE_OK:
        logger.error(
            'Got %s respone code is not valid',
            target_resource.status_code,
        )
        raise ValueError('Target page {0} is not available '.format(page_url))
    return target_resource.raw.data if stream else target_resource.text
