import scrapy
from ..loaders import HhLoader

class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://barnaul.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=11']
    
    _vacancy_xpath = {
        'vacancy':"//a[@data-qa = 'vacancy-serp__vacancy-title']/@href",
        'pagination':"//a[@data-qa = 'pager-page']/@href",
        'url_company':"//a[@class = 'vacancy-company-name']/@href"
     }
    _vacancy_xpath_loader = {
        'title':"//h1[@data-qa = 'vacancy-title']//text()",
        'salary':"//p[@class = 'vacancy-salary']//text()",
        'description1':"//div[@class = 'vacancy-description']//div[contains(@class,'bloko-gap')]//text()",
        'description2':"//div[@class = 'vacancy-description']",
        'skills':"//div[@class = 'bloko-tag-list']//div[contains(@class,'bloko-tag')]//text()",
     }    
    
    def _get_follow(self, response, selector_str, callback):
        for a in response.xpath(selector_str):
            yield response.follow(a, callback = callback)
            
            
    def parse(self, response):
        
        yield from self._get_follow(response, self._vacancy_xpath['pagination'], self.parse)
        
        yield from self._get_follow(response, self._vacancy_xpath['vacancy'], self.vac_parse)
        
    def vac_parse(self, response):
        loader = HhLoader(response=response)
        loader.add_value('url', response.url)
        url_company = response.xpath(self._vacancy_xpath['url_company']).extract_first()
        loader.add_value('url_company', response.urljoin(url_company))
        for key, value in self._vacancy_xpath_loader.items():
            loader.add_xpath(key, value)
            
        yield loader.load_item()
    
         
        
       
        
    
        
           