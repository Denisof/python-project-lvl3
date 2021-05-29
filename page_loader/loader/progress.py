"""Provide progress bar decorator."""
from progress.spinner import Spinner

CHECK_BOX = '\u2705'


class CheckBox(Spinner):
    """[summary].

    Args:
        Spinner (Spinner): [description]
    """

    phases = (CHECK_BOX)


def download_bar(function):
    """[summary].

    Args:
        function ([type]): [description]

    Returns:
        function: [description]
    """
    def download_decorator(url: str) -> str:  # noqa:WPS430
        """[summary].

        Args:
            url (str): [description]

        Returns:
            str: [description]
        """
        check_box = CheckBox('Loading {0} '.format(url))
        down_load_result = function(url)
        check_box.next()  # noqa:B305
        check_box.finish()
        return down_load_result
    return download_decorator
