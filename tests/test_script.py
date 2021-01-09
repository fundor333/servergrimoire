import logging
from unittest.case import TestCase

from rich.logging import RichHandler

from servergrimoire.operation.sslverify import SSLVerify

FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger("rich")


class PluginT:
    def get_plugin(self):
        if self.plugin:
            return self.plugin
        else:
            raise NotImplementedError

    def get_data(self):
        if self.data:
            return self.data
        else:
            raise NotImplementedError

    def test_can_handle(self):
        commands = self.plugin.get_directives()
        logger.info(commands)
        for com in commands:
            self.assertEqual(True, self.plugin.can_handle(com))
        self.assertNotEqual(True, self.plugin.can_handle("Pinocchio"))
        self.assertNotEqual(True, self.plugin.can_handle("SSLCheck"))

    def test_not_implemented_error(self):
        directive = "Pippo"
        data = self.get_data()
        plugin = self.get_plugin()
        try:
            plugin.can_handle(directive)
        except NotImplementedError:
            self.fail("can_handle() raised NotImplementedError unexpectedly!")
        try:
            plugin.execute(directive, data)
        except NotImplementedError:
            self.fail("execute() raised NotImplementedError unexpectedly!")
        try:
            plugin.stats(directive, data)
        except NotImplementedError:
            self.fail("stats() raised NotImplementedError unexpectedly!")
        try:
            plugin.info(directive, data)
        except NotImplementedError:
            self.fail("info() raised NotImplementedError unexpectedly!")


class SSLVerifyTest(TestCase, PluginT):
    def setUp(self):
        self.plugin = SSLVerify()
        self.data = {
            "url": "fundor333.com",
            "ssl_check": {
                "status": "KO",
                "expired": "expiration date",
                "domain": "google.com",
            },
        }

    def status_test(self):
        stats, error = self.plugin.stats(data=self.data)
        self.assertDictEqual({"OK": 0, "KO": 1, "XX": 0}, stats)
        self.assertDictEqual({"KO": "expiration date"}, error)

    def test_execute(self):
        out = self.plugin.execute("ssl_check", self.data)
        logger.error(out)
