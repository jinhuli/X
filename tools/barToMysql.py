

import pymysql
from tools.to_mysql import *

from iFinDPy import *
thsLogin= THS_iFinDLogin("cfzq267", "592935")

class getBar(object):
    def __init__(self,date):
        self.date=date


    def getCodeList(self):
        # 股票-股票市场类-全部A股:001005010
        code_list=THS_DataPool('block',self.date+';001005010', 'date:Y,thscode:Y,security_name:Y')
        self.code_list_pd=THS_Trans2DataFrame(code_list)["THSCODE"].tolist()

    def getBar(self):

        Bar=THS_DateSerial(",".join(self.code_list_pd),'ths_open_price_stock;ths_high_price_stock;ths_low_stock;ths_close_price_stock;ths_amt_stock;ths_chg_ratio_stock;ths_trading_status_stock',\
                           '100;100;100;100;;;','Days:Tradedays,Fill:Previous,Interval:D',self.date,self.date)
        self.bar=THS_Trans2DataFrame(Bar)


A=getBar("2018-08-20")
A.getCodeList()
A.getBar()

A.bar.iloc[1:3,:]["thscode"][1]


To=ToMysql()
To.insert("bar",A.bar)

