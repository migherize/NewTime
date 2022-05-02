# -*- coding: utf-8 -*-
import scrapy
import string
import json 
import re
from datetime import datetime, timedelta
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


class bitcoinmagazine(scrapy.Spider):
    name = 'bitcoinmagazine'
    
    def __init__(self, *args, **kwargs):
        self.schedule = kwargs.pop('schedule', '')  # path to where all workflows are stored
        print("self.schedule",self.schedule)
        
    def start_requests(self):
        url = 'https://bitcoinmagazine.com'
        yield Request(url=url, callback=self.start_search, dont_filter=True)

    def start_search(self, response):
        news = response.xpath('//section[contains(@class, "mm-component-stack--has-header")]/phoenix-hub/section[contains(@class, "m-card-group")]/phoenix-non-personalized-recommendations-tracking/div[contains(@class, "l-grid")]/phoenix-super-link/phoenix-card/div[contains(@class, "m-card--content")]')
        print("noticas",len(news))
        for n in news:
            link = n.xpath('./phoenix-ellipsis/a/@href').extract_first()
            title = n.xpath('.//h2[contains(@class, "m-card--header-text")]/text()').extract_first()
            date = n.xpath('.//span[contains(@class, "mm-card--metadata-text")]/text()').extract_first()
            descripcion = n.xpath('.//p[contains(@class, "m-card--body")]/text()').extract_first()
            print("link",link)
            item = NoticiasItem()
            date = time(date.strip())
            item['date'] = date
            item['title'] = clean_text(title)
            item['description'] = clean_text(descripcion)
            item['link'] = response.url + link
            item['history'] = str(self.schedule)
            
            yield item

    def open_page(self, response):
        open_in_browser(response)