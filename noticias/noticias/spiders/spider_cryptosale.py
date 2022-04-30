# -*- coding: utf-8 -*-
import scrapy
import string
import json 
import re
from datetime import datetime, timedelta
from scrapy import Request
from scrapy.utils.response import open_in_browser
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


class cryptoslate(scrapy.Spider):
    name = 'cryptoslate'

    def start_requests(self):
        url = 'https://cryptoslate.com'
        yield Request(url=url, callback=self.start_search, dont_filter=True)

    def start_search(self, response):
        #print("url",response.url)
        news = response.xpath('//div[contains(@class, "list-feed slate news clearfix")]/div[contains(@class, "list-post clearfix")]/article/a')
        print("noticas",len(news))
        for n in news:
            link = n.xpath('./@href').extract_first()
            title = n.xpath('./div[contains(@class, "content")]/div[contains(@class, "title")]/h2/text()').extract_first()
            date = n.xpath('./div[contains(@class, "content")]/div[contains(@class, "title")]/span/span[contains(@class, "read")]/text()').extract_first()
            tema = ""
            descripcion = n.xpath('./div[contains(@class, "excerpt")]/p/text()').extract_first()
            print("--------------")
            item = NoticiasItem()
            fecha = re.findall(r'hours',date)
            if fecha:
                hora = re.findall(r'^[0-9]+',date)
                if hora:
                    today = datetime.now()
                    pubilicada = today - timedelta(hours = int(hora[0]))
                    print("pubilicada: ",pubilicada)
                    item['date'] = str(pubilicada)
                else:
                    item['date'] = date
            else:
                item['date'] = date
                
            item['title'] = clean_text(title)
            item['description'] = clean_text(descripcion)
            item['link'] = link
            item['topic'] = tema
            print("item_spider",item)
            yield item

    def open_page(self, response):
        print("texto",response.text)
        open_in_browser(response)