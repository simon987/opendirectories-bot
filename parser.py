from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import re
import humanfriendly


class PageParser:
    def get_links(self, text: str, base_url: str):
        raise NotImplementedError()

    @staticmethod
    def get_parser_type(headers):
        """Get appropriate parser type for a a server based on its header"""

        server = headers["Server"]

        if server is not None:
            if server == "nginx":
                return NginxParser

    @staticmethod
    def should_save_link(text):
        return text.lower().find("parent directory") == -1 and text != "Name" and text != "Last modified" and \
               text != "Size" and text != "Description " and text != "Description" and text != "../"

    @staticmethod
    def file_type(link):
        return "d" if link.endswith("/") else "f"


class NginxParser(PageParser):
    def get_links(self, text, base_url: str):

        links = dict()
        soup = BeautifulSoup(text, "html.parser")

        # Handle weird character formats and tag names
        text = text.replace("<A", "<a")
        text = text.replace("</A", "</a")
        text = text.replace("&", "&amp;")

        for link in soup.find("pre").find_all("a"):

            if link.text != "../":
                target = link.get("href")
                full_link = urljoin(base_url, target)
                file_type = PageParser.file_type(full_link)

                if file_type == "f":
                    extension = os.path.splitext(full_link)[1].strip(".")

                    # Parse size
                    target_index = text.find("</a", text.find(target))
                    date_and_size = text[target_index:text.find("<a", target_index)]
                    size = humanfriendly.parse_size(re.split("\s+", date_and_size)[3])

                    links[link.text] = dict(link=full_link, size=size, ext=extension, type=file_type)
                else:
                    links[link.text] = dict(link=full_link, type=file_type)

        return links


class ApacheParser(PageParser):

    def __init__(self):
        self.col_start = None
        self.col_end = None
        self.size_unknown = True

    def get_size_columns(self, cols):

        for i in range(len(cols) - 1):
            try:
                humanfriendly.parse_size(cols[i] + cols[i + 1])
                return tuple([i, i + 1])
            except humanfriendly.InvalidSize:
                try:
                    humanfriendly.parse_size(cols[i])
                    return tuple([i, i])
                except humanfriendly.InvalidSize:
                    continue

    def get_links(self, text, base_url: str):

        links = dict()
        soup = BeautifulSoup(text, "html.parser")

        # Handle weird character formats and tag names
        text = text.replace("<A", "<a")
        text = text.replace("</A", "</a")
        text = text.replace("&", "&amp;")



        if soup.find("table"):

            for row in soup.find("table").find_all("tr"):

                if len(row.find_all("th")) > 0:
                    continue

                link = row.find("a")

                if link is None:
                    # Exited directory listing
                    return links
                if PageParser.should_save_link(link.text):

                    target = link.get("href")
                    full_link = urljoin(base_url, target)
                    file_type = PageParser.file_type(full_link)

                    if file_type == "f":
                        extension = os.path.splitext(full_link)[1].strip(".")

                        cols = row.find_all("td")
                        for i in range(len(cols)):
                            cols[i] = cols[i].string if cols[i].string is not None else ""
                        size = self.get_size(cols)

                        links[link.text] = dict(link=full_link, size=size, ext=extension, type=file_type)
                    else:
                        links[link.text] = dict(link=full_link, type=file_type)
        else:

            for link in soup.find_all("a"):

                if PageParser.should_save_link(link.text):

                    target = link.get("href")
                    full_link = urljoin(base_url, target)
                    file_type = PageParser.file_type(full_link)

                    if file_type == "f":
                        extension = os.path.splitext(full_link)[1].strip(".")

                        target_index = text.find("</a", text.find(target))
                        date_and_size = text[target_index:text.find("<a", target_index)]

                        cols = re.split("\s+", date_and_size)
                        size = self.get_size(cols)

                        links[link.text] = dict(link=full_link, size=size, ext=extension, type=file_type)
                    else:
                        links[link.text] = dict(link=full_link, type=file_type)

        return links

    def get_size(self, cols):
        if self.col_start is None:
            # Figure out which column(s) is the size one
            size_cols = self.get_size_columns(cols)
            if size_cols is not None:
                self.col_start, self.col_end = size_cols
                self.size_unknown = False

        if self.size_unknown:
            size = 0
        else:
            size_human = cols[self.col_start] if self.col_start == self.col_end else cols[self.col_start] + cols[self.col_end]
            size = humanfriendly.parse_size(size_human)
        return size


