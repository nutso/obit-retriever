# -*- coding: utf-8 -*-
import scrapy
import re


class LegacySpider(scrapy.Spider):
    name = 'legacy'
    allowed_domains = ['legacy.com']
        
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
            for date in range(self.date_start, self.date_end + 1):
                url = "http://www.legacy.com/obituaries/" + paper + "/obituary-search.aspx?daterange=0&specificdate=" + str(date) + "&countryid=1&stateid=62&affiliateid=" + str(self.newspapers[paper]["affiliateid"])
                request = scrapy.Request(url=url, callback=self.parse)
                request.meta['date'] = date
                request.meta['newspaper'] = paper
                yield request
    
    # Parse an obituary date index page (list of all obits for a given date)
    # 'Clicks' on each obituary title and hands off processing to parse_obit
    def parse(self, response):
        # Displaying x of y Results
        expected_result_count = response.css(".InlineTotalCountText::text").extract_first()
        matches = re.search("Displaying \d* out of (\d*) Results", expected_result_count) # TODO case-insensitive
        if matches:
            expected_result_count = int(matches.group(1))
            print "Expecting " + str(expected_result_count) + " matches"
        else:
            print "Could not extract expected matches! " # TODO print as error
            print expected_result_count
            expected_result_count = None
        
        print response.body
        
        actual_result_count = 0
        for obit in response.css(".obitName"):
            print "obit!!!!"
            print obit
            actual_result_count += 1
            yield response.follow(obit.css("a::attr(href)"), callback=self.parse_obit)        
        
        if(expected_result_count != None and expected_result_count != actual_result_count):
            print "Did not collect all obituaries! Expected " + str(expected_result_count) + " but captured " + str(actual_result_count)

    # Parse a single obituary/article page
    def parse_obit(self, response):
        print "got date ? " + str(response.meta["date"])
        print "got paper ? " + response.meta["newspaper"]
        
