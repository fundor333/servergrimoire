import json
import pathlib


class ConfigManager:
    def __init__(self, path):
        self.path = path
        file = pathlib.Path(path)
        if file.exists():
            with open(path) as data_file:
                self.config = json.load(data_file)
        else:
            self.config = self.create_default()

    def create_default(self) -> dict:
        with open(self.path, 'w') as outfile:
            json.dump(self.config, outfile)

    @property
    def data_path(self):
        return self.config["data_path"]

    @data_path.setter
    def data_path(self, var):
        self.config["data_path"] = var

    @data_path.getter
    def data_path(self):
        if self.config.get("data_path", None) is None:
            self.config["data_path"] = "~/.servergrimoire_data"
        return self.config["data_path"]
