import json
import os
import sys
from pathlib import Path

from loguru import logger


class ConfigManager:
    def __init__(self, path):
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

    def __preset__(self):
        logger.remove()
        logger.add(sys.stderr, level=self.logger_level)
        logger.debug(f"Data path {self.data_path}")
        self.config["data_path"] = f'{self.config["data_path"]}'
        logger.debug(f"Logger level is {self.logger_level}")

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
