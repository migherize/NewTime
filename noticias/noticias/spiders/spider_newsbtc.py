# -*- coding: utf-8 -*-
import scrapy
import string
import json 
import re
from datetime import datetime, timedelta
from scrapy import Request
from scrapy.utils.response import open_in_browser
from noticias.time import time
from noticias.items import NoticiasItem

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


class newsbtc(scrapy.Spider):
    name = 'newsbtc'
    
    def __init__(self, *args, **kwargs):
        self.schedule = kwargs.pop('schedule', '')  # path to where all workflows are stored
        print("self.schedule",self.schedule)
        
    def start_requests(self):
        url = 'https://www.newsbtc.com'
        yield Request(url=url, callback=self.start_search, dont_filter=True)

    def start_search(self, response):
        news = response.xpath('//div[contains(@class, "jeg_posts jeg_block_container")]/div[contains(@class, "jeg_posts")]/article[contains(@class, "jeg_post")]/div[contains(@class, "jeg_postblock_content")]')
        print("noticas",len(news))
        for n in news:
            link = n.xpath('./h3/a/@href').extract_first()
            title = n.xpath('./h3/a/text()').extract_first()
            date = n.xpath('./div[contains(@class, "jeg_post_meta")]/div[contains(@class, "jeg_meta_date")]/a/text()').extract_first()
            descripcion = n.xpath('./div[contains(@class, "jeg_post_excerpt")]/p/text()').extract_first()
            
            item = NoticiasItem()
            date = time(date.strip())
            item['date'] = date
            item['title'] = clean_text(title)
            item['description'] = clean_text(descripcion)
            item['link'] = link
            item['history'] = str(self.schedule)
            
            print("item_spider",item)
            yield item

    def open_page(self, response):
        open_in_browser(response)