import hashlib
from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from spiders.ClippersyncSpider import ClippersyncSpider
from marshmallow import Schema, fields

DATABASE_SETTINGS = ClippersyncSpider.spider_details()['database']
DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(URL(**DATABASE_SETTINGS), pool_size=20, max_overflow=0)


def create_clipperdata_table(engine):
    DeclarativeBase.metadata.create_all(engine)


# Method to compute hash for date_raw_note columns to enforce unique contraints
def note_hash(context):
    note = (context.current_parameters['raw_note'] + context.current_parameters['date']).encode('utf-8')
    return hashlib.md5(note).hexdigest()


class ClipperData(DeclarativeBase):
    __tablename__ = 'clipperdata'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    raw_note = Column(Text)
    edit_flag = Column(Boolean, default=False)
    edited_note = Column(Text, nullable=True)
    hash = Column(String, unique=True, default=note_hash)

    def __init__(self, id=None, date=None, raw_note=None):
        self.id = id
        self.date = date
        self.raw_note = raw_note

    def __repr__(self):
        return "<Data: date='%s', raw_note='%s' edit_flag='%s edited_note='%s'>" % (self.date, self.raw_note, self.edit_flag, self.edited_note)


class ClipperDataSchema(Schema):
    """
    Marshmallow class for marshalling the Clipper data
    """
    id = fields.Integer()
    date = fields.DateTime()
    raw_note = fields.Str()
    edit_flag = fields.Boolean()
    edited_note = fields.Str()
