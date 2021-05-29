"""Page loader."""
import logging
from urllib.parse import urlparse

import page_loader.content.parser as content_parser
import page_loader.loader.resource_saver as resource_saver
import page_loader.loader.resourse_loader as resourse_loader
from page_loader.path.resolver import Resolver


def download(page_url: str, dist_dir: str) -> str:
    """Download specified page in destination folder and returns a path to the file.

    Args:
        page_url (str): [description]
        dist_dir (str): [description]

    Raises:
        ValueError: [description]

    Returns:
        str: [description]
    """
    logger = logging.getLogger(__name__)
    if not resource_saver.dir_exists(dist_dir):
        raise ValueError('Dir {0} does not exist'.format(dist_dir))
    logger.info('Page {0} loading is started.'.format(page_url))
    page_content = resourse_loader.download(page_url)
    url_compoents = urlparse(page_url)
    path_resolver = Resolver(url_compoents.netloc, dist_dir)
    file_path = path_resolver.get_full_document_path(url_compoents.path)
    page_content = content_parser.parse(
        page_content,
        path_resolver,
        url_compoents,
    )
    if not page_url.endswith('.html'):
        file_path = '{0}.html'.format(file_path)
    resource_saver.save(file_path, page_content)
    return file_path
