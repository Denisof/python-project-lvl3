"""Resolve paths."""
import os
import re
from typing import Optional


class Resolver(object):
    """[summary].

    Returns:
        [type]: [description]
    """

    _files_postfix = '_files'
    _base_path = None
    _hyphen = '-'

    def __init__(self, netloc: str, path: str, dest_dir: str) -> None:
        """[summary].

        Args:
            netloc (str): [description]
            path (str): [description]
            dest_dir (str): [description]
        """
        self.netloc = netloc
        self.path = path
        self.dest_dir = dest_dir

    def get_full_document_path(self, path) -> str:
        """[summary].

        Args:
            path (str): [description]

        Returns:
            str: [description]
        """
        file_name = self._hyphenize(
            self.netloc + path.rstrip(os.path.sep),
        )
        return os.path.join(self.dest_dir, file_name)

    def get_asset_path(self, path: str) -> dict:
        """[summary].

        Args:
            path (str): [description]

        Returns:
            dict: [description]
        """
        split_path = os.path.split(path)
        file_name = '{0}{1}{2}'.format(
            self._hyphenize(split_path[0].lstrip(os.path.sep)),
            self._hyphen,
            split_path[1],
        )
        root_ext = os.path.splitext(file_name)
        if not root_ext[1]:
            file_name = '{0}.html'.format(root_ext[0])
        return {
            'file_path': os.path.join(self.get_asset_folder_path(), file_name),
            'doc_path': os.path.join(
                self.get_asset_folder_path(False),
                file_name,
            ),
        }

    def get_asset_folder_path(self, full: Optional[bool] = True) -> str:
        """[summary].

        Args:
            full (Optional[bool], optional): [description]. Defaults to True.

        Returns:
            str: [description]
        """
        asset_dir = '{0}{1}'.format(
            self._hyphenize(self.netloc + self.path.rstrip(os.path.sep)),
            self._files_postfix,
        )
        if not full:
            return asset_dir
        return os.path.join(self.dest_dir, asset_dir)

    def _hyphenize(self, target: str) -> str:
        """[summary].

        Args:
            target (str): [description]

        Returns:
            str: [description]
        """
        return re.sub(
            r'[^0-9a-zA-Z]',
            self._hyphen,
            target,
        )
