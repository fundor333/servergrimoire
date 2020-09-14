from .configmanager import ConfigManager
from .print_stuff import PrintColor, StrColor


class Plugin(object):
    """
    Abstract base class for commands that process directives.
    """

    def __init__(self, config: ConfigManager):
        self.l = PrintColor(config)
        self.str = StrColor(config)

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

    def stats(self, directive: str, data: dict) -> ({str: int}, {str: str}):
        """
        Return the stats for the directive
        """
        raise NotImplementedError

    def info(self, directive: str, data: dict):
        """
        Return info of the directive
        """
        return data.get(directive, dict())
