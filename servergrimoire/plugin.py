from typing import Optional
from .print_stuff import PrintColor


class Plugin(object):
    """
    Abstract base class for commands that process directives.
    """

    def __init__(self):
        self.l = PrintColor()

    def can_handle(self, directive: str) -> bool:
        """
        Returns true if the Plugin can handle the directive.
        """
        raise NotImplementedError

    def execute(self, directive: str, data: dict) -> dict:
        """
        Executes the directive.
        """
        raise NotImplementedError

    def stats(self, directive: str, data: dict) -> {str: int}:
        """
        Return the stats for the directive
        """
        raise NotImplementedError

    @staticmethod
    def get_directives() -> [str]:
        """
        Return all the directive
        """
        raise NotImplementedError
