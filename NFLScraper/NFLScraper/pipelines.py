# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#import csv
#
#class CsvWriterPipeline(object):
#    def __init__(self):
#        self.csvwriter = None 
#        self.headers_written = False
#
#    def open_spider(self, spider):
#        self.csvwriter = csv.writer(open('nfl_scraped_data.csv', 'wb'))
#    
#    def process_item(self, item, spider):
#        if not self.headers_written:
#           header_keys = item.fields.keys()
#           self.csvwriter.writerow(header_keys)
#           self.headers_written = True  
#        
#        self.csvwriter.writeorw(
#            [item['year'][0],
#            item['week'][0],
#            item['h_team'][0],
#            item['a_team'][0],
#            item['h_score'][0],
#            item['a_score'][0],
#            item['line'][0],
#            item['over'][0],
#            item['temp'][0],
#            item['h_1dcv'][0],
#            item['a_1dcv'][0],
#            item['h_rtot'][0],
#            item['a_rtot'][0],
#            item['h_ratt'][0],
#            item['a_ratt'][0],
#            item['h_ryds'][0],
#            item['a_ryds'][0],
#            item['h_sack'][0],
#            item['a_sack'][0],
#            item['h_ptot'][0],
#            item['a_ptot'][0],
#            item['h_npyd'][0],
#            item['a_npyd'][0],
#            item['h_turn'][0],
#            item['a_turn'][0],
#            item['h_peny'][0],
#            item['a_peny'][0],
#            item['h_3dcv'][0], 
#            item['h_3dcv'][0],
#            item['h_3att'][0], 
#            item['h_3att'][0],
#            item['h_poss'][0],
#            item['a_poss'][0]])
#        return item
