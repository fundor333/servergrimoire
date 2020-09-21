import datetime
import socket
import ssl
from termcolor import colored
from servergrimoire.plugin import Plugin


def broken_response(url) -> {str, str, str}:
    return {"status": "KO", "expired": "****-**-** **:**:**", "domain": url}


class SSLVerify(Plugin):
    def can_handle(self, directive: str) -> bool:
        return directive == "ssl_check"

    @staticmethod
    def get_directives() -> [str]:
        return ["ssl_check"]

    def __ssl_valid_time_remaining(self, hostname: str) -> datetime.datetime:
        ssl_date_fmt = r"%b %d %H:%M:%S %Y %Z"

        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET), server_hostname=hostname,
        )

        self.l.debug("Connect to {}".format(hostname))
        conn.connect((hostname, 443))
        ssl_info = conn.getpeercert()
        # parse the string from the certificate into a Python datetime object
        return datetime.datetime.strptime(ssl_info["notAfter"], ssl_date_fmt)

    def execute(self, directive: str, data: dict) -> dict:
        """Return test message for hostname cert expiration."""
        limit = datetime.datetime.now() + datetime.timedelta(days=30)
        output_strng = None
        url = data["url"]
        try:
            will_expire_in = self.__ssl_valid_time_remaining(url)
        except ResourceWarning as e:
            output_strng = broken_response(url)
        except OSError as e:
            output_strng = broken_response(url)
        except FileNotFoundError as e:
            output_strng = broken_response(url)
        except socket.gaierror as e:
            output_strng = broken_response(url)
        except ssl.CertificateError as e:
            output_strng = broken_response(url)
        except TimeoutError:
            output_strng = broken_response(url)
        except ssl.SSLError as e:
            output_strng = broken_response(url)
        except socket.timeout as e:
            output_strng = broken_response(url)
        else:
            if will_expire_in is None:
                output_strng = broken_response(url)
            elif will_expire_in < limit:
                output_strng = {
                    "status": "KO",
                    "expired": str(will_expire_in),
                    "domain": url,
                }
            elif will_expire_in < limit:
                output_strng = {
                    "status": "XX",
                    "expired": str(will_expire_in),
                    "domain": url,
                }
            else:
                output_strng = {
                    "status": "OK",
                    "expired": str(will_expire_in),
                    "domain": url,
                }
        self.l.info(f"{directive} return {output_strng}")
        return output_strng

    def stats(self, directive: str, data: dict) -> ({str: int}, {str: str}):
        try:
            stat = {"OK": 0, "KO": 0, "XX": 0}
            stat[data[directive]["status"]] = 1
            other = {}
            if data[directive]["status"] != "OK":
                other = {
                    colored(data[directive]["domain"], "red"): colored(
                        data[directive]["expired"], "red"
                    )
                }
            return stat, other
        except KeyError as e:
            self.l.error(str(e))
            return {}, {}
