import os
import json


class CrawTask:

    def __init__(self, url, post_id, title):
        self.url = url
        self.post_id = post_id
        self.post_title = title


class TaskQueue:

    def __init__(self, file):
        self.file = file

        self.tasks = []

        if os.path.isfile(self.file):

            with open(self.file, "r") as f:
                json_tasks = json.load(f)

                for task in json_tasks:
                    self.tasks.append(CrawTask(task["url"], task["post_id"], task["post_title"]))

    def push(self, task):
        self.tasks.append(task)
        self.update_file()

    def pop(self):
        if len(self.tasks) > 0:
            t = self.tasks.pop()
            self.update_file()
        else:
            t = None

        return t

    def update_file(self):
        with open(self.file, "w") as f:
            json.dump(self.tasks, f, default=dumper)

    def is_queued(self, post_id):

        for task in self.tasks:
            if task.post_id == post_id:
                return True

        return False


def dumper(obj):
    return obj.__dict__


class RedditBot:

    def __init__(self, log_file: str):

        self.log_file = log_file

        if not os.path.isfile(log_file):
            self.crawled = []
        else:
            with open(log_file, "r") as f:
                self.crawled = list(filter(None, f.read().split("\n")))

    def log_crawl(self, post_id):

        self.crawled.append(post_id)

        with open(self.log_file, "w") as f:
            for post_id in self.crawled:
                f.write(post_id + "\n")

    def has_crawled(self, post_id):

        return post_id in self.crawled
