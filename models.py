from sqlalchemy import Column, String, Integer, DateTime
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
    date = Column(String)
    note = Column(String(10000), unique=True)

    def __init__(self, id=None, date=None, note=None):
        self.id = id
        self.date = date
        self.note = note

    def __repr__(self):
        return "<Data: id='%d', date='%s', note='%s'>" % (self.id, self.date, self.note)