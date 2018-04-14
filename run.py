from crawler import Crawler
from reddit_bot import RedditBot, TaskQueue, CrawTask, CommentBuilder, ReportBuilder
import time
from multiprocessing import Process
import praw

reddit = praw.Reddit('opendirectories-bot',
                     user_agent='github.com/simon987/opendirectories-bot v1.0  (by /u/Hexahedr_n)')

subreddit = reddit.subreddit("opendirectories")

subs = []

for submission in subreddit.new(limit=3):
    subs.append(submission)

bot = RedditBot("crawled.txt")
tq = TaskQueue()

for s in subs:

    if not s.is_self:
        if not bot.has_crawled(s.id) and not tq.is_queued(s.id):
            tq.push(CrawTask(s))

            print("id: " + s.id)
            print("url: " + str(s.url))
            print("title: " + str(s.title))


def execute_task(submission):

    try:
        if not bot.has_crawled(submission.id):
            c = Crawler(submission.url, True)
            c.crawl()
            c.store_report(submission.id, submission.title)

            report_builder = ReportBuilder(c.files, c.base_url)

            if report_builder.get_total_size() > 10000000:
                com_buider = CommentBuilder(ReportBuilder(c.files, c.base_url), c.base_url, submission.id)

                com_string = com_buider.get_comment()

                print(com_string)
                while True:
                    try:
                        if not bot.has_crawled(submission.id):
                            submission.reply(com_string)
                            bot.log_crawl(submission.id)
                        break
                    except Exception as e:
                        print("Waiting 10 minutes: " + str(e))
                        time.sleep(600)
                        continue

    except Exception as e:
        print(e)
        raise e


while len(tq.tasks) > 0:

    task = tq.pop()

    if task is not None:
        if not bot.has_crawled(task.submission.id):
            p = Process(target=execute_task, args={task.submission})
            p.start()
            print("Started process for " + task.submission.title)
        else:
            print("Already crawled " + task.submission)






