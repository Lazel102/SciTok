# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from neomodel import DoesNotExist
from scrapy import signals
import random

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.exceptions import DropItem, IgnoreRequest

from Scraper import neo4jConfig

user_agent_list = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

class RotateUserAgentsMiddleware:
    def process_request(self, request, spider):
        user_agent = random.choice (user_agent_list)
        request.headers["User-Agent"] =user_agent





class IgnoreDuplicates:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        if "video" in request.url :
            try:
                post = neo4jConfig.Post.nodes.filter(video_url=request.url).first()
            except:
                return None
            raise IgnoreRequest()

        return None




