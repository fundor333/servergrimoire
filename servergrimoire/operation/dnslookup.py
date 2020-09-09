import dns.resolver
from servergrimoire.plugin import Plugin


class DNSLookup(Plugin):
    def can_handle(self, directive: str) -> bool:
        return directive == "dns_lookup"

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
                for rdata in dns.resolver.resolve(query, label):
                    output[label] = str(rdata)
            except:
                self.l.info(f"Not found {label} for {domain}")
        return output

    def stats(self, directive: str, data: dict) -> {str: int}:
        return dict()
