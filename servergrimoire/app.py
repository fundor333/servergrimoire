import json
import logging
from typing import List

from rich import box, print
from rich.columns import Columns, Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table

from servergrimoire.configmanager import ConfigManager
from servergrimoire.operation.dnschecker import DNSChecker
from servergrimoire.operation.dnslookup import DNSLookup
from servergrimoire.operation.pagechecker import PageChecker
from servergrimoire.operation.sslverify import SSLVerify
from servergrimoire.plugin import Plugin

console = Console()


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

        FORMAT = "%(message)s"
        logging.basicConfig(
            level=self.setting_manager.logger_level,
            format=FORMAT,
            datefmt="[%X]",
            handlers=[RichHandler()],
        )

        self.logger = logging.getLogger("rich")

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

    def __get_directives_class(self) -> List[Plugin]:
        directive = [DNSChecker, DNSLookup, SSLVerify, PageChecker]
        # TODO Add reader from folder
        return directive

    def __get_directives_str(self) -> List[str]:
        """
        Return all directive into a array
        """
        arr_directives = []
        for _class in self.__get_directives_class():
            for e in _class.get_directives():
                arr_directives.append(e)
        return arr_directives

    def __get_urls_all(self) -> List[str]:
        """
        Return all urls into a array
        """
        try:
            return self.data["server"].keys()
        except Exception:
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

        with Progress() as progress:
            tasks = {}
            for command in command_to_run:
                tasks[command] = progress.add_task(
                    f"[cyan]{command}", total=(len(url_to_run))
                )

            for url in url_to_run:
                for command in command_to_run:
                    return_val = map_command[command]().execute(
                        command, self.data["server"][url]
                    )
                    self.data["server"][url][command] = return_val
                    progress.update(tasks[command], advance=1)

        with open(self.setting_manager.data_path, "w") as json_file:
            json.dump(self.data, json_file)

    def stats(self, command=None, url=None, short=False) -> None:
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

        if short:
            commands = []
            for command in command_to_run:
                data = {
                    k: self.data["server"][k]
                    for k in self.data["server"].keys() & set(url_to_run)
                }
                plugin = map_command[command]()
                _, errors = plugin.stats(command, data)
                commands.append(len(errors))
            stats_tab = self.__to_table(
                zip(command_to_run, commands),
                "ServerGrimoire",
                ["Command", "# Error"],
            )
            stats_tab.box = box.SIMPLE
            print(stats_tab)

            return
        for command in command_to_run:
            data = {
                k: self.data["server"][k]
                for k in self.data["server"].keys() & set(url_to_run)
            }
            plugin = map_command[command]()
            stats, errors = plugin.stats(command, data)
            stats_tab = self.__to_table(
                stats, plugin.title_stats(), plugin.header_stats()
            )

            error_tab = self.__to_table(
                errors, plugin.title_error(), plugin.header_error()
            )
            print(
                Panel(
                    Columns([stats_tab, error_tab]),
                    title=command,
                    highlight=True,
                )
            )

    def __to_table(
        self, matrix_data: List[List], title: str, header: List[str]
    ) -> Table:
        table = Table(title=title, box=box.MINIMAL, expand=True)
        for ele in header:
            table.add_column(ele)
        for row in matrix_data:
            row = list(map(str, row))
            table.add_row(*row)
        return table

    def info(self, command=None, url=None) -> None:
        """
        Launch info command for plugin
        """

        map_command = self.__get_directives_and_class()
        if command is None:
            command = self.__get_directives_str()
        for c in command:
            map_command[c]().info()

    def add(self, url) -> bool:
        """
        Add command for url
        """
        for e in url:
            if self.data.get("server") is None:
                self.data["server"] = {}
            if self.data["server"].get(e) is None:
                self.data["server"][e] = {"url": e}
                self.logger.info(f"Adding {url}")
        with open(self.setting_manager.data_path, "w") as json_file:
            json.dump(self.data, json_file)
        return True

    def remove(self, url=None) -> bool:
        """
        Remove command for url
        """
        self.data["server"].pop(url, None)
        with open(self.setting_manager.data_path, "w") as json_file:
            json.dump(self.data, json_file)
        self.logger.info(f"Removing {url}")
        return True
