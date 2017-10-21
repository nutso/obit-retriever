# -*- coding: utf-8 -*-
import scrapy


class LegacySpider(scrapy.Spider):
    name = 'legacy'
    allowed_domains = ['legacy.com']
    
    date = "20140609" # TODO
    
    newspapers = {
        'htrnews': {
            'name': "Manitowoc Herald Times Reporter",
            'affiliateid': 2552
        },
        'sheboyganpress': {
            'name': "Sheboygan Press",
            'affiliateid': 2556
        }
    }
    
    def __init__(self, date_start=None, date_end=None, *args, **kwargs):
        super(LegacySpider, self).__init__(*args, **kwargs)
        self.date_start = int(date_start)
        self.date_end = int(date_end)
        # TODO error checking on parameters - required, format

    def start_requests(self):
        for paper in self.newspapers:
            for date in range(self.date_start, self.date_end):
                url = "http://www.legacy.com/obituaries/" + paper + "/obituary-search.aspx?daterange=0&specificdate=" + str(date) + "&countryid=1&stateid=62&affiliateid=" + str(self.newspapers[paper]["affiliateid"])
                yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        pass
