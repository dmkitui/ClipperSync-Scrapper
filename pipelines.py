from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import ClipperData, db_connect, create_clipperdata_table


class AddTablePipeline(object):
    def __init__(self):
        engine = db_connect()
        create_clipperdata_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def process_item(self, item, spider):
        new_item = ClipperData(date=item['date'], note=item['note'])
        try:
            self.session.add(new_item)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            return item
        finally:
            pass
        return item

    def close_spider(self, spider):
        self.session.close()

