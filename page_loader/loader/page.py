"""Page loader."""
import os
import re
from urllib.parse import urlparse

import requests

HTTP_RESPONSE_OK = 200
CHUNK_SIZE = 128


def download(page_url: str, dist_dir: str) -> str:
    """Download specified page in destination folder and returns a path to the file.

    Args:
        page_url (str): Page location.
        dist_dir (str): Destination derictory.

    Raises:
        ValueError: Error description

    Returns:
        str: Path to the downloaded file.
    """
    target_page = requests.get(page_url)
    if target_page.status_code != HTTP_RESPONSE_OK:
        raise ValueError('Target page {0} is not available '.format(page_url))
    file_path = get_target_file_name(page_url, dist_dir)
    try:
        with open(file_path, 'wb') as dest_file:
            for chunk in target_page.iter_content(chunk_size=CHUNK_SIZE):
                dest_file.write(chunk)
    except (IOError, PermissionError):
        raise ValueError('Can not write to {0}'.format(file_path))
    return file_path


def get_target_file_name(page_url: str, dist_dir: str) -> str:
    """Generate target file path.

    Args:
        page_url (str): Page location.
        dist_dir (str): Destination derictory.

    Returns:
        str: File path
    """
    url_components = urlparse(page_url)
    file_name = re.sub(
        r'[^0-9a-zA-Z]',
        '-',
        url_components.netloc + url_components.path,
    )
    return '{0}.html'.format(os.path.join(dist_dir, file_name))
