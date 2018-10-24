#!/usr/bin/env python
from sqlalchemy import create_engine,Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

Base = declarative_base()

class MySQLAlchemy(object):
    def __init__(self, db, dbName):

        url = "mysql+pymysql://root:8261426@localhost:3306/%s" % dbName
        eng = create_engine(url)
        Base = declarative_base()
        Base.metadata.create_all(eng)
        Session = sessionmaker(bind=eng)
        self.session = Session()
        self.db = db
        self.eng = eng82
        ##Base.metadata.create_all(self.eng)
    def insert(self,user):
        self.session.add(user)
        self.session.commit()

    def query(self):
        pass

    def close(self):
        self.eng.dispose()


from sqlalchemy import Sequence
Column(Integer, Sequence('user_id_seq'), primary_key=True)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')


con =  MySQLAlchemy("we","test")
