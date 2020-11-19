import json
import os
import errno
import sys
from pathlib import Path

from loguru import logger


class ConfigManager:
    def __init__(self, path):
        self.config = {}
        if path is None:
            self.path = Path.home() / ".servergrimoire/config"
        else:
            self.path = path

        if not os.path.exists(self.path):
            if not os.path.exists(os.path.dirname(self.path)):
                try:
                    os.makedirs(os.path.dirname(self.path))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            self.__create_default__()
        else:
            with open(self.path) as data_file:
                self.config = json.load(data_file)
        self.__preset__()

        self.__write_config__()

    def __preset__(self):
        logger.remove()
        logger.add(sys.stderr, level="ERROR")
        logger.add(sys.stdout, level=self.logger_level)
        logger.debug(f"Data path {self.data_path}")
        logger.debug(f"Logger level is {self.logger_level}")

        self.config["data_path"] = str(self.data_path)
        self.config["logger_level"] = str(self.logger_level)
        self.config["folder_script"] = str(self.folder_script)

    def __write_config__(self):
        with open(Path(self.path), "w") as outfile:
            self.__preset__()
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
        self.__write_config__()

    @data_path.getter
    def data_path(self):
        return self.config.get(
            "data_path", Path.home() / ".servergrimoire/data"
        )

    @property
    def logger_level(self):
        return self.config["logger_level"]

    @logger_level.setter
    def logger_level(self, var):
        self.config["logger_level"] = var

    @logger_level.getter
    def logger_level(self):
        return self.config.get("logger_level", "ERROR")

    @property
    def folder_script(self):
        return self.config["folder_script"]

    @folder_script.setter
    def folder_script(self, var):
        self.config["folder_script"] = var
        self.__write_config__()

    @folder_script.getter
    def folder_script(self):
        return self.config.get(
            "folder_script", Path.home() / ".servergrimoire/script/"
        )
