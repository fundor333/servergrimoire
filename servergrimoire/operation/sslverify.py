import datetime
import socket
import ssl
from servergrimoire.plugin import Plugin

BROKEN_RESPONSE = {"status": "KO", "expired": "****-**-** **:**:**"}


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
        try:
            will_expire_in = self.__ssl_valid_time_remaining(data["url"])
        except FileNotFoundError as e:
            output_strng = BROKEN_RESPONSE
        except socket.gaierror as e:
            output_strng = BROKEN_RESPONSE
        except ssl.CertificateError as e:
            output_strng = BROKEN_RESPONSE
        except ssl.SSLError as e:
            output_strng = BROKEN_RESPONSE
        except socket.timeout as e:
            output_strng = BROKEN_RESPONSE
        else:
            if will_expire_in is None:
                output_strng = BROKEN_RESPONSE
            elif will_expire_in < limit:
                output_strng = {"status": "KO", "expired": str(will_expire_in)}
            elif will_expire_in < limit:
                output_strng = {"status": "XX", "expired": str(will_expire_in)}
            else:
                output_strng = {"status": "OK", "expired": str(will_expire_in)}
        self.l.info(f"{directive} return {output_strng}")
        return output_strng

    def stats(self, directive: str, data: dict) -> {str: int}:
        stat = {"OK": 0, "KO": 0, "XX": 0}
        stat[data[directive]["status"]] = 1
        return stat
