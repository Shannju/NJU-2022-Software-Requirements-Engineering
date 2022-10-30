# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pandas import DataFrame
import pandas as pd


class Spider2Pipeline:
    def __init__(self):
        self.itemall =DataFrame()
        
    def process_item(self, item, spider):
        que=item['question'].replace("\n","")
        que=item['question'].replace("  ","")
        link=item['link'].replace("\n","")
        link=item['link'].replace("  ","")
        ans=item['answer'].replace("\n","")
        ans=item['answer'].replace("  ","")
        info=DataFrame([que,link,ans]).T
        info.columns=['question','link','answer']
        self.itemall=pd.concat([self.itemall,info])
        self.itemall.to_csv('qa.txt',encoding='utf-8')
        return item
