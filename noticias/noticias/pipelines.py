# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import os
from os import path
import sqlite3

data = {}
path_folder = '/Users/migherize/SourceTree/NewTime/newtime/src/data/'
workname = 'items.json'
list_item = ['date','title','description','link','history']
name_db = '{}_history.db'.format(workname)
con = sqlite3.connect(path.join(path_folder, name_db))
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS info (history text, title text, descripcion text, link text, date_news text)''')

class NoticiasPipeline:
    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        item = []
        schedule = spider.schedule
        
        if os.path.exists(path.join(path_folder, workname)):
            print("existe")
            with open(path.join(path_folder, workname)) as file:
                data = json.load(file)
            print("Tamaño antes",len(data))
            
            print("schedule", data[0]['history'])
            print("item", self.items[0]['history'])
            
            if data[0]['history'] == self.items[0]['history']:
                if len(data) > 0:
                    for i in self.items:
                        data.append(i)
                
                print("Tamaño ahora",len(data))            
                # Ordenar
                ordenado = sorted(data, key=lambda x: x["date"], reverse=True)
                with open(path.join(path_folder, workname), 'w') as file:
                    json.dump(ordenado, file, indent=4)
            else:
                #inser DB
                with open(path.join(path_folder, workname)) as file:
                    data_json = json.load(file)
                
                for lista in data_json:
                    for key,value in lista.items():
                        if key == list_item[0]:
                            date_news = value
                            
                        elif key == list_item[1]:
                            titulo = value
                            
                        elif key == list_item[2]:
                            descripcion = value
                            
                        elif key == list_item[3]:
                            link = value
                            
                        elif key == list_item[4]:
                            historial = value

                    param = (historial,titulo,descripcion,link,date_news)
                    cur.execute("INSERT INTO info VALUES (?,?,?,?,?)",param)
                    con.commit()
                con.close()
                
                #ordenar noticias
                if len(self.items) > 0:
                    for i in self.items:
                        item.append(i)
                    ordenado = sorted(item, key=lambda x: x["date"], reverse=True)
            
                self.file = open(path.join(path_folder, workname), 'w')
                self.file.write(json.dumps(ordenado, indent=4))
                self.file.close()
                
        else:
            #ordenar noticias
            if len(self.items) > 0:
                for i in self.items:
                    item.append(i)
                ordenado = sorted(item, key=lambda x: x["date"], reverse=True)
            
            self.file = open(path.join(path_folder, workname), 'w')
            self.file.write(json.dumps(ordenado, indent=4))
            self.file.close()  
        