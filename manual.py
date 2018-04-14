import sys
from crawler import Crawler
from crawl_report import ReportBuilder
from reddit_bot import CommentBuilder

if __name__ == "__main__":

    if len(sys.argv) > 1:

        command = sys.argv[1]

        if command == "crawl":
            if len(sys.argv) > 2:
                url = sys.argv[2]

                c = Crawler(url, True)
                c.crawl()

                print("Done")
                r = ReportBuilder(c.files, url)
                print(r.get_total_size_formatted())

        if command == "mkreport":
            if len(sys.argv) > 3:
                url = sys.argv[2]
                report_id = sys.argv[3]

                c = Crawler(url, True)
                c.crawl()

                print("Done")
                r = ReportBuilder(c.files, url)
                print(r.get_total_size_formatted())

                c.store_report(report_id, "")

        if command == "getcomment":
            if len(sys.argv) > 3:
                url = sys.argv[2]
                report_id = sys.argv[3]

                c = Crawler(url, True)
                c.crawl()

                print("Done")
                r = ReportBuilder(c.files, url)
                print(r.get_total_size_formatted())

                com_buider = CommentBuilder(ReportBuilder(c.files, c.base_url), url, report_id)
                print(com_buider.get_comment())


    else:
        print("Invalid argument count")