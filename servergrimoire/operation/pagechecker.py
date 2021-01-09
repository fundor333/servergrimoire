from typing import List, Tuple

import requests
import whois
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry

from servergrimoire.plugin import Plugin

MARKDOWN = """
# Page Checker

Save the HTTP/HTTPS status of the url
"""

TIMEOUT = 5
s = Session()
retries = Retry(total=3, backoff_factor=0)
adapter = HTTPAdapter(max_retries=retries)
s.mount("https://", adapter)
s.mount("http://", adapter)


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
                status_code = s.head(
                    url, allow_redirects=True, timeout=TIMEOUT
                ).status_code
            except requests.exceptions.SSLError:
                url = f"http://{data['url']}"
                status_code = s.head(
                    url, allow_redirects=True, timeout=TIMEOUT
                ).status_code
            self.logger.info(w)
        except requests.exceptions.ConnectTimeout:
            status_code = 408
        except Exception:
            status_code = 400

        output_strng = {
            "status": status_code,
            "url": url,
        }
        self.logger.info(output_strng)
        return output_strng

    def stats(
        self, directive: str, data: dict
    ) -> Tuple[List[List], List[List]]:
        stat_temp: dict = {}
        other = []
        try:
            for key in data.keys():
                data_filter = data[key][directive]
                stat_temp[str(data_filter["status"])] = 1
                if not (200 <= data_filter["status"] < 300):
                    status = data_filter["status"]
                    try:
                        if 300 <= status < 400:
                            color = "blue"
                        elif 400 <= status < 500:
                            color = "yellow"
                        elif 500 <= status < 600:
                            color = "red"
                        else:
                            color = "cyan"
                        other.append(
                            [
                                f"[{color}]{data_filter['url']}",
                                f"[{color}]{data_filter['status']}",
                            ]
                        )
                    except KeyError:
                        pass
            stats = []
            for key, value in stat_temp.items():
                temp = [key, value]
                stats.append(temp)

            return stats, other
        except KeyError:
            return [], []

    def header_stats(self) -> List[str]:
        return ["Status", "Number"]

    def header_error(self) -> List[str]:
        return ["Url", "Status"]

    def title_stats(self) -> str:
        return "Page Checker Stats"

    def title_error(self) -> str:
        return "Page Checker Error"

    def get_markdown(self):
        """
        Return info text as Markdown
        """
        return MARKDOWN
