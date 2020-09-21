import datetime

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
            flag = w.expiration_date >= (
                datetime.datetime.now() - datetime.timedelta(days=30)
            )

            if flag:
                output_strng = {
                    "status": "OK",
                    "creation": f"{w.creation_date}",
                    "expiration": f"{w.expiration_date}",
                }
            else:
                output_strng = {
                    "status": "XX",
                    "creation": f"{w.creation_date}",
                    "expiration": f"{w.expiration_date}",
                }

        self.l.info(output_strng)
        return output_strng

    def stats(self, directive: str, data: dict) -> ({str: int}, {str: str}):
        stat = {"OK": 0, "KO": 0, "XX": 0}
        stat[data[directive]["status"]] = 1
        other = {}
        if data[directive]["status"] != "OK":
            other = {data[directive]["domain"]: data[directive]["expired"]}
        return stat, other
