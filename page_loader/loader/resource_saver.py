"""Save content."""
import logging
import os

logger = logging.getLogger(__name__)


def save(file_path: str, file_content: str):
    """[summary].

    Args:
        file_path (str): [description]
        file_content (str): [description]

    Raises:
        ValueError: [description]
    """
    logger.info('Writing content to a file %s', file_path)
    try:
        with open(file_path, 'w') as dest_file:
            dest_file.write(file_content)
    except (IOError, PermissionError) as error:
        logger.error('Could not save a file %s', error)
        raise ValueError('Can not write to {0}'.format(file_path))


def prepare_dir(path: str):
    """[summary].

    Args:
        path (str): [description]

    Raises:
        ValueError: [description]
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except (IOError, PermissionError) as error:
            logger.error(
                'Could not create a directory %s error: %s',
                path,
                error,
            )
            raise ValueError('Can not create a directory {0}'.format(path))


def dir_exists(path: str) -> bool:
    """[summary].

    Args:
        path (str): [description]

    Returns:
        bool: [description]
    """
    return os.path.exists(path)
