import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
#https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time/14132912#14132912
from Scraper.items import TikTokItem
from scrapy.loader import ItemLoader
from scrapy.http import Request
from Scraper import neo4jConfig
from datetime import datetime
import re

#https://www.tiktok.com/tag/shifting
#https://www.tiktok.com/@itstinacolada/video/7051319079558270214
#https://www.tiktok.com/@itstinacolada
#https://www.tiktok.com/music/original-sound-7187811741688974126

class HashtagCrawlSpider(CrawlSpider):

    name = 'HashTagCrawlSpider'
    allowed_domains = ['tiktok.com']
    rules = (
        Rule(LinkExtractor(allow='/video'),callback="parse_video"),
        Rule(LinkExtractor(allow='/music')),

    )
    start_urls = ['http://www.tiktok.com/']

    def start_requests(self):
        yield scrapy.Request(self.startURL)
    def parse_video(self,response):
        """
        This function parses a sample response. Some contracts are mingledwith this docstring.
        @url http://www.tiktok.com/tag/shifting
        @returns items 1 1
        """
        itemLoader =ItemLoader(item=TikTokItem(),selector=response)
        consumeData = response.css("strong.edu4zum2::text").getall()
        username = response.css('span.tiktok-1xccqfx-SpanNickName.e17fzhrb1::text').get()
        date = self.extractDate(response.css("span.evv7pft3").get())
        music = self.extractMusic(response)
        musicLink = "http://www.tiktok.com/"+ response.css("h4.epjbyn0 a").attrib["href"]

        itemLoader.add_css("userScreenname","span.e17fzhrb1")
        itemLoader.add_value("username", username)
        itemLoader.add_css("description", "span.efbd9f0")
        itemLoader.add_value("video_url",response.url)
        itemLoader.add_css("hashtags", "strong.ejg0rhn2::text")
        itemLoader.add_value("nrLikes", self.parseListData(consumeData,0))
        itemLoader.add_value("nrComments",self.parseListData(consumeData,1))
        itemLoader.add_value("nrForwarded", self.parseListData(consumeData,2))
        itemLoader.add_value("date", date)
        itemLoader.add_value("music", music)
        itemLoader.add_value("musicLink",musicLink)
        """
        consumeData     = response.css("strong.edu4zum2::text").getall()
        personalDetails = response.css("span.e17fzhrb2 span::text").getall()
        item["userScreenname"] = response.css("span.e17fzhrb1::text").get()
        item["username"]    = self.parseListData(0,personalDetails)
        item["description"] = response.css("span.efbd9f0::text").get()
        item["video_url"]   = response.url
        item["hashtags"]    = response.css("a.ejg0rhn4::attr(href)").extract()
        item["nrLikes"]     =  self.parseListData(0,consumeData)
        item["nrComments"]  = self.parseListData(1,consumeData)
        item["nrForwarded"] = self.parseListData(2,consumeData)
        item["date"]        = self.parseListData(2,personalDetails)
        item["music"]       = response.css("h4.epjbyn0 a::text").get()
         """
        item =itemLoader.load_item()


        for tag in item["hashtags"]:
            if tag[0]=="@":
                yield Request("http://www.tiktok.com/"+tag)
            else:
                yield Request("http://www.tiktok.com/tag/"+tag)
        yield Request("http://www.tiktok.com/"+"@"+item["userScreenname"])
        yield Request(musicLink)
        yield item

    def extractDate(self, dateString):
        date = re.search(r'<span>(\d+-\d+)</span>', dateString).group(1)
        return date
    def extractMusic(self, res):
        for pos in ["h4.epjbyn0 div::text","h4.epjbyn0 a::text"]:
            music = res.css(pos).get()
            if music is not None:
                return music



    def parseListData(self,list,index ):
        try:
            return list[index]
        except:
            return "NA"


