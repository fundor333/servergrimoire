from typing import Tuple

import requests
import whois

from servergrimoire.plugin import Plugin


class PageChecker(Plugin):
    def can_handle(self, directive: str) -> bool:
        return directive == "p"

    @staticmethod
    def get_directives() -> [str]:
        return ["page_checker"]

    def execute(self, directive: str, data: dict) -> dict:
        w = whois.whois(data["url"])
        if "http" not in data["url"]:
            url = f"http://{data['url']}"
        else:
            url = data["url"]
        if w["domain_name"] is None:
            output_strng = {"status": 408, "url": url}
        else:
            self.logger.info(w)
            output_strng = {
                "status": requests.get(url).status_code,
                "url": url,
            }
        self.logger.info(output_strng)
        return output_strng

    def stats(self, directive: str, data: dict) -> Tuple[dict, dict]:
        stat: dict = {}
        try:
            stat[str(data[directive]["status"])] = 1
            other = {}
            if not (200 <= data[directive]["status"] < 400):
                try:
                    other = {data[directive]["url"]: data[directive]["status"]}
                except KeyError:
                    other = {}
            return stat, other
        except KeyError:
            return {}, {}
