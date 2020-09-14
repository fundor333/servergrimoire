import datetime
import socket
import ssl

from loguru import logger

from servergrimoire.plugin import Plugin


def broken_response(url: str, e: Exception) -> str:
    logger.info(f"{url} return {e}")
    return {"status": "KO", "expired": "****-**-** **:**:**"}


class SSLVerify(Plugin):
    def can_handle(self, directive: str) -> bool:
        return directive == "ssl_check"

    def __ssl_valid_time_remaining(self, hostname: str) -> datetime.datetime:
        ssl_date_fmt = r"%b %d %H:%M:%S %Y %Z"

        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET), server_hostname=hostname,
        )

        self.l.info("Connect to {}".format(hostname))
        conn.connect((hostname, 443))
        ssl_info = conn.getpeercert()
        return datetime.datetime.strptime(ssl_info["notAfter"], ssl_date_fmt)

    def execute(self, directive: str, data: dict) -> dict:
        """Return test message for hostname cert expiration."""
        limit = datetime.datetime.now() + datetime.timedelta(days=30)
        output_strng = None
        try:
            will_expire_in = self.__ssl_valid_time_remaining(data["url"])
        except FileNotFoundError as e:
            output_strng = broken_response(e)
        except socket.gaierror as e:
            output_strng = broken_response(e)
        except ssl.CertificateError as e:
            output_strng = broken_response(e)
        except ssl.SSLError as e:
            output_strng = broken_response(e)
        except socket.timeout as e:
            output_strng = broken_response(e)
        else:
            if will_expire_in is None:
                output_strng = {"status": "KO", "expired": "****-**-** **:**:**"}
                self.l.info(f"{directive} return {output_strng}")
            elif will_expire_in < limit:
                output_strng = {"status": "KO", "expired": str(will_expire_in)}
                self.l.info(f"{directive} return {output_strng}")
            elif will_expire_in < limit:
                output_strng = {"status": "XX", "expired": str(will_expire_in)}
                self.l.info(f"{directive} return {output_strng}")
            else:
                output_strng = {"status": "OK", "expired": str(will_expire_in)}
                self.l.info(f"{directive} return {output_strng}")
        return output_strng

    def stats(self, directive: str, data: dict) -> {str: int}:
        stat = {"OK": 0, "KO": 0, "XX": 0}
        stat[data[directive]["status"]] = 1
        return stat
