import datetime
from typing import Tuple

import whois

from servergrimoire.plugin import Plugin


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

    def stats(self, directive: str, data: dict) -> Tuple[dict, dict]:
        stat: dict = {"OK": 0, "KO": 0, "XX": 0}
        stat[data[directive]["status"]] = 1
        other = {}
        if data[directive]["status"] != "OK":
            try:
                other = {data[directive]["domain"]: data[directive]["expired"]}
            except KeyError:
                other = {}
        return stat, other
