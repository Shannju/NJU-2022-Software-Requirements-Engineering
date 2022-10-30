import scrapy

from Spider1.items import Spider1Item
import csv

class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    
    def start_requests(self):
        _url = 'https://stackoverflow.com/questions/tagged/ide?tab=newest&page={}&pagesize=15'
        urls=[]
        for i in range(1,50):
            urls.append(_url.format(i))
            
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    
    def parse(self, response):
        qlist=response.xpath('//*[@id="questions"]')
        
        for i in qlist.xpath('./div'):
            item=Spider1Item()
            item['id']=i.attrib['id']
            item['question']=i.xpath('div[2]/h3/a/text()').extract()
            item['link']=i.xpath('div[2]/h3/a/@href').extract()
            yield item
            
            
            

