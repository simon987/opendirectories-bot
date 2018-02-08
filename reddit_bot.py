import os
import json
from crawl_report import ReportBuilder
import operator
import humanfriendly


class CrawTask:

    def __init__(self, s):
        self.submission = s


class TaskQueue:

    def __init__(self):
        self.tasks = []

    def push(self, task):
        self.tasks.append(task)

    def pop(self):
        if len(self.tasks) > 0:
            t = self.tasks.pop()
        else:
            t = None

        return t

    def is_queued(self, post_id):

        for task in self.tasks:
            if task.submission.id == post_id:
                return True

        return False


def dumper(obj):
    return obj.__dict__


class RedditBot:

    def __init__(self, log_file: str):

        self.log_file = log_file

        self.crawled = []
        self.load_from_file()

    def log_crawl(self, post_id):

        self.load_from_file()
        self.crawled.append(post_id)

        with open(self.log_file, "w") as f:
            for post_id in self.crawled:
                f.write(post_id + "\n")

    def has_crawled(self, post_id):
        self.load_from_file()
        return post_id in self.crawled

    def load_from_file(self):
        if not os.path.isfile(self.log_file):
            self.crawled = []
        else:
            with open(self.log_file, "r") as f:
                self.crawled = list(filter(None, f.read().split("\n")))


class CommentBuilder:

    def __init__(self, report_builder: ReportBuilder, url, post_id):
        self.report_builder = report_builder
        self.url = url
        self.post_id = post_id

    def get_comment(self):

        total_size = self.report_builder.get_total_size()

        ext_counts = self.report_builder.get_ext_counts()
        ext_sizes = self.report_builder.get_ext_sizes()
        print(ext_sizes)
        ext_sizes_sorted = sorted(ext_sizes.items(), key=operator.itemgetter(1), reverse=True)
        print(ext_sizes_sorted)

        comment = "File types | Count | Total Size\n"
        comment += ":-- | :-- | :--    \n"

        counter = 0
        for i in range(0, len(ext_sizes_sorted)):

            comment += ext_sizes_sorted[i][0]
            comment += " | " + str(ext_counts[ext_sizes_sorted[i][0]])
            comment += " | " + str(humanfriendly.format_size(ext_sizes_sorted[i][1], True)) + "    \n"

            counter += 1
            if counter >= 3:
                break

        comment += "**Total** | **" + str(len(self.report_builder.files)) + "** | **"
        comment += self.report_builder.get_total_size_formatted() + "**    \n\n"

        comment += "[Full Report](https://simon987.net/od-bot/report/" + self.post_id + "/)"
        comment += " | [JSON](https://simon987.net/od-bot/report/" + self.post_id + "/json)"
        comment += " | [Link list](https://simon987.net/od-bot/report/" + self.post_id + "/links)    \n"
        comment += "***    \n^(Beep boop. I am a bot that calculates the file sizes & count of"
        comment += " open directories posted in /r/opendirectories/)"

        return comment
