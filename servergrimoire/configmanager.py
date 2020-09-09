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
