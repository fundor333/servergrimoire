from servergrimoire.configmanager import ConfigManager


class GrimoirePage:
    def __init__(self, path):
        self.path = path
        self.setting_manager = ConfigManager(path)