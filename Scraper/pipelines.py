# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
import os
# Solve this here https://realpython.com/lessons/uninstall-packages/ next time
from neomodel import config
from Scraper import neo4jConfig

class ScraperPipeline:
    def __init__(self):

        db_host = os.environ.get("DB_HOST")
        authentification = os.environ.get("NEO4J_AUTH").split("/")
        config.DATABASE_URL = f'bolt://{authentification[0]}:{authentification[1]}@{db_host}:7687'

    def process_item(self, item, spider):
        post = neo4jConfig.Post.get_or_create({"video_url": item["video_url"]})[0]
        post.description = item.get("description","NA")
        post.nrComments = item.get("nrComments","NA")
        post.nrLikes = item.get("nrLikes","NA")
        post.nrForwarded = item.get("nrForwarded","NA")
        post.date = item.get("date","NA")
        post.save()

        user = neo4jConfig.User.get_or_create({"userScreenname": item["userScreenname"]})[0]
        user.username = item.get("username","NA")
        user.save()
        user.posts.connect(post)

        music = neo4jConfig.Music.get_or_create({"title": item["music"]})[0]
        music.url = item.get("musicLink","NA")
        music.save()
        post.music.connect(music)

        for h in item.get("hashtags",[]):
            if h[0] == "@":
                mentionedUser = neo4jConfig.User.get_or_create({"userScreenname": h[1:]})[0]
                post.mentionedUser.connect(mentionedUser)
            else:
                hashtag = neo4jConfig.Hashtag.get_or_create({"name": h})[0]
                hashtag.save()
                post.hashtags.connect(hashtag)

        return item
