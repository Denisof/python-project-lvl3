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
    def download_decorator(*args, **kwargs) -> str:  # noqa:WPS430
        """[summary].

        Args:
            args (str): [description]
            kwargs (str): [description]

        Returns:
            str: [description]
        """
        check_box = CheckBox('Loading {0} '.format(args[0]))
        down_load_result = function(*args, **kwargs)
        check_box.next()  # noqa:B305
        check_box.finish()
        return down_load_result
    return download_decorator
