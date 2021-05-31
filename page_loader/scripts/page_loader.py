"""Page-loader entry point."""

import argparse
import logging
import sys

from page_loader.loader.page import download

logger = logging.getLogger(__name__)


def main():
    """Run entry function."""
    parser = argparse.ArgumentParser(
        prog='page-loader',
        description='Page loader.',
    )
    parser.add_argument('page_url')
    parser.add_argument('dist_dir')
    args = parser.parse_args()
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(0)
        return
    try:
        output_file = download(args.page_url, args.dist_dir)
    except ValueError as error:
        logger.critical(error)
        sys.exit(1)
    print(output_file)
    sys.exit(0)


if __name__ == '__main__':
    main()
