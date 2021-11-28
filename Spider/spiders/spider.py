import scrapy
from Spider.items import XuetangItem


class XuetangSpider(scrapy.Spider):
    name = 'xuetang'
    allowed_domains = ['www.xuetangx.com']
    start_urls = ['https://www.xuetangx.com/search?query=&org=&classify=1&type=&status=&page=1']
    
    def parse(self, response, **kwargs):
        
        # base_url = get_base_url(response)
        item = XuetangItem()
        
        for each in response.xpath("/html/body/div[1]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div"):
            # self.logger.info('each: %s', each)
            item['name'] = each.xpath("div[2]/p[1]/span[1]/text()")
            if (item['name']):
                item['name'] = item['name'].get().strip()
                self.logger.info('name: %s', item['name'])
                teacher_string = ""
                for teacher_each in each.xpath("div[2]/p[2]/span[1]/span"):
                    teacher_string = teacher_string + teacher_each.xpath("text()").get()
                item['teacher'] = teacher_string
                self.logger.info('teacher: %s', item['teacher'])
                item['school'] = each.xpath("div[2]/p[2]/span[2]/span/text()").get()
                self.logger.info('school: %s', item['school'])
                item['student_num'] = each.xpath("div[2]/p[2]/span[3]/text()").get()
                if item['student_num'] != None:
                    item['student_num'] = item['student_num'].strip()
                self.logger.info('student_num: %s', item['student_num'])
                if (item['name'] and item['teacher'] and item['school'] and item['student_num']):
                    yield item
        
        if response.url != None:
            yield scrapy.Request(response.url, callback=self.parse)
        # # 
        # self.logger.info('next_page: %s', next_page)
        
        
        # if (kwargs.get('page') == 5):
        #     pass
        # else:
        #     yield response.follow(next_page, callback=self.parse, cb_kwargs={'page': kwargs.get('page')+1})
        
