import logging
import pymongo
from scrapy.exceptions import CloseSpider


def write_error_handler(errors):
    """
    Handle write errors
    :param errors:
    :return:
    """
    # To be implemented
    pass


class ProcessRawItem(object):

    def __init__(self, stats, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.items = None
        self.raw_data = []
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.spider.spider_settings['database']
        return cls(
            crawler.stats,
            mongo_uri=db_settings['MONGO_URI'],
            mongo_db=db_settings['MONGO_DB'],
            collection_name=db_settings['RAW_COLLECTION_NAME']
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
        if not self.raw_data:
            logging.error('No items to process!')
            return

        try:
            self.items.create_index([('raw_note', pymongo.ASCENDING)], unique=True, background=True, sparse=True)
            self.items.insert_many(self.raw_data, ordered=False)
        except pymongo.errors.BulkWriteError as e:
            write_error_handler(e.details['writeErrors'])

        self.items.aggregate([{"$match": {}}, {"$out": 'clipper_items'}])
        db = self.db['clipper_items']
        db.create_index([('raw_note', pymongo.TEXT)], background=True, sparse=True)

        # TODO Implement time completed running from scrapy stats 'finish_time'
        last_run = self.stats.get_value('start_time')
        spider_stats = self.db['spider_stats']
        spider_stats.insert({'FancySpider': {'last_run': last_run}})

        self.client.close()

