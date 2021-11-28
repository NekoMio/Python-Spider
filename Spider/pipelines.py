# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import csv


class SpiderPipeline:
    def open_spider(self, spider):
        try:
            self.file = open('data.csv', 'w', encoding='utf_8_sig')
            self.result = csv.writer(self.file)
            self.result.writerow(['name', 'teacher', 'school', 'student_num'])
        except Exception as e:
            print(e)
    
    def process_item(self, item, spider):
        dict_item = ItemAdapter(item).asdict()
        # self.logger.info(dict_item)
        # print(place)
        self.result.writerow(dict_item.values())
        # self.file.write(json_str)
        return item

    def close_spider(self, spider):
        self.file.close()