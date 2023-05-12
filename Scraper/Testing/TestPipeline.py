import datetime
import os
import unittest

import neomodel
from neomodel import db, DoesNotExist
import pytest

from Scraper import neo4jConfig
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from Scraper.pipelines import ScraperPipeline

class TestPipeline(unittest.TestCase):

    def test_scraper_pipeline(self):
        pipeline = ScraperPipeline()

        # Create a test item
        test_item = {
            "description": "Test description",
            "video_url": "https://example.com",
            "nrComments": 10,
            "nrLikes": 20,
            "nrForwarded": 5,
            "date": datetime.datetime.strptime("2023-02-20", '%Y-%m-%d').date(),
            "username": "Test User",
            "userScreenname": "testuser",
            "music": "Test Music",
            "musicLink": "https://example.com/music",
            "hashtags": ["#test", "@mentioneduser"]
        }

        # Process the test item
        pipeline.process_item(test_item, None)

        # Verify that the test item was processed correctly
        post = neo4jConfig.Post.nodes.get(video_url=test_item["video_url"])
        assert post.description == test_item["description"]
        assert post.nrComments == test_item["nrComments"]
        assert post.nrLikes == test_item["nrLikes"]
        assert post.nrForwarded == test_item["nrForwarded"]
        assert isinstance(post.date,datetime.date)
        assert isinstance(post.created,datetime.date)
        user = neo4jConfig.User.nodes.get(userScreenname=test_item["userScreenname"])
        assert user.username == test_item["username"]
        music = neo4jConfig.Music.nodes.get(title=test_item["music"])
        assert music.url == test_item["musicLink"]
        hashtags = [h.name for h in post.hashtags.all()]
        assert hashtags == ["#test"]
        mentioned_users = [u.userScreenname for u in post.mentionedUser.all()]
        assert mentioned_users == ["mentioneduser"]

        # Delete the test item from the database
        for h in post.hashtags.all():
            h.delete()
        post.delete()
        music.delete()
        user.delete()




        # Verify that the test item was deleted
        with pytest.raises(DoesNotExist):
            neo4jConfig.Post.nodes.get(video_url=test_item["video_url"])
        with pytest.raises(DoesNotExist):
            neo4jConfig.User.nodes.get(userScreenname=test_item["userScreenname"])
        with pytest.raises(DoesNotExist):
            neo4jConfig.Music.nodes.get(title=test_item["music"])
        with pytest.raises(DoesNotExist):
            neo4jConfig.Hashtag.nodes.get(name="#test")
        with pytest.raises(DoesNotExist):
            neo4jConfig.Hashtag.nodes.get(name="@mentioneduser")



if __name__ == '__main__':
    unittest.main()


