import os
import re
from urllib.parse import urljoin

import humanfriendly
from bs4 import BeautifulSoup


class PageParser:

    def __init__(self):
        self.col_start = None
        self.col_end = None
        self.size_unknown = True

    def get_links(self, text: str, base_url: str):
        raise NotImplementedError()

    @staticmethod
    def get_size_columns(cols):

        for i in range(len(cols)):

            if i == len(cols) - 1:
                try:
                    humanfriendly.parse_size(cols[i])
                    return tuple([i, i])
                except humanfriendly.InvalidSize:
                    return None

            try:
                humanfriendly.parse_size(cols[i] + cols[i + 1])
                return tuple([i, i + 1])
            except humanfriendly.InvalidSize:
                try:
                    humanfriendly.parse_size(cols[i])
                    return tuple([i, i])
                except humanfriendly.InvalidSize:
                    continue

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

        if link.endswith("/") or link.startswith("?"):
            return "d"
        return "f"


    @staticmethod
    def clean_page(text):
        text = text.replace("<A", "<a")
        text = text.replace("</A", "</a")
        # text = text.replace("&", "&amp;")
        text = text.replace("<hr>", "")

        return text

    def get_size(self, cols):

        # Figure out which column(s) is the size one
        size_cols = self.get_size_columns(cols)
        if size_cols is not None:
            col_start, col_end = size_cols
            self.size_unknown = False

            size_human = cols[col_start] if col_start == col_end else cols[col_start] + cols[col_end]

            try:
                size = humanfriendly.parse_size(size_human)
            except humanfriendly.InvalidSize:
                size = 0
        else:
            size = 0

        return size


class NginxParser(PageParser):
    def get_links(self, text, base_url: str):

        links = dict()

        text = self.clean_page(text)

        soup = BeautifulSoup(text, "html.parser")

        for link in soup.find("pre").find_all("a"):

            parsed_link = self.parse_link(link, text, base_url)
            if parsed_link is not None:
                links[parsed_link[0]] = parsed_link[1]

        return links

    def page_is_valid(self, text):
        # Handle weird character formats and tag names
        text = self.clean_page(text)

        soup = BeautifulSoup(text, "html.parser")

        if soup.find("pre") is None:
            return False

        # try to parse a single link
        for link in soup.find("pre").find_all("a"):
            if PageParser.should_save_link(link.text):
                if self.parse_link(link, text, "") is None:
                    return False

        return True

    def parse_link(self, link, text, base_url):

        try:
            if PageParser.should_save_link(link.text):
                target = link.get("href")
                full_link = urljoin(base_url, target)
                file_type = PageParser.file_type(target)

                if file_type == "f":
                    extension = os.path.splitext(full_link)[1].strip(".")

                    # Parse size
                    target_index = text.find("</a", text.find(target))
                    date_and_size = text[target_index:text.find("<a", target_index)]

                    cols = re.split("\s+", date_and_size)
                    size = self.get_size(cols)

                    return target, dict(link=full_link, size=size, ext=extension, type=file_type)
                else:
                    return target, dict(link=full_link, type=file_type)
        except Exception as e:
            print("Couldn't parse link " + link.get("href") + str(e))
            raise e

        return None


class ApacheParser(PageParser):

    def get_links(self, text, base_url: str):

        links = dict()

        # Handle weird character formats and tag names
        text = self.clean_page(text)

        soup = BeautifulSoup(text, "html.parser")

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
                    file_type = PageParser.file_type(target)
                    full_link = urljoin(base_url, target)

                    if file_type == "f":
                        extension = os.path.splitext(full_link)[1].strip(".")

                        cols = row.find_all("td")
                        for i in range(len(cols)):
                            cols[i] = cols[i].string if cols[i].string is not None else "-"
                        size = self.get_size(cols)

                        links[target] = dict(link=full_link, size=size, ext=extension, type=file_type)
                    else:
                        links[target] = dict(link=full_link, type=file_type)
        else:

            for link in soup.find_all("a"):

                if PageParser.should_save_link(link.text):

                    target = link.get("href")
                    full_link = urljoin(base_url, target)
                    file_type = PageParser.file_type(target)

                    if file_type == "f":
                        extension = os.path.splitext(full_link)[1].strip(".")

                        target_index = text.find("</a", text.find(target))
                        date_and_size = text[target_index:text.find("<a", target_index)]  #  in some cases we,re looking for </pre instead
                        date_and_size = text[target_index:text.find("</pre", target_index)] if text.find("<a", target_index) == -1 else date_and_size

                        cols = re.split("\s+", date_and_size)
                        size = self.get_size(cols)

                        links[target] = dict(link=full_link, size=size, ext=extension, type=file_type)
                    else:
                        links[target] = dict(link=full_link, type=file_type)

        return links

    def page_is_valid(self, text):

        try:
            self.get_links(text, "")
            return True
        except Exception as e:
            print("This is not recognised Apache open directory: " + str(e))




