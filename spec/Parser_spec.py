from parser import NginxParser, PageParser, ApacheParser

from unittest import TestCase


class PageParserTest(TestCase):

    def test_parser_type(self):

        headers = {'Server': 'nginx'}
        result = PageParser.get_parser_type(headers)

        self.assertEqual(result, NginxParser)


class NginxParserTest(TestCase):

    def setUp(self):
        self.parser = NginxParser()

        root_page_file = open("test_nginx_root.html", "r")
        self.root_page = root_page_file.read()
        root_page_file.close()

    def test_link_count(self):

        result = self.parser.get_links(self.root_page, "http://sv4avadl.uploadt.com/")
        self.assertEqual(len(result), 24)

    def test_link_size(self):
        result = self.parser.get_links(self.root_page, "http://sv4avadl.uploadt.com/")

        self.assertEqual(result["txt.jpg"]["size"], 142868)
        self.assertEqual(result["screenshot.rar"]["size"], 10477764)

    def test_link_extension(self):
        result = self.parser.get_links(self.root_page, "http://sv4avadl.uploadt.com/")

        self.assertEqual(result["txt.jpg"]["ext"], "jpg")
        self.assertEqual(result["screenshot.rar"]["ext"], "rar")

    def test_link_type(self):
        result = self.parser.get_links(self.root_page, "http://sv4avadl.uploadt.com/")

        self.assertEqual(result["txt.jpg"]["type"], "f")
        self.assertEqual(result["DL10/"]["type"], "d")

    def test_link_link(self):
        result = self.parser.get_links(self.root_page, "http://sv4avadl.uploadt.com/")

        self.assertEqual(result["txt.jpg"]["link"], "http://sv4avadl.uploadt.com/txt.jpg")
        self.assertEqual(result["DL10/"]["link"], "http://sv4avadl.uploadt.com/DL10/")


class ApacheParserTest(TestCase):

    def setUp(self):
        self.parser = ApacheParser()

        root_page_file = open("test_apache_root.html", "r")
        self.root_page = root_page_file.read()
        root_page_file.close()

    def test_size_column(self):
        result = self.parser.get_size_columns(['</a>', '175289', 'kB', '2008/10/21', '09:00:02', ''])

        self.assertEqual(result, (1, 2))


    def test_link_count(self):

        result = self.parser.get_links(self.root_page, "https://keisari.net/videos/")
        self.assertEqual(len(result), 51)

    def test_link_size(self):
        result = self.parser.get_links(self.root_page, "https://keisari.net/videos/")

        self.assertEqual(result["happyday.mp4"]["size"], 772000)
        self.assertEqual(result["alex_räjähtää.mp4"]["size"], 715000)

    def test_link_type(self):
        result = self.parser.get_links(self.root_page, "https://keisari.net/videos/")

        self.assertEqual(result["arnold_brownschwagger.mp4"]["type"], "f")
        self.assertEqual(result["to_be_continued/"]["type"], "d")

    def test_link_extension(self):
        result = self.parser.get_links(self.root_page, "https://keisari.net/videos/")

        self.assertEqual(result["webm_thread_intro.mp4"]["ext"], "mp4")


class ApacheParserTest2(TestCase):

    def setUp(self):
        self.parser = ApacheParser()

        root_page_file = open("test_apache2.html", "r")
        self.root_page = root_page_file.read()
        self.base_url = "http://akiraito.jpn.ph/g/%E6%98%A0%E7%94%BB%E3%83%BB%E3%83%89%E3%83%A9%E3%83%9E%E3%83%BB%E3%82%A2%E3%83%8B%E3%83%A1/%E3%80%90%E3%82%A2%E3%83%8B%E3%83%A1%E3%80%91%20%E3%83%89%E3%83%A9%E3%82%B4%E3%83%B3%E3%83%9C%E3%83%BC%E3%83%AB/%E3%80%90%E3%82%A2%E3%83%8B%E3%83%A1%E3%80%91%20%E3%83%89%E3%83%A9%E3%82%B4%E3%83%B3%E3%83%9C%E3%83%BC%E3%83%AB%EF%BC%BA%E3%80%80%E5%85%A8%EF%BC%92%EF%BC%99%EF%BC%91%E8%A9%B1/"
        root_page_file.close()

    def test_link_count(self):

        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(len(result), 297)

    def test_link_size(self):
        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(result["ƒhƒ‰ƒSƒ“ƒ{[ƒ‹Z.‘æ020˜b.u‚æ‚Ý‚ª‚¦‚éƒTƒCƒ„l“`àIŒå‹ó‚Ìƒ‹[ƒcv.wmv"]["size"], 179721000)
        self.assertEqual(result["ƒhƒ‰ƒSƒ“ƒ{[ƒ‹Z.‘æ225˜b.u‹­‚¢‚ºƒ`ƒrƒbƒRII‚P‚W†‘å‹êíIHv.wmv"]["size"], 347507000)

    def test_link_type(self):
        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(result["ƒhƒ‰ƒSƒ“ƒ{[ƒ‹Z.‘æ225˜b.u‹­‚¢‚ºƒ`ƒrƒbƒRII‚P‚W†‘å‹êíIHv.wmv"]["type"], "f")
        self.assertEqual(result["ƒhƒ‰ƒSƒ“ƒ{[ƒ‹Z jpg/"]["type"], "d")

    def test_link_extension(self):
        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(result["ƒhƒ‰ƒSƒ“ƒ{[ƒ‹Z.‘æ225˜b.u‹­‚¢‚ºƒ`ƒrƒbƒRII‚P‚W†‘å‹êíIHv.wmv"]["ext"], "wmv")