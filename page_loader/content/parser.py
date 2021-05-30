"""Process html document."""
from itertools import chain
from typing import Iterator
from urllib.parse import ParseResult, urlparse, urlunparse

from bs4 import BeautifulSoup

import page_loader.loader.resource_saver as resource_saver
import page_loader.loader.resourse_loader as resourse_loader
from page_loader.path.resolver import Resolver

SRC_ATTRIBUTE = 'src'
HREF_ATTRIBUTE = 'href'
BOM = '\xef\xbb\xbf'


def parse(
    document: str,
    path_resolver: Resolver,
    page_compoents: ParseResult,
) -> str:
    """[summary].

    Args:
        document (str): [description]
        path_resolver (Resolver): [description]
        page_compoents (ParseResult): [description]

    Returns:
        str: [description]
    """
    document = BeautifulSoup(document, 'html.parser')
    resource_saver.prepare_dir(path_resolver.get_asset_folder_path())
    for link_attr, elem in iter(get_assets(document)):
        link_components = urlparse(elem.get(link_attr))
        if not is_local(page_compoents, link_components):
            continue
        path_dic = path_resolver.get_asset_path(
            page_compoents.netloc + link_components.path,
        )
        load_asset(
            get_asset_url(page_compoents, link_components),
            path_dic.get('file_path'),
        )
        elem[link_attr] = path_dic.get('doc_path')
    return document.prettify(formatter='html5')


def is_local(page_compoents: ParseResult, url_components: ParseResult) -> bool:
    """[summary].

    Args:
        page_compoents (ParseResult): [description]
        url_components (ParseResult): [description]

    Returns:
        bool: [description]
    """
    if not url_components.netloc:
        return True
    return url_components.netloc == page_compoents.netloc


def get_assets(document: BeautifulSoup) -> Iterator:
    """[summary].

    Args:
        document (BeautifulSoup): [description]

    Returns:
        Iterator: [description]
    """
    img_elems = document.find_all('img')
    script_elems = document.select('script[src]')
    link_elems = document.select('link')
    return chain(
        zip(
            len(img_elems) * (SRC_ATTRIBUTE,),
            img_elems,
        ),
        zip(
            len(script_elems) * (SRC_ATTRIBUTE,),
            script_elems,
        ),
        zip(
            len(link_elems) * (HREF_ATTRIBUTE,),
            link_elems,
        ),
    )


def get_asset_url(
    page_compoents: ParseResult,
    url_components: ParseResult,
) -> str:
    """[summary].

    Args:
        page_compoents (ParseResult): [description]
        url_components (ParseResult): [description]

    Returns:
        str: [description]
    """
    parsed = page_compoents._replace(  # noqa:WPS437
        path=url_components.path,
        params=url_components.params,
        query=url_components.query,
        fragment=url_components.fragment,
    )
    return urlunparse(parsed)


def load_asset(url: str, file_path: str) -> None:
    """[summary].

    Args:
        url (str): [description]
        file_path (str): [description]
    """
    asset_content = resourse_loader.download(
        url,
    )
    resource_saver.save(file_path, BOM + asset_content)
