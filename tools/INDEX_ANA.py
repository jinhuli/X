from WindPy import *
from datetime import *
import pandas as pd
w.start()

class index(object):
    def __init__(self,indexCode,tradate):
        self.indexCode = indexCode
        self.tradate = tradate



    def get_code_list(self):
        self.codelist = w.wset("indexconstituent","date="+self.tradate+";windcode="+self.indexCode)


    def










indexCode="000905.SH"