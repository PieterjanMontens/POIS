# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class PoisItem(Item):
    role = Field()
    room = Field()
    room_number = Field()
    app_party  = Field()
    app_lawyer = Field()
    opp_party  = Field()
    opp_lawyer = Field()
    date       = Field()
    time       = Field()
