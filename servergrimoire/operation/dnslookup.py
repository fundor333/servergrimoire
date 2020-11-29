import dns.resolver

from servergrimoire.plugin import Plugin


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

    def stats(self, directive: str, data: dict) -> ({str: int}, {str: str}):
        stats = {}
        self.logger.debug(data[directive])
        for e in data[directive]:
            stats[e] = len(data[directive][e])
        other = {}
        self.logger.debug(stats)
        return stats, other
