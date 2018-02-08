from unittest import TestCase
from reddit_bot import RedditBot, TaskQueue, CrawTask
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


class TaskQueueTest(TestCase):

    def tearDown(self):
        if os.path.isfile("task_queue_test.txt"):
            os.remove("task_queue_test.txt")

    # def test_push_pop_test(self):
    #
    #     if os.path.isfile("task_queue_test.txt"):
    #         os.remove("task_queue_test.txt")
    #
    #     tq = TaskQueue("task_queue_test.txt")
    #     tq.push(CrawTask(dict()))
    #
    #     task1 = tq.pop()
    #
    #     self.assertEqual(tq.pop(), None)
    #     self.assertEqual(task1.submission.url, "http://awebsite.com/")
    #     self.assertEqual(task1.submission.post_id, "postid")
    #
    # def test_multiple_tasks(self):
    #     if os.path.isfile("task_queue_test.txt"):
    #         os.remove("task_queue_test.txt")
    #
    #     tq = TaskQueue("task_queue_test.txt")
    #
    #     tq.push(CrawTask(dict()))
    #     tq.push(CrawTask(dict()))
    #     tq.push(CrawTask(dict()))
    #
    #     self.assertIsNotNone(tq.pop())
    #     self.assertIsNotNone(tq.pop())
    #     self.assertIsNotNone(tq.pop())
    #     self.assertIsNone(tq.pop())
    #
    # def test_is_queued(self):
    #     if os.path.isfile("task_queue_test.txt"):
    #         os.remove("task_queue_test.txt")
    #
    #     tq = TaskQueue("task_queue_test.txt")
    #
    #     tq.push(CrawTask({id: "postid"}))
    #
    #     self.assertTrue(tq.is_queued("postid"))
    #     self.assertFalse(tq.is_queued("123456"))