import json
import os
from pathlib import Path


class ConfigManager:
    def __init__(self, path):
        self.config = {}
        if path is None:
            path = Path.home() / ".servergrimoire_config"
        self.path = path

        if not os.path.exists(path):
            self.create_default()
        else:
            with open(path) as data_file:
                self.config = json.load(data_file)

    def create_default(self) -> dict:
        with open(Path(self.path), "w") as outfile:
            self.config["data_path"] = str(Path.home() / ".servergrimoire_data")
            json.dump(self.config, outfile)
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
