from WindPy import *
from datetime import *
import pandas as pd
import numpy as np
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
        print("写入第%s行数据"%i)
        for j in range(b):
            if type(data.iloc[i, j]) == pd.Timestamp:
                row_cells[j + 1].text = data.iloc[i, j].strftime('%Y-%m-%d')
            elif type(data.iloc[i, j]) == str:
                row_cells[j + 1].text = data.iloc[i, j]
            elif type(data.iloc[i, j]) == float:
                row_cells[j + 1].text = str(np.round(data.iloc[i, j],2))

            else:
                print("数据包含异常格式变量")

###指数截面表现#####
class index(object):
    def __init__(self, tradate,indexCode ,benchmark):
        self.indexCode = indexCode
        self.tradate = tradate
        self.benchmark = benchmark
        self.factor = None
        self.data = None
        self.indextimeseries = None
        codelist = w.wset("indexconstituent", "date=" + self.tradate + ";windcode=" + self.indexCode)
        self.list = pd.DataFrame(codelist.Data, columns=codelist.Codes, index=codelist.Fields).T["wind_code"].tolist()

##########获取指数成分#####
    def get_code_list(self):
        codelist = w.wset("indexconstituent","date="+self.tradate+";windcode="+self.indexCode)
        self.codelist = pd.DataFrame(codelist.Data, columns=codelist.Codes, index=codelist.Fields).T
        return self.codelist
    ###获取指数截面因子#####
    def get_factor(self):
        tradedate = datetime.strptime(self.tradate, '%Y-%m-%d').strftime('%Y%m%d')
        startdate = w.tdaysoffset(-1, "2018-10-10", "Period=M").Data[0][0].strftime('%Y%m%d')
        year = datetime.strptime(self.tradate, '%Y-%m-%d').year
        ind="pct_chg_per,val_pe_deducted_ttm,pb_lyr,dividendyield2,pe_est,est_peg,BOLL,DMA,industry_sw,val_lnfloatmv,val_floatmv"
        factor =w.wss(self.list,ind,"startDate=%s;endDate=%s;tradeDate=%s;year=%s;rptYear=%s;BOLL_N=26;BOLL_Width=2;BOLL_IO=1;priceAdj=F;cycle=D;DMA_S=10;DMA_L=50;DMA_N=10;DMA_IO=1;industryType=1" %(startdate,tradedate,tradedate,year,year))
        self.factor = pd.DataFrame(factor.Data, columns=factor.Codes, index=factor.Fields).T
        return self.factor

    def get_data(self):
        codelist = self.get_code_list()
        codelist.set_index(['wind_code'], inplace = True)

        factor = self.get_factor()
        self.data = pd.concat([codelist,factor], axis=1, join_axes=[factor.index])
        return self.data

    def get_indextimeseries(self):
        data = w.wsd(self.indexCode,"close,pct_chg", "ED-5Y",self.tradate, "")
        self.indextimeseries = pd.DataFrame(data.Data, columns=data.Times, index=data.Fields).T
        self.indextimeseries["PCT_CHG_1"] = self.indextimeseries["PCT_CHG"].map(lambda x: x / 100 + 1)
        self.indextimeseries["nav"] = self.indextimeseries["PCT_CHG_1"].cumprod()










if __name__ == '__main__':
    from docx import Document
    zz500=index("2018-9-26","000905.SH","000905.SH")
    zz500.get_code_list()
    zz500.get_factor()
    zz500.get_data()
    zz500.get_indextimeseries()
    timeseries = zz500.indextimeseries
    aa=plt.figure()
    timeseries["nav"].plot()
    plt.savefig("E:\\github\\X\\2.jpg")
    plt.show()


    document = Document()
    data=zz500.get_data()

    writeTable(data,document)
    document.save("E:\\github\\X\\demo.docx")
    print("end")



