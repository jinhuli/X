from WindPy import *
from datetime import *
import pandas as pd
w.start()

class index(object):
    def __init__(self,indexCode,tradate):
        self.indexCode = indexCode
        self.tradate = tradate
        codelist = w.wset("indexconstituent", "date=" + self.tradate + ";windcode=" + self.indexCode)
        self.list = pd.DataFrame(codelist.Data, columns=codelist.Codes, index=codelist.Fields).T["wind_code"].tolist()

    def get_code_list(self):
        codelist = w.wset("indexconstituent","date="+self.tradate+";windcode="+self.indexCode)
        self.codelist = pd.DataFrame(codelist.Data, columns=codelist.Codes, index=codelist.Fields).T
        return self.codelist

    def get_factor(self):
        tradedate = datetime.strptime(self.tradate, '%Y-%m-%d').strftime('%Y%m%d')
        ind="industry_sw,val_pe_deducted_ttm,mkt_cap_ard,pb_lf"
        factor = w.wss(self.list,ind ,"industryType=1;tradeDate="+tradedate+";unit=1")
        self.factor = pd.DataFrame(factor.Data, columns=factor.Codes, index=factor.Fields).T
        return self.factor

    def get_data(self):
        codelist = self.get_code_list()
        factor = self.get_factor()
        pd.concat(codelist,factor)


if __name__ == '__main__':
    from docx import Document
    zz500=index("000905.SH","2018-9-26")
    zz500.get_code_list()
    zz500.get_factor()


