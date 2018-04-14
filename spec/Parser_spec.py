from parsing import NginxParser, PageParser, ApacheParser

from unittest import TestCase


class PageParserTest(TestCase):

    def test_parser_type(self):

        headers = {'Server': 'nginx'}
        result = PageParser.get_parser_type(headers)

        self.assertEqual(result, NginxParser)


class NginxParserTest(TestCase):

    def setUp(self):
        self.parser = NginxParser()

        root_page_file = open("test_nginx1.html", "r")
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

        root_page_file = open("test_apache1.html", "r")
        self.root_page = root_page_file.read()
        root_page_file.close()

    def test_size_column(self):
        result = self.parser.get_size_columns(['</a>', '175289', 'kB', '2008/10/21', '09:00:02', ''], "")
        result1 = self.parser.get_size_columns(['100pxfilename.jpg', '175289', 'kB', '2008/10/21', '09:00:02', ''], "100pxfilename.jpg")

        self.assertEqual(result, (1, 2))
        self.assertEqual(result1, (1, 2))


    def test_link_count(self):

        result = self.parser.get_links(self.root_page, "https://keisari.net/videos/")
        self.assertEqual(len(result), 51)

    def test_link_size(self):
        result = self.parser.get_links(self.root_page, "https://keisari.net/videos/")

        self.assertEqual(result["happyday.mp4"]["size"], 772000)
        self.assertEqual(result["alex_r%c3%a4j%c3%a4ht%c3%a4%c3%a4.mp4"]["size"], 715000)

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

        self.assertEqual(result["ƒhƒ‰ƒSƒ“ƒ{[ƒ‹Z.‘æ011˜b.u‰F’ˆˆê‚Ì‹­íŽmƒTƒCƒ„l‚ß‚´‚ß‚éIv.wmv"]["size"], 232185000)
        self.assertEqual(result["ƒhƒ‰ƒSƒ“ƒ{[ƒ‹Z.‘æ019˜b.ud—Í‚Æ‚Ìí‚¢Iƒoƒuƒ‹ƒXŒN‚ð‚Â‚©‚Ü‚¦‚ëv.wmv"]["size"], 185385000)

    def test_link_type(self):
        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(result["ƒhƒ‰ƒSƒ“ƒ{[ƒ‹Z.‘æ011˜b.u‰F’ˆˆê‚Ì‹­íŽmƒTƒCƒ„l‚ß‚´‚ß‚éIv.wmv"]["type"], "f")
        self.assertEqual(result["ƒhƒ‰ƒSƒ“ƒ{[ƒ‹Z%20jpg/"]["type"], "d")

    def test_link_extension(self):
        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(result["ƒhƒ‰ƒSƒ“ƒ{[ƒ‹Z.‘æ011˜b.u‰F’ˆˆê‚Ì‹­íŽmƒTƒCƒ„l‚ß‚´‚ß‚éIv.wmv"]["ext"], "wmv")


class ApacheParserTest3(TestCase):

    def setUp(self):
        self.parser = ApacheParser()

        root_page_file = open("test_apache3.html", "r")
        self.root_page = root_page_file.read()
        self.base_url = "http://files.duspectacle.com/mp3/Jardinets/"
        root_page_file.close()

    def test_link_count(self):

        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(len(result), 21)

    def test_link_size(self):
        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(result["15%20Woodkid%20-%20Iron%20(Remix%20By%20Gucci%20Vump).mp3"]["size"], 9300000)
        self.assertEqual(result["16%20Yellow%20Ostrich%20-%20WHALE.mp3"]["size"], 7100000)

    def test_link_type(self):
        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(result["15%20Woodkid%20-%20Iron%20(Remix%20By%20Gucci%20Vump).mp3"]["type"], "f")
        self.assertEqual(result["01%20Jean%20Rochefort%20-%20Winnie%20et%20ses%20amis%20(introduction)/"]["type"], "d")

    def test_link_extension(self):
        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(result["15%20Woodkid%20-%20Iron%20(Remix%20By%20Gucci%20Vump).mp3"]["ext"], "mp3")


class ApacheParserTest4(TestCase):

    def setUp(self):
        self.parser = ApacheParser()

        root_page_file = open("test_apache4.html", "r")
        self.root_page = root_page_file.read()
        self.base_url = "http://jenserserver.no-ip.biz/movieserver/serien/bigbangtheorie/S3/"
        root_page_file.close()

    def test_link_size(self):
        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(result["The.Big.Bang.Theory.S03E06.Football.fuer.Nerds.German.WS.DVDRip.XviD-DELiCiOUS.avi"]["size"], 175000000)
        self.assertEqual(result["The.Big.Bang.Theory.S03E03.Sex.oder.Pralinen.German.WS.DVDRip.XviD-DELiCiOUS.avi"]["size"], 0)


class ApacheParserTest5(TestCase):

    def setUp(self):
        self.parser = ApacheParser()

        root_page_file = open("test.html", "r")
        self.root_page = root_page_file.read()
        self.base_url = "http://archive.scene.org/pub/resources/docs/"
        root_page_file.close()

    def test_link_size(self):
        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(result["17toilet.txt"]["size"], 12700)
        self.assertEqual(result["288help.diz"]["size"], 9000)


class ApacheParserTest7(TestCase):

    def setUp(self):
        self.parser = ApacheParser()

        root_page_file = open("test_apache7.html", "r")
        self.root_page = root_page_file.read()
        self.base_url = "http://www.serenitystreetnews.com/videos/feb 2013/"
        root_page_file.close()

    def test_link_size(self):
        result = self.parser.get_links(self.root_page, self.base_url)

        self.assertEqual(result["700%20Emerald%20Tablets%20Dark%20Brothers%20-%20YouTube.flv"]["size"], 145000000)
        self.assertEqual(result["Economic%20Collapse%20Survival%20Map%20-%20Risk%20Analysis%20of%20best%20area%20in%20United%20States%20-%20YouTube.flv"]["size"], 28000000)