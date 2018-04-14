from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import ClipperData, db_connect, create_clipperdata_table


class AddTablePipeline(object):
    def __init__(self):
        engine = db_connect()
        create_clipperdata_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        self.raw_data = []

    def process_item(self, item, spider):
        new_item = ClipperData(date=item['date'], note=item['note'])
        self.raw_data.append(new_item)
        return item

    def close_spider(self, spider):
        for item in self.raw_data:
            try:
                self.session.add(item)
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
        self.session.close()

