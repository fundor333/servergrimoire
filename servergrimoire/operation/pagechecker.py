from typing import Tuple, List

import requests
import whois
from termcolor import colored
from urllib3.exceptions import NewConnectionError

from servergrimoire.plugin import Plugin


class PageChecker(Plugin):
    def can_handle(self, directive: str) -> bool:
        return directive == "p"

    @staticmethod
    def get_directives() -> List[str]:
        return ["page_checker"]

    def execute(self, directive: str, data: dict) -> dict:
        w = whois.whois(data["url"])
        try:
            try:
                if "https" not in data["url"]:
                    url = f"https://{data['url']}"
                else:
                    url = data["url"]
                status_code = requests.head(
                    url, allow_redirects=True
                ).status_code
            except requests.exceptions.SSLError:
                url = f"http://{data['url']}"
                status_code = requests.head(
                    url, allow_redirects=True
                ).status_code
        except NewConnectionError:
            status_code = 408

        self.logger.info(w)
        output_strng = {
            "status": status_code,
            "url": url,
        }
        self.logger.info(output_strng)
        return output_strng

    def stats(self, directive: str, data: dict) -> Tuple[dict, dict]:
        stat: dict = {}
        try:
            stat[str(data[directive]["status"])] = 1
            other = {}
            if not (200 <= data[directive]["status"] < 300):
                status = data[directive]["status"]
                try:
                    if 300 <= status < 400:
                        color = "blue"
                    elif 400 <= status < 500:
                        color = "yellow"
                    elif 500 <= status < 600:
                        color = "red"
                    else:
                        color = "cyan"
                    other = {
                        colored(data[directive]["url"], color): colored(
                            data[directive]["status"], color
                        )
                    }
                except KeyError:
                    other = {}
            return stat, other
        except KeyError:
            return {}, {}
