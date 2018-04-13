from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, String, Integer

# db settings
dbuser = 'user' #DB username
dbpass = 'password' #DB password
dbhost = 'localhost' #DB host
dbname = 'scrapyspiders' #DB database name
engine = create_engine("mysql://%s:%s@%s/%s?charset=utf8&use_unicode=0"
                       %(dbuser, dbpass, dbhost, dbname),
                       echo=False,
                       pool_recycle=1800)
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))

Base = declarative_base()

class AllData(Base):
    __tablename__ = 'alldata'

    id = Column(Integer, primary_key=True)
    date = Column(String(1000))
    note = Column(String(1000))

    def __init__(self, id=None, date=None, note=None):
        self.id = id
        self.date = date
        self.note = note

    def __repr__(self):
        return "<AllData: id='%d', date='%s', note='%s'>" % (self.id, self.date, self.note)