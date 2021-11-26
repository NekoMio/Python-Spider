# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json


class SpiderPipeline:
    def open_spider(self, spider):
        try:
            self.file = open('data.json', 'w', encoding='utf-8')
            self.result = {'海淀': [], '东城': [], '西城': [], '朝阳': []}
        except Exception as e:
            print(e)
    
    def process_item(self, item, spider):
        dict_item = ItemAdapter(item).asdict()
        # self.logger.info(dict_item)
        place = dict_item['place']
        # print(place)
        dict_item.pop('place')
        self.result[place].append(dict_item)
        # self.file.write(json_str)
        return item

    def close_spider(self, spider):
        self.file.write(json.dumps(self.result, ensure_ascii=False, indent=4, separators=(',', ': ')))
        self.file.close()