import logging
from typing import List, Tuple

from rich.console import Console
from rich.logging import RichHandler
from rich.markdown import Markdown


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

    def stats(
        self, directive: str, data: dict
    ) -> Tuple[List[List], List[List]]:
        """
        Return the stats for the directive
        """
        raise NotImplementedError

    def get_markdown(self):
        """
        Return info text as Markdown
        """
        raise NotImplementedError

    def info(self):
        """
        Return info of the directive
        """
        console = Console()
        md = Markdown(self.get_markdown())
        console.print(md)

    def header_stats(self) -> List[str]:
        raise NotImplementedError

    def header_error(self) -> List[str]:
        raise NotImplementedError

    def title_stats(self) -> str:
        raise NotImplementedError

    def title_error(self) -> str:
        raise NotImplementedError
