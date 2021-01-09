import datetime
import socket
import ssl
from typing import Tuple, List

from servergrimoire.plugin import Plugin

MARKDOWN = """
# SSL Verify

Plugin for get some info of the SSL certificate of a domain
"""


def broken_response(url) -> {str, str, str}:
    return {
        "status": "KO",
        "expired": "****-**-** **:**:**",
        "domain": url,
        "organization_name": "***",
    }


class SSLVerify(Plugin):
    def can_handle(self, directive: str) -> bool:
        return directive == "ssl_check"

    @staticmethod
    def get_directives() -> [str]:
        return ["ssl_check"]

    def __ssl_valid_time_remaining(
        self, hostname: str
    ) -> Tuple[datetime.datetime, str]:
        ssl_date_fmt = r"%b %d %H:%M:%S %Y %Z"

        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=hostname,
        )

        self.logger.debug("Connect to {}".format(hostname))
        conn.connect((hostname, 443))
        ssl_info = conn.getpeercert()
        # parse the string from the certificate into a Python datetime object
        self.logger.info(ssl_info)
        try:
            organizzator = ssl_info["issuer"][2][0][1]
            self.logger.info(f"How relaise it {organizzator}")
        except Exception as e:
            organizzator = "***"
            self.logger.info(e)
        return (
            datetime.datetime.strptime(ssl_info["notAfter"], ssl_date_fmt),
            organizzator,
        )

    def execute(self, directive: str, data: dict) -> dict:
        """Return test message for hostname cert expiration."""
        limit = datetime.datetime.now() + datetime.timedelta(days=30)
        output_strng = None
        url = data["url"]
        try:
            will_expire_in, organizzator = self.__ssl_valid_time_remaining(url)
        except ResourceWarning:
            output_strng = broken_response(url)
        except OSError:
            output_strng = broken_response(url)
        except FileNotFoundError:
            output_strng = broken_response(url)
        except socket.gaierror:
            output_strng = broken_response(url)
        except ssl.CertificateError:
            output_strng = broken_response(url)
        except TimeoutError:
            output_strng = broken_response(url)
        except ssl.SSLError:
            output_strng = broken_response(url)
        except socket.timeout:
            output_strng = broken_response(url)
        else:
            self.logger.info(
                f"will_expire {will_expire_in}, limit {limit}, today {datetime.datetime.now()}"
            )
            if will_expire_in is None:
                output_strng = broken_response(url)
            elif will_expire_in < datetime.datetime.now():
                output_strng = {
                    "status": "KO",
                    "expired": str(will_expire_in),
                    "domain": url,
                    "organization_name": organizzator,
                }
            elif will_expire_in < limit:
                output_strng = {
                    "status": "XX",
                    "expired": str(will_expire_in),
                    "domain": url,
                    "organization_name": organizzator,
                }
            else:
                output_strng = {
                    "status": "OK",
                    "expired": str(will_expire_in),
                    "domain": url,
                    "organization_name": organizzator,
                }
        self.logger.info(f"{directive} return {output_strng}")
        return output_strng

    def stats(
        self, directive: str, data: dict
    ) -> Tuple[List[List], List[List]]:
        try:
            stat = {"OK": 0, "KO": 0, "XX": 0}
            other = []
            for key in data.keys():
                data_filter = data[key][directive]
                stat[data_filter["status"]] = 1
                if data_filter["status"] == "KO":
                    other.append(
                        [
                            f"[red]{data_filter['domain']}",
                            f"[red]{data_filter['expired']} ",
                            f"[red]{data_filter['organization_name']}",
                        ]
                    )
                elif data_filter["status"] == "XX":
                    other.append(
                        [
                            f"[yellow]{data_filter['domain']}",
                            f"[yellow]{data_filter['expired']}",
                            f"[yellow]{data_filter['organization_name']}",
                        ]
                    )
            return (
                [
                    ["OK", stat["OK"]],
                    ["KO", stat["KO"]],
                    ["XX", stat["XX"]],
                ],
                other,
            )
        except KeyError as e:
            self.logger.error(str(e))
            return [], []

    def header_stats(self) -> List[str]:
        return ["Status", "Number"]

    def header_error(self) -> List[str]:
        return ["Url", "Date", "Authority"]

    def title_stats(self) -> str:
        return "SSL Verify Status"

    def title_error(self) -> str:
        return "SSL Verify Error"

    def get_markdown(self):
        """
        Return info text as Markdown
        """
        return MARKDOWN
