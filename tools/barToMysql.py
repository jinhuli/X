
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

    def getBar_ifindBar(self):

        Bar=THS_HistoryQuotes(",".join(self.code_list_pd),'open,high,low,close,changeRatio,amount,totalShares,totalCapital','Interval:D,CPS:1,baseDate:1900-01-01,Currency:YSHB,fill:Previous',self.date,self.date)
        self.bar=THS_Trans2DataFrame(Bar)

    def getBar_series(self):

        pass


To=ToMysql()
To.creat("bar")

To.insert("bar",A.bar)
To.delete("bar","2018-08-20")
To.close()

To=ToMysql()
date_A=THS_DateQuery('SSE','dateType:0,period:D,dateFormat:0','2016-1-1','2016-12-31')["tables"]["time"]
for day in date_A:
    print(day)
    A = getBar(day)
    A.getCodeList()
    A.getBar_ifindBar()
    To.insert("bar", A.bar)
To.close()


