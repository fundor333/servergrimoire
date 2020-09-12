from tabulate import tabulate

class ColorClass:
    def __init__(self, palet=None):
        if palet is None:
            palet = dict()
        self.info_color = palet.get("okblue", "\033[94m")
        self.debug_color = palet.get("okgreen", "\033[92m")
        self.warning_color = palet.get("warning", "\033[93m")
        self.fail_color = palet.get("fail", "\033[91m")
        self.end_color = palet.get("endc", "\033[0m")

    def info(self, message: str) -> str:
        raise NotImplementedError

    def debug(self, message: str) -> str:
        raise NotImplementedError

    def warning(self, message: str) -> str:
        raise NotImplementedError

    def fail(self, message: str) -> str:
        raise NotImplementedError

class StrColor(ColorClass):
    def __printer__(self, message: str, color: str = None) -> str:
        return f"{color}{message}{self.end_color}"

    def info(self, message: str) -> str:
        return self.__printer__(message, self.info_color)

    def debug(self, message: str) -> str:
        return self.__printer__(message, self.debug_color)

    def warning(self, message: str) -> str:
        return self.__printer__(message, self.warning_color)

    def fail(self, message: str) -> str:
        return self.__printer__(message, self.fail_color)


class PrintColor(ColorClass):
    def __init__(self, palet=None):
        super().__init__(palet)
        self.s = StrColor(palet)

    def info(self, message: str) -> str:
        return self.s.info(message)

    def debug(self, message: str) -> str:
        return self.s.debug(message)

    def warning(self, message: str) -> str:
        return self.s.warning(message)

    def fail(self, message: str) -> str:
        return self.s.fail(message)
