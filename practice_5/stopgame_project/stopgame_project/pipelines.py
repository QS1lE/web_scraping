# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class StopgameProjectPipeline:
#     def process_item(self, item, spider):
#         return item


import pymongo
from scrapy.utils.project import get_project_settings

class MongoDBPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.mongo_uri = settings.get('MONGO_URI', 'mongodb://localhost:27017/')
        self.mongo_db = settings.get('MONGO_DATABASE', 'stopgame_db')
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db['blogs']
        # Создаем уникальный индекс по data_key
        self.collection.create_index([('data_key', pymongo.ASCENDING)], unique=True)
    
    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        try:
            # Обновляем существующую запись или вставляем новую
            self.collection.update_one(
                {'data_key': item['data_key']},
                {'$set': dict(item)},
                upsert=True
            )
            spider.logger.info(f"Данные сохранены в MongoDB: {item['title']}")
        except Exception as e:
            spider.logger.error(f"Ошибка при сохранении в MongoDB: {e}")
        return item