
from Scraper.spiders import HashTagCrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys

if __name__ == '__main__':
    #startURL = sys.argv[1]
    startURL="https://www.tiktok.com/tag/lgbt"
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    process.crawl(HashTagCrawlSpider.HashtagCrawlSpider, startURL=startURL, count=3)
    process.start()