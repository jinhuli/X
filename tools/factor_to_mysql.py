import pymysql


class ToMysql(object):
    def __init__(self):
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_pass = "8261426"
        self.db_name = "stock"
        # 打开数据库连接
        self.db = pymysql.connect(self.db_host, self.db_user, self.db_pass,self.db_name
                                  , use_unicode=True, charset="utf8")
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    def creat(self, table_name):
        self.cursor.execute("DROP TABLE IF EXISTS %s" % table_name)
        sql = """CREATE TABLE %s (
         date  DATE PRIMARY KEY,
         open  DOUBLE,
         high  DOUBLE,  
         low   DOUBLE,
         close DOUBLE,
         volume  DOUBLE,
         pct_chg  DOUBLE,
         trade_status varchar(20) character set utf8   
                       )""" %table_name
        self.cursor.execute(sql)
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        self.db.commit()

    def insert(self, table_name, data):
        for i in range(len(data)):
            data_date = data.index[i].strftime('%Y-%m-%d')
            data_open = data["OPEN"][i]
            data_high = data["HIGH"][i]
            data_low = data["LOW"][i]
            data_close = data["CLOSE"][i]
            data_volume = data["VOLUME"][i]
            data_pct_chg = data["PCT_CHG"][i]
            data_trade_status = data["TRADE_STATUS"][i]
            sql = """INSERT INTO %s(date,open, high, low, close,volume,pct_chg,trade_status)
            VALUES (%s,%f,%f,%f,%f,%f,%f,%s)""" % (table_name, repr(data_date), data_open, data_high, data_low\
                                                 , data_close, data_volume, data_pct_chg, repr(data_trade_status))
            self.cursor.execute(sql)
            self.db.commit()

    def get_data(self):
        pass

    def close(self):
        self.db.close()

    def update(self):
        pass