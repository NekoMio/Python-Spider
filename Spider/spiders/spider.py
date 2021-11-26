import scrapy
from Spider.items import LianjiaItem

Pinyin_to_City = {
    "dongcheng": "东城",
    "xicheng": "西城",
    "chaoyang": "朝阳",
    "haidian": "海淀",
}

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['bj.lianjia.com']
    start_urls = ['https://bj.lianjia.com/ershoufang/dongcheng/',
                  'https://bj.lianjia.com/ershoufang/xicheng/',
                  'https://bj.lianjia.com/ershoufang/chaoyang/',
                  'https://bj.lianjia.com/ershoufang/haidian/',
                 ]
    
    def parse(self, response, **kwargs):
        self.logger.info('A response from %s just arrived!, args: %s', response.url, kwargs)
        
            
        item = LianjiaItem()
        
        for each in response.xpath("/html/body/div[4]/div[1]/ul/li/div[1]"):
            # self.logger.info('each: %s', each)
            item['name'] = each.xpath("div[2]/div/a[1]/text()").get().strip()
            # self.logger.info('name: %s', item['name'])
            item['price'] = each.xpath("div[6]/div[1]/span/text()").get().strip() + each.xpath("div[6]/div[1]/i[2]/text()").get().strip()
            
            item['area'] = each.xpath("div[3]/div/text()").get().split('|')[1].strip()
            # self.logger.info('area: %s', item['area'])
            item['unit_price'] = each.xpath("div[6]/div[2]/span/text()").get().strip()
            item['place'] = Pinyin_to_City[response.url.split('/')[4]]
            if (item['name'] and item['price'] and item['area'] and item['unit_price']):
                self.logger.info('%s %s %s %s', item['name'], item['price'], item['area'], item['unit_price'])
                yield item
        
        nowpage_id = kwargs.get('page', 1)
        if (nowpage_id == 1):
            next_page = response.url + 'pg2' + '/'
        else:
            next_page = response.url.replace('pg' + str(nowpage_id), 'pg' + str(nowpage_id + 1))
        
        self.logger.info('next_page: %s', next_page)
        
        
        
        if (nowpage_id == 5):
            pass
        else:
            yield response.follow(next_page, callback=self.parse, cb_kwargs={'page': nowpage_id+1})
        
