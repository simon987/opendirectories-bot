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

    # def test_guess_parser3(self):
    #     with open("test_invalid.html", "r") as f:
    #         text = f.read()
    #
    #     c = Crawler("http://some.website", False)
    #
    #     self.assertEqual(c.guess_parser(text, {}), None)

    def test_invalid_schema(self):

        c1 = Crawler("http://google.com/", False)
        c2 = Crawler("https://google.com/", False)
        c3 = Crawler("ftp://website.com/", False)
        c4 = Crawler("ws://website.com/", False)

        self.assertIsNotNone(c1.parser)
        self.assertIsNotNone(c2.parser)
        self.assertIsNone(c3.parser)
        self.assertIsNone(c4.parser)
