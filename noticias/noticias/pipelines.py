# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import os

class NoticiasPipeline:
    def open_spider(self, spider):
        #self.file = open('items.json', 'a')
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item
        #line = json.dumps(ItemAdapter(item).asdict()) + ",\n"
        #self.file.write(line)
        #return item

    def close_spider(self, spider):
        path = '/Users/migherize/SourceTree/NewTime/newtime/src/data/items.json'
        with open(path) as file:
            data = json.load(file)
        print("Tamaño antes",len(data))
                
        if len(data) > 0:
            for i in self.items:
                data.append(i)
            print("Tamaño ahora",len(data))            
            # Ordenar
            ordenado = sorted(data, key=lambda x: x["date"], reverse=True)
            
            with open(path, 'w') as file:
                json.dump(ordenado, file, indent=4)
            
        else:
            self.file = open(path, 'a')
            self.file.write(json.dumps(self.items))
            self.file.close()
