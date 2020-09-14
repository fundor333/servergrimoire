from loguru import logger


class Plugin(object):
    """
    Abstract base class for commands that process directives.
    """

    def __init__(self):
        self.l = logger.bind(task=type(self).__name__)

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
