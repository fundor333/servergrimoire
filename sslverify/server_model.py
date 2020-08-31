import datetime
import logging
import socket

from sslverify.djangocheck import single_django_checker
from sslverify.ssl_stuff import ssh_status

logger = logging.getLogger(__name__)


class SSLData:
    def __init__(self, hostname: str, buffer: int = 30, ssl: bool = False, ssl_last_check: datetime.datetime = None,
                 expiration: datetime.datetime = None):
        self.buffer = buffer
        self.ssl = ssl
        self.ssl_last_check = ssl_last_check
        self.expiration = expiration
        self.hostname = hostname.strip()

    def check(self):
        self.ssl, _, self.expiration = ssh_status(self.hostname, self.buffer)
        self.ssl_last_check = datetime.datetime.now()

    def __str__(self):
        self.check()
        return {"buffer": self.buffer,
                "ssl": self.ssl,
                "ssl_last_check": f"{self.ssl_last_check}",
                "espiration": f"{self.expiration}"}


class EndpointChecker:
    def __init__(self,hostname:str, path: str = "/life", message_out: dict = {"status": "alive and kicking"}, endpoint_check: bool = False,
                 last_check: datetime.datetime = None, last_status: int = None):
        self.path = path
        self.hostname=hostname
        self.message_out = message_out
        self.endpoint_check = endpoint_check
        self.last_check = last_check
        self.last_status = last_status

    def check(self):
        self.endpoint_check, _, _ , self.last_status= single_django_checker(self.hostname, self.path,self.message_out)
        self.last_check = datetime.datetime.now()


    def __str__(self):
        self.check()
        return {"paht": self.path, "message_out": self.message_out, "endpoint_check": self.endpoint_check, "last_check": f"{self.last_check}",
                "last_status": self.last_status}


class Server:
    def __init__(self, hostname, buffer: int = 30, endpoint_check: EndpointChecker = None):
        self.hostname = hostname
        self.ip = socket.gethostbyname(hostname)
        self.ssl_data = SSLData(hostname, buffer)
        self.endpoint_check = endpoint_check

    def add_django_check(self):
        self.endpoint_check = EndpointChecker(self.hostname)

    def __str__(self):
        output = {
            "ip": self.ip,
            "hostname": self.hostname,
        }

        if self.endpoint_check:
            output["endpoint_check"] = self.endpoint_check.__str__()
        if self.ssl_data:
            output["ssl_data"] = self.ssl_data.__str__()

        return output

