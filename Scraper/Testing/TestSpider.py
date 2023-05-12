import unittest
from datetime import datetime

from Scraper.Testing.FakeResponses import Response
from Scraper.spiders import HashTagCrawlSpider
import os


# Stackoverflow entry related to this Test : https://stackoverflow.com/questions/6456304/scrapy-unit-testing/12741030#12741030
class TestHashTagSpider(unittest.TestCase):
    def setUp(self):
        self.spider = HashTagCrawlSpider.HashtagCrawlSpider()
        fakeResponse = Response.fake_response_from_file('fakeHtmls/example_video.html')
        self.results = list(self.spider.parse_video(fakeResponse))[14]


    def test_item_results_exist(self):
        self.assertIsNotNone(self.results["userScreenname"])
        self.assertIsNotNone(self.results["username"])
        self.assertIsNotNone(self.results["description"])
        self.assertIsNotNone(self.results["video_url"])
        self.assertIsNotNone(self.results["hashtags"])
        self.assertIsNotNone(self.results["nrLikes"])
        self.assertIsNotNone(self.results["nrComments"])
        self.assertIsNotNone(self.results["nrForwarded"])
        self.assertIsNotNone(self.results["date"])
        self.assertIsNotNone(self.results["music"])



    def test_item_results_content(self):
        self.assertEqual(self.results["userScreenname"],"itstinacolada")
        self.assertEqual(self.results["username"], "tina colada")
        self.assertEqual(self.results["description"], "no idea how to feel rn")
        self.assertEqual(self.results["video_url"], "http://www.example.com")
        self.assertEqual(self.results["hashtags"], ["scifi", "timetravel", "shifting", "shiftingrealities", "alternateuniverse",  "doctorwho",  "timetraveler",  "timetravelerswife", "glee",  "foryou",  "snl",  "comedy"])
        self.assertEqual(self.results["nrLikes"], 4700000)
        self.assertEqual(self.results["nrComments"], 64200)
        self.assertEqual(self.results["nrForwarded"],53600 )
        self.assertEqual(self.results["date"], datetime.strptime("2022-1-9", '%Y-%m-%d').date())
        self.assertEqual(self.results["music"], "original sound - tina colada")








