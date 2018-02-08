import pickle
from unittest import TestCase
from crawl_report import ReportBuilder


class ReportBuilderTest(TestCase):

    def setUp(self):
        with open("test_report.pkl", 'rb') as f:
            self.files = pickle.load(f)
        self.report_builder = ReportBuilder(self.files, "https://server.elscione.com/")

    def test_total_size(self):

        result = self.report_builder.get_total_size()

        self.assertEqual(result, 426737457589)

    def test_total_size_formatted(self):
        result = self.report_builder.get_total_size_formatted()

        self.assertEqual(result, "426.74 GB")

    def test_ext_counts(self):

        result = self.report_builder.get_ext_counts()

        self.assertEqual(result["jpg"], 140)
        self.assertEqual(result["zip"], 74)

    def test_ext_sizes(self):

        result = self.report_builder.get_ext_sizes()

        self.assertEqual(result["jpg"], 140972306)
        self.assertEqual(result["zip"], 9367400136)
