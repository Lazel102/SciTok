# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime
from datetime import timedelta

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def parseNumber(stringNumber):
    if stringNumber[-1]=="K":
        stringNumber=stringNumber[:-1]+"00"
    if stringNumber[-1]=="M":
        stringNumber=stringNumber[:-1]+"00000"
    if "." in stringNumber:
        stringNumber=stringNumber.replace(".","")
    else:
        stringNumber+="0"
    return int(stringNumber)
def parse_description(value):
    return value.lstrip().rstrip()

def parseHashtags(htg):
    htgs_new = htg.split("/")[-1]
    return htgs_new
def toDate(dateString):
    for i in range(8):
        if str(i)+"d" in dateString:
            return datetime.today()- timedelta(days=int(i))

    datetime_object = datetime.strptime(dateString, '%Y-%m-%d').date()
    return datetime_object
class TikTokItem(scrapy.Item):
    # define the fields for your item here like:



    #TODO :Implement ITEMLOADER  as suggested in  : https://www.youtube.com/watch?v=wyE4oDxScfE
    userScreenname  = scrapy.Field(input_processor= MapCompose(remove_tags),output_processor = TakeFirst())
    username        = scrapy.Field(input_processor= MapCompose(remove_tags),output_processor = TakeFirst())
    description     = scrapy.Field(input_processor= MapCompose(remove_tags,parse_description),output_processor = TakeFirst())
    video_url       = scrapy.Field(input_processor= MapCompose(remove_tags),output_processor = TakeFirst())
    hashtags        = scrapy.Field(input_processor= MapCompose(parseHashtags))
    nrLikes         = scrapy.Field(input_processor= MapCompose(parseNumber),output_processor = TakeFirst())
    nrComments      = scrapy.Field(input_processor= MapCompose(parseNumber),output_processor = TakeFirst())
    nrForwarded     = scrapy.Field(input_processor= MapCompose(parseNumber),output_processor = TakeFirst())
    date            = scrapy.Field(input_processor= MapCompose(remove_tags,toDate),output_processor = TakeFirst())
    music           = scrapy.Field(input_processor= MapCompose(remove_tags),output_processor = TakeFirst())
    musicLink       = scrapy.Field(input_processor= MapCompose(remove_tags),output_processor = TakeFirst())
    collectionTime  = scrapy.Field(input_processor= MapCompose(remove_tags),output_processor = TakeFirst())



