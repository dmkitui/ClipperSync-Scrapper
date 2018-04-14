from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from spiders.ClippersyncSpider import ClippersyncSpider

DATABASE_SETTINGS = ClippersyncSpider.spider_details()['database']
print('DB SETS: ', DATABASE_SETTINGS)
DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**DATABASE_SETTINGS), pool_size=20, max_overflow=0)


def create_clipperdata_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class ClipperData(DeclarativeBase):
    __tablename__ = 'clipperdata'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    note = Column(Text, unique=True)

    def __init__(self, id=None, date=None, note=None):
        self.id = id
        self.date = date
        self.note = note

    def __repr__(self):
        return "<Data: date='%s', note='%s'>" % (self.date, self.note)