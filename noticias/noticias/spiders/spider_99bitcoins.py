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


class bitcoins(scrapy.Spider):
    name = 'bitcoins'
    
    def __init__(self, *args, **kwargs):
        self.schedule = kwargs.pop('schedule', '')  # path to where all workflows are stored
        print("self.schedule",self.schedule)
        
    def start_requests(self):
        url = 'https://99bitcoins.com/category/news/'
        yield Request(url=url, callback=self.start_search, dont_filter=True)

    def start_search(self, response):
        news = response.xpath('//div[contains(@class, "ast-row")]/article//div[contains(@class, "nnbitcoins")]')
        print("noticas",len(news))
        for n in news:
            link = n.xpath('./header/h2/a/@href').extract_first()
            print("link",link)
            
            title = n.xpath('./header/h2/a/text()').extract_first()
            print("title",title)
            
            descripcion = n.xpath('./div/p/text()').extract_first()
            print("descripcion",descripcion)
            
            guion = re.search(r'\–',title)
            print("guion",guion)
            
            if guion:
                date = (title[guion.end():]).strip()
                title = (title[:guion.start()]).strip()
                print("date",date)
            
            print("--------------")
            item = NoticiasItem()
            date = time(date.strip())
            date = date #+' '+ '00:00:00'
            print("date change",date)
            item['date'] = date
            item['title'] = clean_text(title)
            item['description'] = clean_text(descripcion)
            item['link'] = link
            item['history'] = str(self.schedule)
            
            yield item

    def open_page(self, response):
        open_in_browser(response)