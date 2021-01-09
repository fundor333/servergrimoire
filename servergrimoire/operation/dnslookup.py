from typing import List, Tuple

import dns.resolver

from servergrimoire.plugin import Plugin

MARKDOWN = """
# DNSL Lookup

Save the DNSL lookup of the domain
"""


class DNSLookup(Plugin):
    def can_handle(self, directive: str) -> bool:
        return directive == "dns_lookup"

    @staticmethod
    def get_directives() -> [str]:
        return ["dns_lookup"]

    def execute(self, directive: str, data: dict) -> dict:
        domain = data["url"]
        array_input = [
            (domain, "A"),
            (domain, "MX"),
            ("mail." + domain, "A"),
            (domain, "NS"),
            (domain, "TXT"),
        ]
        output = {}
        for query, label in array_input:
            try:
                output[label] = []
                for rdata in dns.resolver.resolve(query, label):
                    output[label].append(str(rdata))
            except Exception:
                output.pop(label)
                self.logger.info(f"Not found {label} for {domain}")
        return output

    def stats(
        self, directive: str, data: dict
    ) -> Tuple[List[List], List[List]]:
        stats = {"MX": 0, "NS": 0, "TXT": 0, "A": 0}
        for key in data.keys():
            data_filter = data[key][directive]
            self.logger.debug(data_filter)
            for e in data_filter:
                stats[e] += len(data_filter[e])
            self.logger.debug(stats)
        return [
            ["MX", stats["MX"]],
            ["NS", stats["NS"]],
            ["TXT", stats["TXT"]],
            ["A", stats["A"]],
        ], []

    def header_stats(self) -> List[str]:
        return ["Type", "Number"]

    def header_error(self) -> List[str]:
        return ["Type", "Number"]

    def title_stats(self) -> str:
        return "DNS Lookup Stats"

    def title_error(self) -> str:
        return "DNS Lookup Error"

    def get_markdown(self):
        """
        Return info text as Markdown
        """
        return MARKDOWN
