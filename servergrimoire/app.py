import json
from pprint import pprint

from tabulate import tabulate

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
            with open(self.setting_manager.data_path, "w") as f:
                json.dump({}, f)
            self.data = {}

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
            return self.data["server"].keys()
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
                self.data["server"][url][command] = cl.execute(
                    directive=command, data=self.data["server"][url]
                )

        with open(self.setting_manager.data_path, "w") as json_file:
            json.dump(self.data, json_file)

    def stats(self, command=None, url=None) -> None:
        """
        Launch stats command for plugin
        """
        map_command = self.__get_directives_and_class()
        if command is None:
            command_to_run = self.__get_directives_str()
        else:
            command_to_run = [command]
        if url is None:
            url_to_run = self.__get_urls_all()
        else:
            url_to_run = [url]

        printable = {}
        for command in command_to_run:
            printable[command] = {}
            for url in url_to_run:
                all = map_command[command]().stats(command, self.data["server"][url])
                for key in all.keys():
                    printable[command][key] = printable[command].get(key, 0) + int(
                        all[key]
                    )

        for command in printable.keys():
            message = [(k, v) for k, v in printable[command].items()]
            head = [command, ""]
            print(tabulate(message, head, tablefmt="pipe"))
            print()

    def add(self, url) -> bool:
        """
        Add command for url
        """
        for e in url:
            if self.data.get("server") is None:
                self.data["server"] = {}
            if self.data["server"].get(e) is None:
                self.data["server"][e] = {"url": e}
        with open(self.setting_manager.data_path, "w") as json_file:
            json.dump(self.data, json_file)

    def remove(self, url=None) -> bool:
        """
        Remove command for url
        """
        self.data["server"].pop(url, None)
        with open(self.setting_manager.data_path, "w") as json_file:
            json.dump(self.data, json_file)
