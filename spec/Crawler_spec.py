from unittest import TestCase

from parser import ApacheParser, NginxParser
from crawler import Crawler


class CrawlerTest(TestCase):

    def test_guess_parser1(self):

        with open("test_apache1.html", "r") as f:
            text = f.read()

        c = Crawler("http://some.website/", False)

        self.assertEqual(c.guess_parser(text, {}), ApacheParser)

    def test_guess_parser2(self):
        with open("test_nginx1.html", "r") as f:
            text = f.read()

        c = Crawler("http://some.website", False)

        self.assertEqual(c.guess_parser(text, {}), NginxParser)

    def test_guess_parser3(self):
        with open("test_invalid.html", "r") as f:
            text = f.read()

        c = Crawler("http://some.website", False)

        self.assertEqual(c.guess_parser(text, {}), None)