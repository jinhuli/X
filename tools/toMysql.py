#!/usr/bin/env python
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base




engine = create_engine('mysql+pymysql://root:8261426@localhost:3306/test?charset=utf8')
Base = declarative_base()

class MySQLAlchemy(object):
    def __init__(self, db, dbName,User):
        import pymysql
        url = "mysql+pymysql://root:8261426@localhost:3306/%s" % dbName

    eng = create_engine(url)


class User(Base):

    __tablename__ = 'users'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


DBSession = sessionmaker(bind=engine)

# 创建session对象:
session = DBSession()
# 创建新User对象:
new_user = User(id='5', name='Bob')
# 添加到session:
session.add(new_user)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()