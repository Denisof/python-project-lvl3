"""Page-loader entry point."""

import argparse
import sys

from page_loader.loader.page import download


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
        output_file = download(args.page_url, args.dist_dir)
    except ValueError as error:
        print(error)
        sys.exit(0)
    print(output_file)


if __name__ == '__main__':
    main()
