import json
import os
from pathlib import Path


class ConfigManager:
    def __init__(self, path):
        from servergrimoire.print_stuff import PrintColor
        self.config = {}
        if path is None:
            path = Path.home() / ".servergrimoire_config"
        self.path = path

        if not os.path.exists(path):
            self.__create_default__()
        else:
            with open(path) as data_file:
                self.config = json.load(data_file)
        self.__preset__()

        self.__write_config__()
        self.l = PrintColor(self)

    def __preset__(self):
        from servergrimoire.print_stuff import PrintColor
        l = PrintColor(self)
        l.debug(self.data_path)
        self.config["data_path"] = f'{self.config["data_path"]}'
        l.debug(self.colors)
        l.debug(self.logger_level)

    def __write_config__(self):
        with open(Path(self.path), "w") as outfile:
            self.__preset__()
            self.config["data_path"] = f'{self.config["data_path"]}'
            json.dump(self.config, outfile)

    def __create_default__(self) -> dict:
        self.__write_config__()
        return self.config

    @property
    def data_path(self):
        return self.config["data_path"]

    @data_path.setter
    def data_path(self, var):
        self.config["data_path"] = var

    @data_path.getter
    def data_path(self):
        if self.config.get("data_path", None) is None:
            self.config["data_path"] = Path.home() / ".servergrimoire_data"
        return self.config["data_path"]

    @property
    def colors(self):
        return self.config['colors']

    @colors.setter
    def colors(self, var: dict):
        if self.config.get("colors", None) is None:
            self.config["colors"] = {}
        self.config["colors"]["info_colo"] = var.get("info_colo", "\033[94m")
        self.config["colors"]["debug_color"] = var.get("debug_color", "\033[92m")
        self.config["colors"]["warning_color"] = var.get("warning_color", "\033[93m")
        self.config["colors"]["warning_color"] = var.get("fail_color", "\033[91m")
        self.config["colors"]["end_color"] = var.get("end_color", "\033[0m")
        self.config["colors"] = var

    @colors.getter
    def colors(self):
        var = self.config.get("colors", dict())
        if self.config.get("colors", None) is None:
            self.config["colors"] = {}
        self.config["colors"]["info_colo"] = var.get("info_colo", "\033[94m")
        self.config["colors"]["debug_color"] = var.get("debug_color", "\033[92m")
        self.config["colors"]["warning_color"] = var.get("warning_color", "\033[93m")
        self.config["colors"]["warning_color"] = var.get("fail_color", "\033[91m")
        self.config["colors"]["end_color"] = var.get("end_color", "\033[0m")
        return self.config["colors"]


    @property
    def logger_level(self):
        return self.config["logger_level"]

    @logger_level.setter
    def logger_level(self, var):
        self.config["logger_level"] = var

    @logger_level.getter
    def logger_level(self):
        if self.config.get("logger_level", None) is None:
            self.config["logger_level"] = "ERROR"
        return self.config["logger_level"]
