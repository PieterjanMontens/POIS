from scrapy.spider import Spider
from scrapy.selector import Selector
from POIS.items import PoisItem
import re

class RvsSpider(Spider):
    name = "rvs"
    allowed_domains = ["raadvst-consetat.be"]
    start_urls = ["http://www.raadvst-consetat.be/?lang=fr&page=hearing_page1"]


    def parse(self, response):
        hxs = Selector(response)
        AudMask = '^G/A (?P<role>[0-9\.]{1,})/(?P<room>[VIX]{1,})-(?P<room_number>[0-9]*), (?P<applicant>[^(]+?)(\((?P<app_lawyer>[^)]+)\))? contre (?P<opposer>[^(]+?)(\((?P<opp_lawyer>[^)]+)\))?$'
        AudReObj = re.compile(AudMask)
        items = []

        RawDate   = hxs.xpath("//h4/text()").extract()[0]
        print RawDate
        DateMatch = re.match('[a-zA-Z ]+([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})$',RawDate)
        DateDay   = DateMatch.group(1)
        DateMonth = DateMatch.group(2)
        DateYear  = DateMatch.group(3)


        #TODO: get all times, loop on them.
        Times = hxs.xpath("//h5/text()").re(re.compile('^[0-9]+:[0-9]+$'))
        for Time in Times:
            #Audiences = hxs.xpath("//h5[text()='{0}']/following-sibling::ul[1]/li".format(Time))
            Audiences = hxs.xpath("//h6[preceding-sibling::h5[1][text()='{0}']]/following-sibling::ul[1]/li".format(Time))

        #Audiences = hxs.xpath("//li")
            for Audience in Audiences:
                item = PoisItem()
                AudList = Audience.xpath("text()").extract()
                if len(AudList) == 0:
                    continue

                print AudList[0]
                Match   = re.match(AudReObj,AudList[0])
                if Match:
                    item ['date'] = "{0}/{1}/{2}".format(DateDay,DateMonth,DateYear)
                    item ['time'] = Time
                    item ['role'] = Match.group('role')
                    item ['room'] = Match.group('room')
                    item ['room_number'] = Match.group('room_number')
                    item ['app_party'] = Match.group('applicant')
                    if Match.group('app_lawyer'):
                        item ['app_lawyer'] = Match.group('app_lawyer').replace(', avocat','').replace(', advocaat','')

                    item ['opp_party'] = Match.group('opposer')
                    if Match.group('opp_lawyer'):
                        item ['opp_lawyer'] = Match.group('opp_lawyer').replace(', avocat','').replace(', advocaat','')

                    items.append(item)

        return items
