# from models import AllData, db


class AddTablePipeline(object):

    def process_item(self, item, spider):
        print('Pipeline runnning? ')
        return item

    def close_spider(self, spider):
        print('Did we close?')

