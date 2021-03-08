from scrapy.loader import ItemLoader
from .items import GbAutoYoulaItem
from .items import GbHhItem
from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy import Selector



def get_parameters(item):
    selector = Selector(text = item)
    data = {
        'name':selector.xpath("//div[contains(@class,'AdvertSpecs_label')]/text()").extract_first(),
        'value':selector.xpath("//div[contains(@class,'AdvertSpecs_data')]//text()").extract_first()
    }
    return data

def get_description(item):
    selector = Selector(text = item)
    descr = selector.xpath("//div[@class='g-user-content']//text()").extract()
    if not descr:
        descr = selector.xpath("//div[@itemprop='description']//text()").extract()
    return descr

class AutoyoulaLoader(ItemLoader):
    default_item_class = GbAutoYoulaItem
    url_out = TakeFirst() 
    title_out = TakeFirst()
    parameters_in = MapCompose(get_parameters) 
    
class HhLoader(ItemLoader):
    default_item_class = GbHhItem
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_in = Join()
    salary_out = TakeFirst()
    description1_in = Join()
    description1_out = TakeFirst()
    description2_in = MapCompose(get_description)
    description2_out = Join()
    url_company_out = TakeFirst()
    