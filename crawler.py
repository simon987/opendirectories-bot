import requests
from parser import NginxParser, ApacheParser
from reports import ReportSaver, ReportBuilder


class Crawler:

    def __init__(self, url, test_url):
        self.files = []
        self.base_url = url

        if url.startswith("http"):
            if test_url:
                # Test url
                try:
                    r = requests.get(self.base_url, timeout=10)  # todo change to 30

                    if r.status_code == 200:
                        self.parser = self.guess_parser(r.text, r.headers)()

                        print("Using " + self.parser.__class__.__name__ + " as parser")
                    else:
                        print("Couldn't connect (" + str(r.status_code) + ")")
                        self.parser = None

                except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
                    print("Timed out / Connection refused")
                    self.parser = None
            else:
                print("Using ApacheParser by default because test_url was set to False")
                self.parser = ApacheParser()  # Default parser
        else:
            print("Invalid Schema")
            self.parser = None

    @staticmethod
    def guess_parser(text, headers):

        server = headers["Server"] if "Server" in headers else ""

        # try nginx
        parser = NginxParser()
        if parser.page_is_valid(text):
            return NginxParser

        # Try apache
        parser = ApacheParser()
        if parser.page_is_valid(text):
            return ApacheParser

        return None

    def crawl(self, address=None):

        if self.parser is None:
            return

        if address is None:
            address = self.base_url

        if not address.startswith(self.base_url):
            print("Skipping " + address + " because it does not match " + self.base_url)
            return

        retries = 20
        while retries >= 0:
            try:
                response = requests.get(address, timeout=10)
                break
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                print("Timeout, " + str(retries) + " retries left")
                retries -= 1

        links = self.parser.get_links(response.text, address)

        for k in links:
            if links[k]["type"] == "d":
                print(links[k]["link"])
                self.crawl(links[k]["link"])
            else:
                self.files.append(dict(link=links[k]["link"], size=links[k]["size"], ext=links[k]["ext"]))

    def store_report(self, report_id):
        report_saver = ReportSaver(self.files, ReportBuilder(self.files, self.base_url))

        with open("static/reports/" + report_id + "_chart.json", "w") as f:
            f.write(report_saver.to_json_chart())
        with open("static/reports/" + report_id + ".json", "w") as f:
            f.write(report_saver.to_json())
        with open("static/reports/" + report_id + ".txt", "w") as f:
            f.write(report_saver.to_link_list())


if __name__ == "__main__":
    c = Crawler("http://dl.apkhome.org/", True)
    c.crawl()

    r = ReportBuilder(c.files, "http://dl.apkhome.org/")
    print(r.get_total_size_formatted())

    for f in c.files:
        if f["size"] > 1000000:
            print(f)

    c.store_report("000009")

