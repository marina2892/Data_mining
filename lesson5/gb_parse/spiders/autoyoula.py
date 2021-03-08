import scrapy
import re
from ..loaders import AutoyoulaLoader

class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru'] 
    start_urls = ['https://auto.youla.ru/']  
    _xpath_selectors = {
        'brands':"//div[@data-target='transport-main-filters']/div[contains(@class,'TransportMainFilters_brandsList')]//a[@data-target='brand']/@href",
        'pagination':"//a[contains(@class,'Paginator_button')]/@href",
        'car':"//div[contains(@class,'SerpSnippet_titleWrapper')]//a[@data-target='serp-snippet-title']/@href"   
    
    }
    
    _car_xpath = {
        'title':"//div[@data-target='advert-title']/text()",
        'list_img':"//img[contains(@class,'PhotoGallery_photoImage')]/@src",
        'parameters':"//h3[contains(text(),'Характеристики')]/..//div[contains(@class,'AdvertSpecs_row')]"
    
    
    }
    
     
    
    @staticmethod
    def get_user(response):
        marker = "window.transitState = decodeURIComponent"
        for script in response.xpath("//script"):
            try:
                if marker in script.xpath("./text()").extract_first():
                    re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
                    result = re.findall(re_pattern, script.xpath("./text()").extract_first())
                    return (response.urljoin(f"/user/{result[0]}")) if result else None
            except TypeError:
                pass        
        
    
    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.xpath(select_str):
            yield response.follow(a, callback = callback, cb_kwargs = kwargs)
        
        
    def parse(self, response, *args, **kwargs):
        
        
        yield from self._get_follow(response,self._xpath_selectors['brands'], self.brand_parse, hello = 'moto') 
    
        
            
            
    def brand_parse(self, response, **kwargs):
        yield from self._get_follow(response, self._xpath_selectors['pagination'],self.brand_parse)
        
        
        
        yield from self._get_follow(response, self._xpath_selectors['car'], self.car_parse)    
        
            
    def car_parse(self, response):
        loader = AutoyoulaLoader(response=response)
        loader.add_value('url', response.url)
        loader.add_xpath("title","//div[@data-target='advert-title']/text()")
        
        for key, value in self._car_xpath.items():
            loader.add_xpath(key, value)
    
        
        yield loader.load_item()
        
       
       
        
       
        
   
        
        
           
        
        
        
        
