import datetime
from typing import List, Tuple

import whois

from servergrimoire.plugin import Plugin

MARKDOWN = """
# DNS Check

Check the DNS for the domain
"""


class DNSChecker(Plugin):
    def can_handle(self, directive: str) -> bool:
        return directive == "dns_checker"

    @staticmethod
    def get_directives() -> [str]:
        return ["dns_checker"]

    def execute(self, directive: str, data: dict) -> dict:
        w = whois.whois(data["url"])
        if w["domain_name"] is None:
            output_strng = {
                "status": "XX",
                "creation": "Error trying to connect to socket",
                "expiration": "Error trying to connect to socket",
            }
        else:
            self.logger.info(w)

            if isinstance(w.expiration_date, list):
                expiration_date = w.expiration_date[0]
            else:
                expiration_date = w.expiration_date

            flag = expiration_date >= (
                datetime.datetime.now() - datetime.timedelta(days=30)
            )

            self.logger.info(flag)

            if flag:
                output_strng = {
                    "status": "OK",
                    "creation": f"{expiration_date}",
                    "expiration": f"{w.expiration_date}",
                }
            else:
                output_strng = {
                    "status": "XX",
                    "creation": f"{expiration_date}",
                    "expiration": f"{w.expiration_date}",
                }

        self.logger.info(output_strng)
        return output_strng

    def stats(
        self, directive: str, data: dict
    ) -> Tuple[List[List], List[List]]:
        stat: dict = {"OK": 0, "KO": 0, "XX": 0}
        other = []
        for key in data.keys():
            data_filter = data[key][directive]["status"]
            stat[data_filter] += 1
            if data_filter != "OK":
                try:
                    other.append(
                        [data[directive]["domain"], data[directive]["expired"]]
                    )
                except KeyError:
                    pass
        return [
            ["OK", stat["OK"]],
            ["KO", stat["KO"]],
            ["XX", stat["XX"]],
        ], other

    def header_stats(self) -> List[str]:
        return ["Status", "Number"]

    def header_error(self) -> List[str]:
        return ["URL", "Date"]

    def title_stats(self) -> str:
        return "DNS Checker Stats"

    def title_error(self) -> str:
        return "DNS Checker Error"

    def get_markdown(self):
        """
        Return info text as Markdown
        """
        return MARKDOWN
