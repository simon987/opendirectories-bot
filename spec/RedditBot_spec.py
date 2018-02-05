from unittest import TestCase
from reddit_bot import RedditBot
import os


class RedditBotTest(TestCase):

    def test_load_crawled(self):

        with open("crawled.txt", "r") as f:
            saved_len = len(f.read())

        bot = RedditBot("crawled.txt")

        self.assertTrue(bot.has_crawled("384390"))
        self.assertFalse(bot.has_crawled("123456"))

        with open("crawled.txt", "r") as f:
            self.assertEqual(saved_len, len(f.read()))

    def test_save_crawled(self):

        if os.path.isfile("crawled_empty.txt"):
            os.remove("crawled_empty.txt")

        open("crawled_empty.txt", "w").close()

        tmp_bot = RedditBot("crawled_empty.txt")
        tmp_bot.log_crawl("000000")

        bot = RedditBot("crawled_empty.txt")

        self.assertTrue(bot.has_crawled("000000"))


