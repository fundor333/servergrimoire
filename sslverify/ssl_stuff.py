import datetime
import logging
import socket
import ssl
from typing import Iterable

from sslverify import print_stuff

logger = logging.getLogger("SSLVerify")
pc = print_stuff.PrintColor()


def ssl_valid_time_remaining(hostname: str) -> datetime.datetime:
    ssl_date_fmt = r"%b %d %H:%M:%S %Y %Z"

    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname, )
    conn.settimeout(3.0)

    logger.debug("Connect to {}".format(hostname))
    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info["notAfter"], ssl_date_fmt)


def ssh_status(hostname: str, buffer_days: int = 30) -> (bool, str, datetime.datetime):
    """Return test message for hostname cert expiration."""
    limit = datetime.datetime.now() + datetime.timedelta(days=buffer_days)
    output_strng = None
    try:
        will_expire_in = ssl_valid_time_remaining(hostname)
    except socket.gaierror as e:
        output_strng = False, hostname, None
    except ssl.CertificateError as e:
        if "Hostname mismatch" in str(e):
            output_strng = False, hostname, None
    except ssl.SSLError as e:
        logger.error(f"{hostname} launch this error {e}")
        output_strng = False, hostname, None
    except socket.timeout as e:
        logger.error(f"{hostname} launch this error {e}")
        output_strng = False, hostname, None
    else:
        if will_expire_in < limit:
            output_strng =False, hostname, will_expire_in
        elif will_expire_in < limit:
            output_strng = None, hostname, will_expire_in
        else:
            output_strng = True, hostname, will_expire_in
    logger.info(output_strng)
    return output_strng


def ssh_check_hostname(hosts: Iterable) -> [[str, str, str]]:
    output_array = []
    for data in hosts:
        host = data["host"]
        buffer_day = data.get("buffer", 30)
        host = host.strip()
        message = ssh_status(host, buffer_day)
        output_array.append(message)
    return sorted(output_array, key=lambda x: x[2])
