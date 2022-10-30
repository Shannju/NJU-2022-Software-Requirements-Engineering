import scrapy
import csv

import twisted
from Spider2.items import Spider2Item
from time import sleep
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
# from threads import error()
import requests

class ItcastSpider(scrapy.Spider):
    name = 'itcast1'
    
    def start_requests(self): 
        urls=[]
        csv_reader = csv.reader(open("link.csv"))
        for line in csv_reader:
            if(line[3][-1]=="\n" or line[3][-1]=="\r"): 
                urls.append('https://stackoverflow.com'+line[3][:-1])
            else:
                urls.append('https://stackoverflow.com'+line[3])
        proxy = ["http://207.236.12.190:80",
                "http://51.75.165.14:80",
                "http://103.172.116.231:80",
                "http://104.148.36.10:80"]
        cnt=0
        for url in urls:
            sleep(0.1)
            yield scrapy.Request(url=url,callback=self.parse,
                                    #  errback=self.errback_httpbin,
                                     dont_filter=True,
                                     meta={"proxy": proxy[cnt]}
                                     )
            cnt=(cnt+1)%4
            
    
    def parse(self, response):
        sel1 = response.xpath('//*[@class="postcell post-layout--right"]/div[1]')  
        item = Spider2Item()
        pro = sel1.xpath(
            'string(.)').extract()[0]
        pro.replace("\r","")
        pro.replace("\n"," ")
        item['question'] = pro
        #多个回答
        sel2s = response.xpath('//*[@class="answercell post-layout--right"]/div[1]')
        sol = sel2s[0].xpath(
            'string(.)').extract()[0]
        if(len(sel2s)) >= 2:
            for i in range(1, len(sel2s)):
                sol = sol + "..."
                sol = sol + sel2s[i].xpath(
                'string(.)').extract()[0]
        sol.replace("\r","")
        sol.replace("\n"," ")
        item['answer'] = sol
        item['link']=response.url
        yield item
        
    def errback_httpbin(self, failure):
        # log all failures
        pass
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
