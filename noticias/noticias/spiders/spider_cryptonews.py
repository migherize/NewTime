# -*- coding: utf-8 -*-
import scrapy
import string
import json 
from datetime import datetime
from scrapy import Request
from scrapy.utils.response import open_in_browser
from noticias.items import NoticiasItem
from noticias.time import time

def clean_text(text, replace_commas_for_spaces=True):
    text = str(text)
    if not isinstance(text, float) and not isinstance(text, int):
        text = ''.join([c for c in text if c in string.printable])
        if replace_commas_for_spaces:
            text = text.replace(';', ' ').replace(',', '').replace('"','').replace("['", '').replace("']", '').replace('\xa0','')\
                .replace("\n", '').replace("\t", '').replace("\r", '').strip()
        else:
            text = text.replace(';', ' ').replace(',', '').replace('"','').replace("['", '').replace("']", '').replace('\xa0','').replace("\n", '').strip()
    if text == 'nan':
        text = ''
    return text


class cryptonews(scrapy.Spider):
    name = 'cryptonews'
    
    def __init__(self, *args, **kwargs):
        self.schedule = kwargs.pop('schedule', '')  # path to where all workflows are stored
        print("self.schedule",self.schedule)
        
    def start_requests(self):
        url = 'https://it.cryptonews.com'
        yield Request(url=url, callback=self.start_search, dont_filter=True)

    def start_search(self, response):
        print("url",response.url)
        news = response.xpath('//section[contains(@class, "category_contents_details")]/article/div[contains(@class, "row")]')
        print("noticas",len(news))
        for n in news:
            date = n.xpath('.//div[contains(@class, "article__badge-date")]/@data-utctime').extract_first()
            title = n.xpath('./div/a[contains(@class, "article__title")]/text()').extract_first()
            descripcion = n.xpath('./div/div[contains(@class, "mb-25")]/text()').extract_first()
            link = n.xpath('./div/a/@href').extract_first()
            print("--------------")
            item = NoticiasItem()
            date = time(date.strip())
            item['date'] = date
            item['title'] = clean_text(title)
            item['description'] = clean_text(descripcion)
            item['link'] = response.url + link
            item['history'] = str(self.schedule)
            print("item_spider",item)
            yield item

    def open_page(self, response):
        print("texto",response.text)
        open_in_browser(response)