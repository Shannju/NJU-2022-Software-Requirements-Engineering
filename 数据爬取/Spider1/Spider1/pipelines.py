# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pandas import DataFrame
import pandas as pd


class Spider1Pipeline:
    def __init__(self):
        self.itemall =DataFrame()
        
    def process_item(self, item, spider):
        info=DataFrame([item['id'],item['question'][0],item['link'][0]]).T
        info.columns=['id','question','link']
        self.itemall=pd.concat([self.itemall,info])
        self.itemall.to_csv('link.csv',encoding='utf-8')
        return item
