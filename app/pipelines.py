import logging
import pymongo
from scrapy.exceptions import CloseSpider
import pprint

pp = pprint.PrettyPrinter(indent=4)


def write_error_handler(errors):
    """
    Handle write errors
    :param errors:
    :return:
    """
    # To be implemented
    pass


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
            mongo_db=db_settings['MONGO_DB'],
            collection_name=db_settings['COLLECTION_NAME']
        )

    def open_spider(self, spider):
        if not isinstance(self.mongo_uri, str):
            raise CloseSpider(reason='Invalid Mongo URI')

        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            self.items = self.db[self.collection_name]
        except Exception as e:
            raise CloseSpider(e)

    def process_item(self, item, spider):
        self.raw_data.append(dict(item))
        return item

    def close_spider(self, spider):

        if not self.client:
            logging.error('No client available')
            return

        try:
            self.items.create_index([('raw_note', pymongo.TEXT)], unique=True, background=True, sparse=True)
            self.items.insert_many(self.raw_data, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            write_error_handler(e.details['writeErrors'])

        self.client.close()

