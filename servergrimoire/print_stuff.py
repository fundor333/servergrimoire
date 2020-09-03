from tabulate import tabulate


class PrintColor:
    def __init__(self, palet=None):
        if palet is None:
            palet = dict()
        self.info_color = palet.get("okblue", "\033[94m")
        self.debug_color = palet.get("okgreen", "\033[92m")
        self.warning_color = palet.get("warning", "\033[93m")
        self.fail_color = palet.get("fail", "\033[91m")
        self.end_color = palet.get("endc", "\033[0m")

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


def print_t(input, headers: [str] = None):
    if headers:
        print(tabulate(input, headers, tablefmt="pipe"))
    else:
        print(tabulate(input, tablefmt="pipe"))
