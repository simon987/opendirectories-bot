from unittest import TestCase
from webserver import is_valid_id


class WebServerTest(TestCase):

    def test_report_id(self):

        self.assertTrue(is_valid_id("7ux5al"))
        self.assertFalse(is_valid_id(".7ux5al"))
        self.assertFalse(is_valid_id("7u/x5al"))
        self.assertFalse(is_valid_id("../7ux5al"))
        self.assertFalse(is_valid_id("1234567-"))
        self.assertFalse(is_valid_id("1234567"))
        self.assertFalse(is_valid_id("12345"))
