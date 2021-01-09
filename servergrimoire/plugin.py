from typing import List
import logging
from rich.logging import RichHandler


class Plugin(object):
    """
    Abstract base class for commands that process directives.
    """

    def __init__(self):

        FORMAT = "%(message)s"
        logging.basicConfig(
            level="NOTSET",
            format=FORMAT,
            datefmt="[%X]",
            handlers=[RichHandler()],
        )

        self.logger = logging.getLogger("rich")

    @staticmethod
    def get_directives() -> List[str]:
        """
        Returns the directives.
        """
        raise NotImplementedError

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

    def stats(self, directive: str, data: dict) -> List[dict]:
        """
        Return the stats for the directive
        """
        raise NotImplementedError

    def info(self, directive: str, data: dict):
        """
        Return info of the directive
        """
        return data.get(directive, dict())
