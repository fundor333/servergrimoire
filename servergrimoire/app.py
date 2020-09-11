import json

from servergrimoire.configmanager import ConfigManager
from servergrimoire.operation.dnschecker import DNSChecker
from servergrimoire.operation.dnslookup import DNSLookup
from servergrimoire.operation.sslverify import SSLVerify
from servergrimoire.plugin import Plugin


class GrimoirePage:
    def __init__(self, path):
        self.path = path
        self.setting_manager = ConfigManager(path)

        try:
            with open(self.setting_manager.data_path) as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open(self.setting_manager.data_path,"w") as f:
                json.dump({}, f)
            self.data={}


    def __get_directives_and_class(self) -> dict:
        """
        Return a dict with all directories and theire class
        """
        dict_directives = {}
        for _class in self.__get_directives_class():
            for e in _class.get_directives():
                dict_directives[e] = _class
        return dict_directives

    def __get_urls(self):
        """
        Return a array with all urls and theire class
        """
        return self.__get_directives_class().keys()

    def __get_directives_class(self) -> [Plugin]:
        return [DNSChecker, DNSLookup, SSLVerify]

    def __get_directives_str(self) -> [str]:
        """
        Return all directive into a array
        """
        arr_directives = []
        for _class in self.__get_directives_class():
            for e in _class.get_directives():
                arr_directives.append(e)
        return arr_directives

    def __get_urls_all(self) -> [str]:
        """
        Return all urls into a array
        """
        try:
            return self.data['server'].keys()
        except:
            return []

    def run(self, command=None, url=None):
        """
        Launch command for plugin
        """
        map_command = self.__get_directives_and_class()
        if command is None:
            command_to_run = self.__get_directives_str()
        else:
            command_to_run = [command]
        url_to_run = None
        if url is None:
            url_to_run = self.__get_urls_all()
        else:
            url_to_run = [url]

        for url in url_to_run:
            for command in command_to_run:
                cl = map_command[command]()
                self.data['server'][url][command] = cl.execute(directive=command,data=self.data['server'][url])

        with open(self.setting_manager.data_path, 'w') as json_file:
            json.dump(self.data, json_file)

    def stats(self, command=None, url=None) -> bool:
        """
        Launch stats command for plugin
        """
        raise NotImplementedError

    def add(self, command=None, url=None) -> bool:
        """
        Add command for url
        """
        raise NotImplementedError

    def remove(self, command=None, url=None) -> bool:
        """
        Remove command for url
        """
        raise NotImplementedError
