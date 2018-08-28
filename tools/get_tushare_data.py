from WindPy import *
import numpy as np
import pandas as pd
from datetime import datetime


import tushare as ts
ts.get_hist_data('600848')
w.start()
class wss(object):
    ##获取wind 里面的WSD数据，并转换为dataframe
    def __init__(self,code,startdate,enddate,variable="open,high,low,close,volume,pct_chg,trade_status",frequency="day"):
        self.code=code
        self.startdate=startdate
        self.enddate=enddate
        self.frequency=frequency
        self.variable=variable

    def get_data(self):
        if self.frequency=="day":
            indata = w.wsd(self.code,self.variable, datetime.strftime(self.startdate,'%Y-%m-%d'),
                           datetime.strftime(self.enddate,'%Y-%m-%d'), "")
            if indata.ErrorCode != 0:
                    print('错误:' + str(indata.ErrorCode) + '\n')
                    return ()
            data = np.array(indata.Data)
            Fields = indata.Fields
            df = pd.DataFrame(data.transpose(), index=list(indata.Codes), columns=Fields)
            return df
        elif self.frequency=="min":
            indata=w.wsi(self.code, "open,high,low,close,volume,pct_chg",strftime(self.startdate,'%Y-%m-%d'),
                         datetime.strftime(self.enddate,'%Y-%m-%d %H:%M:%S'), "BarSize=5")
            if indata.ErrorCode != 0:
                    print('错误:' + str(indata.ErrorCode) + '\n')
                    return ()
            data = np.array(indata.Data)
            Fields = indata.Fields
            df = pd.DataFrame(data.transpose(), index=list(indata.Times), columns=Fields)
            return df

    class wss(object):
        ##获取多维数据
        w.start()

        def __init__(self, code, date, variable="close"):
            self.code = code
            self.date = datetime.strftime(date, '%Y%m%d')
            self.variable = variable

        def get_data(self):
            indata = w.wss(self.code, self.variable, "tradeDate=" + self.date + ";priceAdj=F;cycle=D")
            if indata.ErrorCode != 0:
                print('错误:' + str(indata.ErrorCode) + '\n')
                return ()
            data = np.array(indata.Data)
            Fields = indata.Fields
            df = pd.DataFrame(data.transpose(), index=list(indata.Times), columns=Fields)
            return df
