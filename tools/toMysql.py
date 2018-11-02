#!/usr/bin/env python
from sqlalchemy import create_engine,Column, Integer, String,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

class MySQLAlchemy(object):
    def __init__(self,Base,user,dbName):
        """python和Mysql的接口类"""
        self.dbName =dbName
        url = "mysql+mysqlconnector://root:8261426@localhost:3306/%s" % self.dbName
        eng = create_engine(url)
        self.Base =Base
        Session = sessionmaker(bind=eng)
        self.session = Session()
        self.eng = eng
        ##Base.metadata.create_all(self.eng)
        self.user=user

    def creat(self):
        """创建表"""
        print("创建表",self.user.__tablename__)
        self.Base.metadata.create_all(self.eng)

    def insert(self,user,option):
        """插入数据"""
        if option == 1:
            self.session.add(user)
            self.session.commit()

        else:
            self.session.add_all(user)
            self.session.commit()

    def query(self,user):
        """查询数据"""
        our_user = self.session.query(user)
        return our_user

    def close(self):
        self.eng.dispose()




from sqlalchemy import Sequence
Base = declarative_base()
class Factor(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                                self.name, self.fullname, self.password)

class dateMon(Base):
    __tablename__ = 'month'
    id = Column(DateTime, primary_key=True)
    date = Column(DateTime)
    def __repr__(self):
        return "<User(name='%s')>" % (self.date)

