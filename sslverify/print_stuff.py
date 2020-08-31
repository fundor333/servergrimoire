from tabulate import tabulate


class PrintColor:
    def __init__(self, palet=None):
        if palet is None:
            palet = dict()
        self.okblue = palet.get("okblue", "\033[94m")
        self.okgreen = palet.get("okgreen", "\033[92m")
        self.warningc = palet.get("warning", "\033[93m")
        self.failc = palet.get("fail", "\033[91m")
        self.endc = palet.get("endc", "\033[0m")

    def __printer__(self, message: str, color: str = None) -> str:
        return f"{color}{message}{self.endc}"

    def info(self, message: str) -> str:
        return self.__printer__(message, self.okblue)

    def ok(self, message: str) -> str:
        return self.__printer__(message, self.okgreen)

    def warning(self, message: str) -> str:
        return self.__printer__(message, self.warningc)

    def fail(self, message: str) -> str:
        return self.__printer__(message, self.failc)


def print_t(input, headers: [str] = None):
    if headers:
        print(tabulate(input, headers, tablefmt="pipe"))
    else:
        print(tabulate(input, tablefmt="pipe"))
