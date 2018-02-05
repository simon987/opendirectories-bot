import pickle
from unittest import TestCase
from reports import ReportSaver, ReportBuilder
import json


class ReportSaverTest(TestCase):

    def setUp(self):
        with open("test_report.pkl", 'rb') as f:
            self.files = pickle.load(f)

        self.report_saver = ReportSaver(self.files, ReportBuilder(self.files, "https://server.elscione.com/"))

        with open("test_report.json", 'r') as f:
            self.expected_json = f.read()

        with open("test_report_chart.json", 'r') as f:
            self.expected_json_chart = f.read()

    def test_to_json(self):

        result = self.report_saver.to_json()

        self.assertEqual(json.loads(result)["total_size"], 426737457589)

    def test_to_link_list(self):
        result = self.report_saver.to_link_list()
        self.assertEqual(len(result.split("\n")), 2905)

    def test_to_json_chart(self):

        result = self.report_saver.to_json_chart()
        self.assertEqual(json.loads(result)["total_size"], 426737457589)
        self.assertEqual(len(json.loads(result)["ext_sizes"]), 39)

