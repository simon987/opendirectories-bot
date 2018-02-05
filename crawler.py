import requests
from parser import NginxParser, ApacheParser
from reports import ReportSaver, ReportBuilder

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}


class Crawler:

    def __init__(self, url):
        self.parser = NginxParser()
        self.files = []
        self.base_url = url

    def crawl(self, address=None):

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


c = Crawler("http://dl.upload8.in/files/Serial/Altered%20Carbon/")
c.crawl()
c.store_report("000002")
