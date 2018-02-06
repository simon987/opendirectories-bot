import humanfriendly
import datetime
import json


class ReportBuilder:

    def __init__(self, files: list, base_url: str):
        self.files = files
        self.report_time = datetime.datetime.today()
        self.base_url = base_url

    def get_total_size(self):
        size = 0

        for f in self.files:
            size += f["size"]

        return size

    def get_total_size_formatted(self):

        size = self.get_total_size()

        if size == 0:
            return "Unknown (or empty)"

        return humanfriendly.format_size(size, True) + " (" + str(size) + " bytes)"

    def get_ext_counts(self):

        ext_counts = dict()

        for f in self.files:

            ext = f["ext"].lower()

            if ext in ext_counts:
                ext_counts[ext] += 1
            else:
                ext_counts[ext] = 1

        return ext_counts

    def get_ext_sizes(self):

        ext_sizes = dict()

        for f in self.files:

            ext = f["ext"].lower()

            if ext in ext_sizes:
                ext_sizes[ext] += f["size"]
            else:
                ext_sizes[ext] = f["size"]

        return ext_sizes

    def get_ext_sizes_formatted(self):

        ext_sizes = self.get_ext_sizes()

        for ext in ext_sizes:
            ext_sizes[ext] = humanfriendly.format_size(ext_sizes[ext])
        return ext_sizes


class ReportSaver:

    def __init__(self, files, builder: ReportBuilder):
        self.files = files
        self.builder = builder

    def to_json(self):

        out = dict()

        out["files"] = []

        base_url_len = len(self.builder.base_url)

        for f in self.files:
            stripped_url = f["link"][base_url_len-1:]
            out["files"].append(stripped_url)

        out["total_size"] = self.builder.get_total_size()
        out["base_url"] = self.builder.base_url
        out["total_size_formatted"] = self.builder.get_total_size_formatted()
        out["ext_count"] = self.builder.get_ext_counts()
        out["ext_sizes"] = self.builder.get_ext_sizes()
        out["ext_sizes_formatted"] = self.builder.get_ext_sizes_formatted()
        out["report_time"] = str(self.builder.report_time)
        out["total_count"] = len(self.builder.files)

        return json.dumps(out)

    def to_json_chart(self):

        out = dict()

        out["total_size"] = self.builder.get_total_size()
        out["base_url"] = self.builder.base_url
        out["ext_count"] = self.builder.get_ext_counts()
        out["ext_sizes"] = self.builder.get_ext_sizes()
        out["report_time"] = str(self.builder.report_time)
        out["total_count"] = len(self.builder.files)

        return json.dumps(out)

    def to_link_list(self):

        out = ""

        for f in self.files:
            out += f["link"] + "\n"

        out = out[:-1]  # Remove trailing newline

        return out

