import os


class RedditBot:

    def __init__(self, log_file: str):

        self.log_file = log_file

        if not os.path.isfile(log_file):
            self.crawled = []
        else:
            with open(log_file, "r") as f:
                self.crawled = f.read().split("\n")
                self.crawled = list(filter(None, self.crawled))

    def log_crawl(self, post_id):

        self.crawled.append(post_id)

        with open(self.log_file, "w") as f:
            for post_id in self.crawled:
                f.write(post_id + "\n")

    def has_crawled(self, post_id):

        return post_id in self.crawled
