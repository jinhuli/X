from WindPy import *
from datetime import *
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

w.start()


def writeTable(data,document):
    a = len(data)
    b = len(data.columns)
    table = document.add_table(rows=1, cols=b + 1)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "index"

    for cols in range(b):
        hdr_cells[cols + 1].text = data.columns[cols]

    for i in range(a):
        row_cells = table.add_row().cells
        row_cells[0].text = str(data.index[i])
        for j in range(b):
            if type(data.iloc[i, j]) == pd.Timestamp:
                row_cells[j + 1].text = data.iloc[i, j].strftime('%Y-%m-%d')
            elif type(data.iloc[i, j]) == str:
                row_cells[j + 1].text = data.iloc[i, j]
            elif type(data.iloc[i, j]) == float:
                row_cells[j + 1].text = str(data.iloc[i, j])

            else:
                print("数据包含异常格式变量")

###指数每日#####
class index(object):
    def __init__(self,tradate,indexCode = None):
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
        codelist.set_index(['wind_code'], inplace = True)

        factor = self.get_factor()
        self.data = pd.concat([codelist,factor], axis=1, join_axes=[factor.index])
        return self.data

    def get_indexTimeSeries(self):
        data = w.wsd(self.indexCode,"close,pct_chg", "ED-5Y",self.tradate, "")
        self.indextimeseries = pd.DataFrame(data.Data, columns=data.Times, index=data.Fields).T
        nav = self.indextimeseries
        ##plt.figure()
        ##indextimeseries.plot()
        ##plt.title("Simple Plot")
        ##plt.savefig("E:\\github\\X\\1.jpg")













if __name__ == '__main__':
    from docx import Document
    zz500=index("2018-9-26","000905.SH")
    zz500.get_code_list()
    zz500.get_factor()
    zz500.get_data()
    zz500.get_indexTimeSeries()
    timeseries = zz500.indextimeseries
    timeseries["PCT_CHG_1"] = timeseries["PCT_CHG"].map(lambda x: x / 100 + 1)
    from docx import Document

    document = Document()
    data=zz500.get_data()

    writeTable(data,document)
    document.save("E:\\github\\X\\demo.docx")




