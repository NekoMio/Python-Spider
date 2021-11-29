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
    
    def start_requests(self):
        self.logger.info('start_requests')
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, cb_kwargs={'page': 1})
    
    def parse(self, response, **kwargs):
        self.logger.info('A response from %s just arrived!, args: %s', response.url, kwargs)
        
        # base_url = get_base_url(response)
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
        
        next_page = response.xpath("/html/body/div[4]/div[1]/div[7]/div[2]/div/a[last()]/@href").get()
        # 
        self.logger.info('next_page: %s', next_page)
        
        
        if (kwargs.get('page') == 5):
            pass
        else:
            yield response.follow(next_page, callback=self.parse, cb_kwargs={'page': kwargs.get('page')+1})
        
