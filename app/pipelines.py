import mongoengine
import logging
import pymongo
import json
from scrapy.exceptions import CloseSpider
from mongoengine import *
from app.models import ClipperItem
import pprint

pp = pprint.PrettyPrinter(indent=4)


def write_error_handler(errors):
    # pp.pprint(errors)
    # print('No of errors: ', len(errors))
    for error in errors:
        # print('ERROR CODE: ', error['code'])
        if 'E11000' not in error['errmsg']:
            print(error)
            print('Errors as above...')



class AddTablePipeline(object):

    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.items = None
        self.raw_data = []

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.spider.spider_settings['database']
        return cls(
            mongo_uri=db_settings['MONGO_URI'],
            mongo_db=db_settings['MONGO_DB_NAME'],
            collection_name=db_settings['COLLECTION_NAME']
        )

    def open_spider(self, spider):
        if not isinstance(self.mongo_uri, str):
            raise CloseSpider(reason='Invalid Mongo URI')

        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            self.items = self.db[self.collection_name]
            # self.items.create_index([('raw_note', pymongo.TEXT)], unique=True, background=True)
        except Exception as e:
            raise CloseSpider(e)

    def process_item(self, item, spider):
        # new_item = ClipperItem(date=item['date'], raw_note=item['raw_note'])
        self.raw_data.append(dict(item))
        return item

    def close_spider(self, spider):

        if not self.client:
            logging.error('No client available')
            return
        print('Total Items Scraped: ', len(self.raw_data))

        try:
            self.items.create_index([('raw_note', pymongo.TEXT)], unique=True, background=True, sparse=True)
            self.items.insert_many(self.raw_data, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            write_error_handler(e.details['writeErrors'])

        self.client.close()

