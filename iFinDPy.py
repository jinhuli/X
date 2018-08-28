# -*- coding: utf-8 -*-
"""
版本：1.0.0.1
作者：邓猛 dengmeng@myhexin.com 时间：20141106
更新时间：20141106 增加数据接口
文档介绍：iFinD Python接口程序。需与FTDataInterface.dll一起使用
修改历史：
版权：同花顺iFinD
"""

from ctypes import *
import sys
import re
import string
import types
import platform
import os
import threading
import copy
from datetime import datetime,date,time,timedelta
from collections import OrderedDict

def THS_iFinDLogin(username, password):
    return iFinD.FT_iFinDLogin(username, password);

def THS_iFinDLogout():
    return iFinD.FT_iFinDLogout();

def THS_HighFrequenceSequence(thscode, jsonIndicator, jsonparam, begintime, endtime):
    return iFinD.FTQuerySynTHS_HighFrequenceSequence(thscode, jsonIndicator, jsonparam, begintime, endtime);

def THS_RealtimeQuotes(thscode, jsonIndicator, jsonparam=""):
    if(jsonparam == ""):
        jsonparam="pricetype:1";
    return iFinD.FTQuerySynTHS_RealtimeQuotes(thscode,jsonIndicator,jsonparam);

def THS_HistoryQuotes(thscode, jsonIndicator, jsonparam, begintime, endtime):
    return iFinD.FTQuerySynTHS_HisQuote(thscode,jsonIndicator,jsonparam,begintime,endtime);

def THS_BasicData(thsCode, indicatorName, paramOption):
    return iFinD.FTQuerySynTHS_BasicData(thsCode,indicatorName,paramOption);

def THS_Snapshot(thscode, jsonIndicator, jsonparam, begintime, endtime):
    return iFinD.FTQuerySynTHS_Snapshot(thscode,jsonIndicator,jsonparam,begintime,endtime);

def THS_DateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime):
    return iFinD.FTQuerySynTHS_DateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime);

def THS_DataPool(DataPoolname,paramname,FunOption):
    return iFinD.FTQuerySynTHS_DataPool(DataPoolname,paramname,FunOption)
def THS_EDBQuery(indicators, begintime, endtime):
    return iFinD.FT_EDBQuery(indicators,begintime,endtime)

def THS_iwencai(query,domain):
    return iFinD.FT_iwencai(query,domain)
    
def THS_DataStatistics():
    return iFinD.FT_DataStastics()

def THS_GetErrorInfo(errorcode):
    return iFinD.FT_GetErrorInfo(errorcode);
def THS_DateQuery(exchange, params, begintime, endtime):
    return iFinD.FT_DateQuery(exchange, params, begintime, endtime)
def THS_DateOffset(exchange, params, endtime):
    return iFinD.FT_DateOffset(exchange, params, endtime)
def THS_DateCount(exchange, params, begintime, endtime):
    return iFinD.FT_DateCount(exchange, params, begintime, endtime)
def THS_DateSerial(thscode, jsonIndicator, jsonparam, globalparam, begintime, endtime):
    return iFinD.FTQueryTHS_DateSerial(thscode, jsonIndicator, jsonparam, globalparam, begintime, endtime);

def THS_AsyHighFrequenceSequence(thscode, jsonIndicator, jsonparam, begintime, endtime,Callback,pUser,iD):
    return iFinD.FTQueryTHS_HighFrequenceSequence(thscode, jsonIndicator, jsonparam, begintime, endtime,Callback,pUser,iD)
    
def THS_AsyRealtimeQuotes(thscode, jsonIndicator, jsonparam,Callback,pUser,ID):
    return iFinD.FTQueryTHS_RealtimeQuotes(thscode,jsonIndicator,jsonparam,Callback,pUser,ID);

def THS_AsyHistoryQuotes(thscode, jsonIndicator, jsonparam, begintime, endtime,Callback,pUser,iD):
    return iFinD.FTQueryTHS_HisQuote(thscode,jsonIndicator,jsonparam,begintime,endtime,Callback,pUser,iD);

def THS_AsyBasicData(thsCode, indicatorName, paramOption,Callback,pUser,iD):
    return iFinD.FTQueryTHS_BasicData(thsCode,indicatorName,paramOption,Callback,pUser,iD);

def THS_AsyDateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime,Callback,pUser,iD):
    return iFinD.FTQueryTHS_DateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime,Callback,pUser,iD);

def THS_AsyEDBQuery(indicators, begintime, endtime,Callback,pUser,iD):
    return iFinD.FTQueryTHS_EDBQuery(indicators,begintime,endtime,Callback,pUser,iD)

def THS_Asyiwencai(query,domain,Callback,pUser,iD):
    return iFinD.FTQueryTHS_iwencai(query,domain,Callback,pUser,iD)
    
def THS_AsyDataPool(DataPoolname,paramname,FunOption,Callback,pUser,iD):
    return iFinD.FTQueryTHS_DataPool(DataPoolname,paramname,FunOption,Callback,pUser,iD)

def THS_AsySnapshot(thscode, jsonIndicator, jsonparam, begintime, endtime,Callback,pUser,iD):
    return iFinD.FTQueryTHS_Snapshot(thscode,jsonIndicator,jsonparam,begintime,endtime,Callback,pUser,iD);

def THS_AsyDateSerial(thscode,jsonIndicator,jsonparam,globalparam,begintime,endtime,Callback,pUser,iD):
    return iFinD.FTQueryTHS_AsyDateSerial(thscode,jsonIndicator,jsonparam,globalparam,begintime,endtime,Callback,pUser,iD);

def THS_QuotesPushing(thscode,indicator="",Callback=None):
    return iFinD.FTQueryTHS_QuotesPushing(thscode,indicator,Callback)

def THS_UnQuotesPushing(thscode="",indicator=""):
    return iFinD.FTQueryTHS_UnQuotesPushing(thscode,indicator)       
def THS_Trans2DataFrame(data):
    '''基本业务数据转换函数'''
    Data=copy.deepcopy(data)
    import numpy as np,pandas as pd
    if  ((('errorcode') in Data)and(Data['errorcode']==0)):
        codelength=len(Data['tables']);
        dataframe = pd.DataFrame()
        for x in range(codelength):
            #EDB处理
            if  ('id') in Data['tables'][x]:
                EdbId = Data['tables'][x]['id'][0]
                if (('time') in Data['tables'][x]):
                    Edblength = len(Data['tables'][x]['time'])
                    if(Edblength > 0):
                        Edblist = list()
                        for y in range(Edblength):
                            Edblist.append(EdbId)
                        dataframe1 = pd.DataFrame()
                        dataframe1.insert(0,'value',Data['tables'][x]['value'])
                        dataframe1.insert(0,'id',Edblist)
                        dataframe1.insert(0,'time',Data['tables'][x]['time'])
                        dataframe = dataframe.append(dataframe1,ignore_index=True)
            else:#除EDB之外的业务
                table =dict()
                detail=dict()
                datatype=0
                dataframezhubi=pd.DataFrame()
                if(('table' not in Data['tables'][x])and('detail' in Data['tables'][x])):#zhubi
                    datatype = 1
                    if(('time' in Data['tables'][x]) and (len(Data['tables'][x]['time'])>0)):
                        zbaccount = len(Data['tables'][x]['detail'])#获取每分钟的detail
                        for zb in range(zbaccount):
                            maxlen=0
                            detaillist = Data['tables'][x]['detail'][zb]
                            if(len(detaillist) == 0):
                                continue
                            detaillistkeys = list(detaillist.keys())
                            for keysi in range(len(detaillistkeys)):
                                detaillen = len(detaillist[detaillistkeys[keysi]])
                                if(detaillen > maxlen):
                                    maxlen = detaillen
                            for keysi in range(len(detaillistkeys)):
                                subdetaillist = detaillist[detaillistkeys[keysi]]
                                subdetaillen = len(subdetaillist)
                                for j in range(maxlen-subdetaillen):
                                    subdetaillist.append(None)
                                detaillist[detaillistkeys[keysi]] = subdetaillist
                            detailframe1 = pd.DataFrame(detaillist)
                            if(('thscode' in Data['tables'][x]) and len(Data['tables'][x]['thscode'])>0):
                                if(detailframe1.size>0):
                                    codelist = list()
                                    for z in range(maxlen):
                                        codelist.append(Data['tables'][x]['thscode'])
                                    detailframe1.insert(0,'thscode',codelist)
                            if(('time' in Data['tables'][x]) and len(Data['tables'][x]['time'])>0):
                                if(detailframe1.size>0):
                                    timelist = list()
                                    for m in range(maxlen):
                                        timelist.append(Data['tables'][x]['time'][zb])
                                    detailframe1.insert(0,'time',timelist)
                            dataframezhubi = dataframezhubi.append(detailframe1,ignore_index=True)
                    dataframe = dataframe.append(dataframezhubi,ignore_index=True)
                elif(('table' in Data['tables'][x])and('detail' in Data['tables'][x])):   #feizhubiandzhubi
                    datatype = 2
                    if(('time' in Data['tables'][x]) and (len(Data['tables'][x]['time'])>0)):
                        zbaccount = len(Data['tables'][x]['detail'])#获取每分钟的detail
                        for zb in range(zbaccount):
                            maxlen=0
                            detaillist = Data['tables'][x]['detail'][zb]
                            if(len(detaillist) == 0):
                                continue
                            detaillistkeys = list(detaillist.keys())
                            for keysi in range(len(detaillistkeys)):
                                detaillen = len(detaillist[detaillistkeys[keysi]])
                                if(detaillen > maxlen):
                                    maxlen = detaillen
                            for keysi in range(len(detaillistkeys)):
                                subdetaillist = detaillist[detaillistkeys[keysi]]
                                subdetaillen = len(subdetaillist)
                                for j in range(maxlen-subdetaillen):
                                    subdetaillist.append(None)
                                detaillist[detaillistkeys[keysi]] = subdetaillist
                            #detailframe1 = pd.DataFrame(detaillist)
                            tablekeys = list(Data['tables'][x]['table'].keys())
                            tabledict = {}
                            for keysaccount in range(len(tablekeys)):
                                sublist = list()
                                for o in range(maxlen):
                                    #print(tablekeys[keysaccount])
                                    #print(zb)
                                    sublist.append(Data['tables'][x]['table'][tablekeys[keysaccount]][zb])
                                tabledict[tablekeys[keysaccount]]=sublist
                            #tableframe1 = pd.DataFrame(tabledict)
                            dictMerged=dict(tabledict,**detaillist)
                            detailframe1 = pd.DataFrame(dictMerged)
                            if(('thscode' in Data['tables'][x]) and len(Data['tables'][x]['thscode'])>0):
                                if(detailframe1.size>0):
                                    codelist = list()
                                    for z in range(maxlen):
                                        codelist.append(Data['tables'][x]['thscode'])
                                    detailframe1.insert(0,'thscode',codelist)
                            if(('time' in Data['tables'][x]) and len(Data['tables'][x]['time'])):
                                if(detailframe1.size>0):
                                    timelist = list()
                                    for m in range(maxlen):
                                        timelist.append(Data['tables'][x]['time'][zb])
                                    detailframe1.insert(0,'time',timelist)
                            dataframezhubi = dataframezhubi.append(detailframe1,ignore_index=True)
                    dataframe = dataframe.append(dataframezhubi,ignore_index=True)
                else:#feizhubi
                    maxlen=0
                    datatype = 3
                    if('table' not in Data['tables'][x]):
                        continue
                    table=Data['tables'][x]['table']
                    #处理返回数据长度不一的问题
                    keys=list(table.keys())
                    for i in range(len(keys)):
                        if(table[keys[i]] == None):
                            continue
                        datalen = len(table[keys[i]])
                        if(datalen > maxlen):
                            maxlen=datalen
                    if(maxlen > 0):    
                        for i in range(len(keys)):
                            datalist = table[keys[i]]
                            if(datalist == None):
                                datalistlen = 0;
                                datalist = list();
                            else:
                                datalistlen = len(datalist)
                            for j in range(maxlen-datalistlen):
                                datalist.append(None)
                                table[keys[i]] = datalist
                        dataframe1 = pd.DataFrame(table)#先从字典转换到dataframe
                        if  (('thscode' not in dataframe1)and('thscode') in Data['tables'][x])and(len(Data['tables'][x]['thscode'])>0):#有股票
                            if dataframe1.size>0:#有股票有值   实时行情  基础数据  数据池
                                #keys = Data['tables'][x]['table'].keys()
                                #if len(keys)>0:
                                    #    keyname=keys[0]
                                #    valuelength=len(Data['tables'][0]['table'][keyname])
                                codelist  = list()
                                for y in range(maxlen):
                                    codelist.append(Data['tables'][x]['thscode'])
                                dataframe1.insert(0,'thscode',codelist)
                            else:
                                dataframe1.insert(0,'thscode',[Data['tables'][x]['thscode']])
                        if  (('time') in Data['tables'][x])and(len(Data['tables'][x]['time'])>0):
                            dataframe1.insert(0,'time',Data['tables'][x]['time'])        
                        dataframe = dataframe.append(dataframe1,ignore_index=True)
        return dataframe
        
    else:
        return Data

def OnRealTimeCallback(pUderdata,id,sResult,len,errorcode,reserved):
    print(sResult)
    return 0

def OnFTAsynCallback(pUserdata,id,sResult,len,errorcode,reserved):
    global g_FunctionMgr
    global g_Funclock
    g_Funclock.acquire();
    userfunc = g_FunctionMgr[id]
    del(g_FunctionMgr[id])
    g_Funclock.release()
    if(callable(userfunc)):
        userfunc(pUserdata,id,sResult,len,errorcode,reserved)
    return 0

CMPTHSREALTIMEFUNC=CFUNCTYPE(c_int,c_void_p,c_int32,c_wchar_p,c_int32,c_int32,c_int32)

pRealTimeFunc=CMPTHSREALTIMEFUNC(OnRealTimeCallback)
pAsyFunc=CMPTHSREALTIMEFUNC(OnFTAsynCallback)
nRegRTID = 0;

g_FunctionMgr={};
g_Funclock=threading.Lock();

class iFinD:

    decodeMethod = "gb2312";
    isWin = 'Windows' in platform.system()
    version=sys.version  
    #print(version);
    verss=version.split()[0].split('.');
    ver=int(verss[0])+float(verss[1])/10;
    isless3 = True
    if(ver  >= 3.0):
        isless3 = False
    sitepath=".";           
    for x in sys.path:
        ix=x.find('site-packages')
        iy=x.find('dist-packages')
        if( (ix>=0 and x[ix:]=='site-packages') or (iy>=0 and x[iy:]=='dist-packages')):
            sitepath=x;
            if(isWin):
                sitepath=sitepath+"\\iFinDPy.pth"
            else:
                sitepath=sitepath+"/iFinDPy.pth"
            print(sitepath)
            if(os.path.exists(sitepath)):
                pathfile=open(sitepath)
                dllpath=pathfile.readlines();
                pathfile.close();
                dllpath=''.join(dllpath).strip('\n')
                if(isWin):
                    bit=int(sys.version.split(' bit ')[0].split()[-1]);
                    if(bit==32 ):
                        sitepath=dllpath+"\\ShellExport.dll"
                    else:
                        sitepath=dllpath+"\\ShellExport.dll"
                else:
                    architecture = platform.architecture();
                    if(architecture[0]== '32bit'):
                        sitepath=dllpath+"/libShellExport.so";
                    else:
                        sitepath=dllpath+"/libShellExport.so";

    #print(sitepath)
    c_iFinDlib=cdll.LoadLibrary(sitepath)

    #FT_ifinDLoginPy
    c_FT_ifinDLoginPy=c_iFinDlib.THS_iFinDLoginPython;
    c_FT_ifinDLoginPy.restype=c_int32;
    c_FT_ifinDLoginPy.argtypes=[c_char_p,c_char_p]

    #FTQueryTHS_SynHFQByJsonPy
    c_FTQueryTHS_SynHFQByJsonPy=c_iFinDlib.THS_HighFrequenceSequencePython;
    c_FTQueryTHS_SynHFQByJsonPy.restype=c_void_p;
    c_FTQueryTHS_SynHFQByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p]

    #FTQueryTHS_SynDateSeriesByJsonPy
    c_FTQueryTHS_SynDateSeriesByJsonPy=c_iFinDlib.THS_DateSequencePython;
    c_FTQueryTHS_SynDateSeriesByJsonPy.restype=c_void_p;
    c_FTQueryTHS_SynDateSeriesByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p]

    #c_FTQuery_SynSnapshotPy
    c_FTQuery_SynSnapshotPy=c_iFinDlib.THS_SnapshotPython;
    c_FTQuery_SynSnapshotPy.restype=c_void_p;
    c_FTQuery_SynSnapshotPy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p]

    #c_FTQuery_SynDateSerialPy
    c_FTQuery_SynTHS_DateSerialPython=c_iFinDlib.THS_DateSerialPython;
    c_FTQuery_SynTHS_DateSerialPython.restype=c_void_p;
    c_FTQuery_SynTHS_DateSerialPython.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p]

    #FTQuery_SynRTByJsonPy
    c_FTQuery_SynRTByJsonPy=c_iFinDlib.FTQuery_SynRTByJsonPy;
    c_FTQuery_SynRTByJsonPy.restype=c_char_p;
    c_FTQuery_SynRTByJsonPy.argtypes=[c_wchar_p,c_wchar_p,c_wchar_p]

    #FTQuery_SynBasicDataPy
    c_FTQuery_SynBasicDataPy=c_iFinDlib.FTQuery_SynBasicDataPy;
    c_FTQuery_SynBasicDataPy.restype=c_char_p;
    c_FTQuery_SynBasicDataPy.argtypes=[c_wchar_p,c_wchar_p]

    #FTQuery_SynDataPoolByJsonPy
    c_FTQuery_SynDataPoolByJsonPy=c_iFinDlib.FTQuery_SynDatapool;
    c_FTQuery_SynDataPoolByJsonPy.restype=c_char_p;
    c_FTQuery_SynDataPoolByJsonPy.argtypes=[c_wchar_p,c_wchar_p,c_wchar_p]

    #FTQuery_SynHisQuoteByJsonPy
    c_FTQuery_SynHisQuoteByJsonPy=c_iFinDlib.FTQuery_SynHisQuoteByJsonPy;
    c_FTQuery_SynHisQuoteByJsonPy.restype=c_char_p;
    c_FTQuery_SynHisQuoteByJsonPy.argtypes=[c_wchar_p,c_wchar_p,c_wchar_p,c_wchar_p,c_wchar_p]

    #c_FTQuery_SynDateSerialByJsonPy=c_iFinDlib.FTQuery_SynDateSerialByJsonPy;
    #c_FTQuery_SynDateSerialByJsonPy.restype=c_char_p;
    #c_FTQuery_SynDateSerialByJsonPy.argtypes=[c_wchar_p,c_wchar_p,c_wchar_p,c_wchar_p,c_wchar_p,c_wchar_p]

    #FTQueryTHS_SynRTByJsonPy
    c_FTQueryTHS_SynRTByJsonPy=c_iFinDlib.THS_RealtimeQuotesPython;
    c_FTQueryTHS_SynRTByJsonPy.restype=c_void_p;
    c_FTQueryTHS_SynRTByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p]

    #FTQueryTHS_SynBasicDataPy
    c_FTQueryTHS_SynBasicDataPy=c_iFinDlib.THS_BasicDataPython;
    c_FTQueryTHS_SynBasicDataPy.restype=c_void_p;
    c_FTQueryTHS_SynBasicDataPy.argtypes=[c_char_p,c_char_p,c_char_p]

    #FTQueryTHS_SynDataPoolByJsonPy
    c_FTQueryTHS_SynDataPoolByJsonPy=c_iFinDlib.THS_DataPoolPython;
    c_FTQueryTHS_SynDataPoolByJsonPy.restype=c_void_p;
    c_FTQueryTHS_SynDataPoolByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p]

    #FTQueryTHS_SynHisQuoteByJsonPy
    c_FTQueryTHS_SynHisQuoteByJsonPy=c_iFinDlib.THS_HistoryQuotesPython;
    c_FTQueryTHS_SynHisQuoteByJsonPy.restype=c_void_p;
    c_FTQueryTHS_SynHisQuoteByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p]


    #FT_ifinDLogoutPy
    c_FT_ifinDLogoutPy=c_iFinDlib.THS_ifinDLogoutPython;
    c_FT_ifinDLogoutPy.restype=c_int32;
    c_FT_ifinDLogoutPy.argtypes=[]

    #FT_EDBQuery
    C_FT_ifinDEDBQuery=c_iFinDlib.THS_EDBQueryPython;
    C_FT_ifinDEDBQuery.restype=c_void_p;
    C_FT_ifinDEDBQuery.argtypes=[c_char_p,c_char_p,c_char_p]

    #FT_iwencai
    C_FT_ifinDiwencai=c_iFinDlib.THS_iwencaiPython;
    C_FT_ifinDiwencai.restype=c_void_p;
    C_FT_ifinDiwencai.argtypes=[c_char_p,c_char_p]

    #FTQueryTHS_DateSerialPy
    c_FTQueryTHS_THS_AsyDateSerialPython=c_iFinDlib.THS_AsyDateSerialPython;
    c_FTQueryTHS_THS_AsyDateSerialPython.restype=c_int32;
    c_FTQueryTHS_THS_AsyDateSerialPython.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)];

    #FTQueryTHS_AsynRTByJsonPy
    C_FTQueryTHS_AsynRTByJsonPy=c_iFinDlib.THS_QuotesPushingPython;
    C_FTQueryTHS_AsynRTByJsonPy.restype=c_int32;
    C_FTQueryTHS_AsynRTByJsonPy.argtypes=[c_char_p,c_char_p,c_char_p,c_bool,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_HighFrequenceSequencePy
    c_FTQueryTHS_HighFrequenceSequencePy=c_iFinDlib.THS_AsyHighFrequenceSequencePython;
    c_FTQueryTHS_HighFrequenceSequencePy.restype=c_int32;
    c_FTQueryTHS_HighFrequenceSequencePy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)];

    #FTQueryTHS_DateSequencePy
    c_FTQueryTHS_DateSequencePy=c_iFinDlib.THS_AsyDateSequencePython;
    c_FTQueryTHS_DateSequencePy.restype=c_int32;
    c_FTQueryTHS_DateSequencePy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_SnapshotPy
    c_FTQueryTHS_SnapshotPy=c_iFinDlib.THS_AsySnapshotPython;
    c_FTQueryTHS_SnapshotPy.restype=c_int32;
    c_FTQueryTHS_SnapshotPy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_RealtimeQuotesPy
    c_FTQueryTHS_RealtimeQuotesPy=c_iFinDlib.THS_AsyRealtimeQuotesPython;
    c_FTQueryTHS_RealtimeQuotesPy.restype=c_int32;
    c_FTQueryTHS_RealtimeQuotesPy.argtypes=[c_char_p,c_char_p,c_char_p,c_bool,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQuerySynTHS_iwencaiPy
    c_FTQueryTHS_iwencaiPy=c_iFinDlib.THS_AsyiwencaiPython;
    c_FTQueryTHS_iwencaiPy.restype=c_int32;
    c_FTQueryTHS_iwencaiPy.argtypes=[c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_BasicDataPy
    c_FTQueryTHS_BasicDataPy=c_iFinDlib.THS_AsyBasicDataPython;
    c_FTQueryTHS_BasicDataPy.restype=c_int32;
    c_FTQueryTHS_BasicDataPy.argtypes=[c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_DatapoolPy
    c_FTQueryTHS_DatapoolPy=c_iFinDlib.THS_AsyDataPoolPython;
    c_FTQueryTHS_DatapoolPy.restype=c_int32;
    c_FTQueryTHS_DatapoolPy.argtypes=[c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_HisQuotePy
    c_FTQueryTHS_HisQuotePy=c_iFinDlib.THS_AsyHistoryQuotesPython;
    c_FTQueryTHS_HisQuotePy.restype=c_int32;
    c_FTQueryTHS_HisQuotePy.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #FTQueryTHS_EDBQueryPy
    c_FTQueryTHS_EDBQueryPy=c_iFinDlib.THS_AsyEDBQueryPython;
    c_FTQueryTHS_EDBQueryPy.restype=c_int32;
    c_FTQueryTHS_EDBQueryPy.argtypes=[c_char_p,c_char_p,c_char_p,CMPTHSREALTIMEFUNC,c_void_p,POINTER(c_int32)]

    #SetValue
    c_SetValue=c_iFinDlib.SetValue;
    c_SetValue.restype=c_int;
    c_SetValue.argtypes=[c_int,POINTER(c_int)]

    #DeleteMm
    c_DeleteMm=c_iFinDlib.DeleteMemory;
    c_DeleteMm.restype=c_int;
    c_DeleteMm.argtypes=[c_void_p];

    #FT_DataStatistics
    C_FT_ifinDDataStatissticsPy=c_iFinDlib.THS_DataStatisticsPython;
    C_FT_ifinDDataStatissticsPy.restype=c_void_p;
    C_FT_ifinDDataStatissticsPy.argtypes=[]

    #FT_GetErrorMsg
    C_FT_ifinDErrorMsg=c_iFinDlib.THS_GetErrorInfoPython;
    C_FT_ifinDErrorMsg.restype=c_void_p;
    C_FT_ifinDErrorMsg.argtypes=[c_int32];

    #FTQueryTHS_SynDateQueryPy
    C_FT_ifinDDateQuery=c_iFinDlib.THS_DateQueryPython;
    C_FT_ifinDDateQuery.restype=c_void_p;
    C_FT_ifinDDateQuery.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p]

    #FTQueryTHS_SynDateOffsetPy
    C_FT_ifinDDateOffset=c_iFinDlib.THS_DateOffsetPython;
    C_FT_ifinDDateOffset.restype=c_void_p;
    C_FT_ifinDDateOffset.argtypes=[c_char_p,c_char_p,c_char_p]

    #FTQueryTHS_SynDateCountPy
    C_FT_ifinDDateCount=c_iFinDlib.THS_DateCountPython;
    C_FT_ifinDDateCount.restype=c_void_p;
    C_FT_ifinDDateCount.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p]

    #FTQuery_SynHFQByJsonPy
    c_FTQuery_SynHFQByJsonPy=c_iFinDlib.FTQuery_SynHFQByJsonPy;
    c_FTQuery_SynHFQByJsonPy.restype=c_char_p;
    c_FTQuery_SynHFQByJsonPy.argtypes=[c_wchar_p,c_wchar_p,c_wchar_p,c_wchar_p,c_wchar_p]

    #FTQuery_SynDateSeriesByJsonPy
    c_FTQuery_SynDateSeriesByJsonPy=c_iFinDlib.FTQuery_SynDateSeriesByJsonPy;
    c_FTQuery_SynDateSeriesByJsonPy.restype=c_char_p;
    c_FTQuery_SynDateSeriesByJsonPy.argtypes=[c_wchar_p,c_wchar_p,c_wchar_p,c_wchar_p,c_wchar_p]

    @staticmethod
    def FT_iFinDLogin(username,password):
        """登陆入口函数"""
        if(iFinD.isWin):
            if(iFinD.isless3):
                username=c_char_p(username);
                password=c_char_p(password);
            else:
                username=c_char_p(bytes(username,'gbk'));
                password=c_char_p(bytes(password,'gbk'));
        else:
            username=c_char_p(bytes(username,'utf8'));
            password=c_char_p(bytes(password,'utf8'));
        out=iFinD.c_FT_ifinDLoginPy(username.value,password.value);
        return out;
    #FT_ifinDLoginPy=staticmethod(FT_ifinDLoginPy)

    @staticmethod
    def FT_iFinDLogout():
         """登出入口函数"""
         out=iFinD.c_FT_ifinDLogoutPy();
         return out;
     #FT_ifinDLogoutPy=staticmethod(FT_ifinDLogoutPy)

    @staticmethod
    def FTQuerySyn_HighFrequenceSequence(thscode,jsonIndicator,jsonparam,begintime,endtime):
        import json
        """高频序列"""
        thscode=c_wchar_p(thscode);
        jsonIndicators=c_wchar_p(jsonIndicator);
        jsonparams=c_wchar_p(jsonparam);
        begintime=c_wchar_p(begintime);
        endtime=c_wchar_p(endtime);
        out=iFinD.c_FTQuery_SynHFQByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value);
        out=json.loads(out.decode(iFinD.decodeMethod));
        return out;

    @staticmethod    
    def FTQuerySynTHS_HighFrequenceSequence(thscode,jsonIndicator,jsonparam,begintime,endtime):
        import json
        """高频序列"""
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                jsonparams=c_char_p(jsonparam);
                begintime=c_char_p(begintime);
                endtime=c_char_p(endtime);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
                begintime=c_char_p(bytes(begintime,'gbk'));
                endtime=c_char_p(bytes(endtime,'gbk'));
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));
        ptr=iFinD.c_FTQueryTHS_SynHFQByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod),object_pairs_hook=OrderedDict);
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FTQuerySyn_DateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime):
        import json
        """日期序列"""
        thscode=c_wchar_p(thscode);
        jsonIndicators=c_wchar_p(jsonIndicator);
        jsonparams=c_wchar_p(jsonparam);
        begintime=c_wchar_p(begintime);
        endtime=c_wchar_p(endtime);
        out=iFinD.c_FTQuery_SynDateSeriesByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value);
        out=json.loads(out.decode(iFinD.decodeMethod));
        return out;

    @staticmethod
    def FTQuerySynTHS_DateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime):
        import json
        """日期序列"""
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                jsonparams=c_char_p(jsonparam);
                begintime=c_char_p(begintime);
                endtime=c_char_p(endtime);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
                begintime=c_char_p(bytes(begintime,'gbk'));
                endtime=c_char_p(bytes(endtime,'gbk'));
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));
        ptr=iFinD.c_FTQueryTHS_SynDateSeriesByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod),object_pairs_hook=OrderedDict);
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FTQuerySyn_RealtimeQuotes(thscode,jsonIndicator,jsonparam):
        import json
        """实时行情"""
        thscode=c_wchar_p(thscode);
        jsonIndicators=c_wchar_p(jsonIndicator);
        jsonparams=c_wchar_p(jsonparam);
        out=iFinD.c_FTQuery_SynRTByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value);
        out=json.loads(out.decode(iFinD.decodeMethod));
        return out;

    @staticmethod
    def FTQuerySynTHS_RealtimeQuotes(thscode,jsonIndicator,jsonparam):
        import json
        """实时行情"""
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                jsonparams=c_char_p(jsonparam);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
        ptr=iFinD.c_FTQueryTHS_SynRTByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod),object_pairs_hook=OrderedDict);
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FTQuerySyn_BasicData(Indicatorname,paramname):
        import json
        """基础数据"""
        indicator=c_wchar_p(Indicatorname);
        params=c_wchar_p(paramname);
        out=iFinD.c_FTQuery_SynBasicDataPy(indicator.value,params.value);
        out=json.loads(out.decode(iFinD.decodeMethod));
        return out;

    @staticmethod
    def FTQuerySynTHS_BasicData(code,Indicatorname,paramname):
        import json
        """基础数据"""
        if(iFinD.isWin):
            if(iFinD.isless3):
                codes=c_char_p(code)
                indicator=c_char_p(Indicatorname);
                params=c_char_p(paramname);
            else:
                codes=c_char_p(bytes(code,'gbk'))
                indicator=c_char_p(bytes(Indicatorname,'gbk'));
                params=c_char_p(bytes(paramname,'gbk'));
        else:
            codes=c_char_p(bytes(code,'utf8'))
            indicator=c_char_p(bytes(Indicatorname,'utf8'));
            params=c_char_p(bytes(paramname,'utf8'));
        ptr=iFinD.c_FTQueryTHS_SynBasicDataPy(codes.value,indicator.value,params.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod),object_pairs_hook=OrderedDict);
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FTQuerySyn_DataPool(DataPoolname,paramname,FunOption):
        import json
        """数据池"""
        DataPoolnames=c_wchar_p(DataPoolname);
        params=c_wchar_p(paramname);
        FunOptions=c_wchar_p(FunOption);
        out=iFinD.c_FTQuery_SynDataPoolByJsonPy(DataPoolnames.value,params.value,FunOptions.value);
        out=json.loads(out.decode(iFinD.decodeMethod));
        return out;

    @staticmethod
    def FTQuerySyn_HisQuote(thscode,jsonIndicator,jsonparam,begintime,endtime):
        import json
        """历史行情"""
        thscode=c_wchar_p(thscode);
        jsonIndicators=c_wchar_p(jsonIndicator);
        jsonparams=c_wchar_p(jsonparam);
        begintime=c_wchar_p(begintime);
        endtime=c_wchar_p(endtime);
        out=iFinD.c_FTQuery_SynHisQuoteByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value);
        out=json.loads(out.decode(iFinD.decodeMethod));
        return out;

    @staticmethod
    def FTQueryTHS_DateSerial(thscode,jsonIndicator,jsonparam,globalparam,begintime,endtime):
        import json
        """日期序列"""
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                jsonparams=c_char_p(jsonparam);
                globalparam=c_char_p(globalparam);
                begintime=c_char_p(begintime);
                endtime=c_char_p(endtime);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
                globalparam=c_char_p(bytes(globalparam,'gbk'));
                begintime=c_char_p(bytes(begintime,'gbk'));
                endtime=c_char_p(bytes(endtime,'gbk'));
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            globalparam=c_char_p(bytes(globalparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));
        ptr=iFinD.c_FTQuery_SynTHS_DateSerialPython(thscode.value,jsonIndicators.value,jsonparams.value,globalparam.value,begintime.value,endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod),object_pairs_hook=OrderedDict);
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FTQuerySynTHS_Snapshot(thscode,jsonIndicator,jsonparam,begintime,endtime):
        import json
        """快照数据"""
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                jsonparams=c_char_p(jsonparam);
                begintime=c_char_p(begintime);
                endtime=c_char_p(endtime);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
                begintime=c_char_p(bytes(begintime,'gbk'));
                endtime=c_char_p(bytes(endtime,'gbk'));
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));
        ptr=iFinD.c_FTQuery_SynSnapshotPy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod),object_pairs_hook=OrderedDict);
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FTQuerySynTHS_DataPool(DataPoolname,paramname,FunOption):
        import json
        """数据池"""
        if(iFinD.isWin):
            if(iFinD.isless3):
                DataPoolnames=c_char_p(DataPoolname);
                params=c_char_p(paramname);
                FunOptions=c_char_p(FunOption);
            else:
                DataPoolnames=c_char_p(bytes(DataPoolname,'gbk'));
                params=c_char_p(bytes(paramname,'gbk'));
                FunOptions=c_char_p(bytes(FunOption,'gbk'));
        else:
            DataPoolnames=c_char_p(bytes(DataPoolname,'utf8'));
            params=c_char_p(bytes(paramname,'utf8'));
            FunOptions=c_char_p(bytes(FunOption,'utf8'));
        ptr=iFinD.c_FTQueryTHS_SynDataPoolByJsonPy(DataPoolnames.value,params.value,FunOptions.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod),object_pairs_hook=OrderedDict);
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FTQuerySynTHS_HisQuote(thscode,jsonIndicator,jsonparam,begintime,endtime):
        import json
        """历史行情"""
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                jsonparams=c_char_p(jsonparam);
                begintime=c_char_p(begintime);
                endtime=c_char_p(endtime);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
                begintime=c_char_p(bytes(begintime,'gbk'));
                endtime=c_char_p(bytes(endtime,'gbk'));
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));        
        ptr=iFinD.c_FTQueryTHS_SynHisQuoteByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod),object_pairs_hook=OrderedDict);
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FT_EDBQuery(indicators, begintime, endtime):
        """查询EDB"""
        import json
        if(iFinD.isWin):
            if(iFinD.isless3):
                Indicators=c_char_p(indicators);
                Begintime=c_char_p(begintime);
                Endtime=c_char_p(endtime);
            else:
                Indicators=c_char_p(bytes(indicators,'gbk'));
                Begintime=c_char_p(bytes(begintime,'gbk'));
                Endtime=c_char_p(bytes(endtime,'gbk'));
        else:
            Indicators=c_char_p(bytes(indicators,'utf8'));
            Begintime=c_char_p(bytes(begintime,'utf8'));
            Endtime=c_char_p(bytes(endtime,'utf8'));
        ptr=iFinD.C_FT_ifinDEDBQuery(Indicators.value, Begintime.value, Endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod),object_pairs_hook=OrderedDict);
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FT_iwencai(query,domain):
        import json
        if(iFinD.isWin):
            if(iFinD.isless3):
                first=c_char_p(query);
                second=c_char_p(domain);
            else:
                first=c_char_p(bytes(query,'gbk'));
                second=c_char_p(bytes(domain,'gbk'));
        else:
             first=c_char_p(bytes(query,'utf8'));
             second=c_char_p(bytes(domain,'utf8'));
        ptr=iFinD.C_FT_ifinDiwencai(first.value,second.value);
        out=cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod),object_pairs_hook=OrderedDict);
        iFinD.c_DeleteMm(ptr);
        return out;   

    @staticmethod
    def FTQueryTHS_BasicData(thsCode, indicatorName, paramOption,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin):
            if(iFinD.isless3):
                thsCode=c_char_p(thsCode);
                indicatorName=c_char_p(indicatorName);
                paramOption=c_char_p(paramOption);
            else:
                thsCode=c_char_p(bytes(thsCode,'gbk'));
                indicatorName=c_char_p(bytes(indicatorName,'gbk'));
                paramOption=c_char_p(bytes(paramOption,'gbk'));
        else:
            thsCode=c_char_p(bytes(thsCode,'utf8'));
            indicatorName=c_char_p(bytes(indicatorName,'utf8'));
            paramOption=c_char_p(bytes(paramOption,'utf8'));
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_BasicDataPy(thsCode.value,indicatorName.value,paramOption.value,pAsyFunc,pUser,byref(pIQueryID)) 
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQueryTHS_DataPool(DataPool,indicatorName,ParamOption,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin):
            if(iFinD.isless3):
                DataPool=c_char_p(DataPool);
                indicatorName=c_char_p(indicatorName);
                ParamOption=c_char_p(ParamOption);
            else:
                DataPool=c_char_p(bytes(DataPool,'gbk'));
                indicatorName=c_char_p(bytes(indicatorName,'gbk'));
                ParamOption=c_char_p(bytes(ParamOption,'gbk')); 
        else:
            DataPool=c_char_p(bytes(DataPool,'utf8'));
            indicatorName=c_char_p(bytes(indicatorName,'utf8'));
            ParamOption=c_char_p(bytes(ParamOption,'utf8'));   
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_DatapoolPy(DataPool.value,indicatorName.value,ParamOption.value,pAsyFunc,pUser,byref(pIQueryID));
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQueryTHS_DateSequence(thscode,jsonIndicator,jsonparam,begintime,endtime,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                jsonparams=c_char_p(jsonparam);
                begintime=c_char_p(begintime);
                endtime=c_char_p(endtime);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
                begintime=c_char_p(bytes(begintime,'gbk'));
                endtime=c_char_p(bytes(endtime,'gbk')); 
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));    
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_DateSequencePy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQueryTHS_RealtimeQuotes(thscode,jsonIndicator,jsonparam,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                jsonparams=c_char_p(jsonparam);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));      
        onlyonce=c_bool(True);
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_RealtimeQuotesPy(thscode.value,jsonIndicators.value,jsonparams.value,onlyonce,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQueryTHS_HighFrequenceSequence(thscode,jsonIndicator,jsonparam,begintime,endtime,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin):
            if(iFinDP.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                jsonparams=c_char_p(jsonparam);
                begintime=c_char_p(begintime);
                endtime=c_char_p(endtime);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
                begintime=c_char_p(bytes(begintime,'gbk'));
                endtime=c_char_p(bytes(endtime,'gbk'));
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));      
        pIQueryID=c_int(0);
        #CBResultsFunc=CMPTHSREALTIMEFUNC(CBResultsFunc);
        #out=iFinD.c_FTQueryTHS_HighFrequenceSequencePy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value,CBResultsFunc,c_void_p(pUser),byref(piQueryID))
        out=iFinD.c_FTQueryTHS_HighFrequenceSequencePy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQueryTHS_HisQuote(thscode,jsonIndicator,jsonparam,begintime,endtime,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                jsonparams=c_char_p(jsonparam);
                begintime=c_char_p(begintime);
                endtime=c_char_p(endtime);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
                begintime=c_char_p(bytes(begintime,'gbk'));
                endtime=c_char_p(bytes(endtime,'gbk')); 
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));     
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_HisQuotePy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQueryTHS_AsyDateSerial(thscode,jsonIndicator,jsonparam,globalparam,begintime,endtime,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                globalp=c_char_p(globalparam);
                jsonparams=c_char_p(jsonparam);
                begintime=c_char_p(begintime);
                endtime=c_char_p(endtime);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                globalp=c_char_p(bytes(globalparam,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
                begintime=c_char_p(bytes(begintime,'gbk'));
                endtime=c_char_p(bytes(endtime,'gbk')); 
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            globalp=c_char_p(bytes(globalparam,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));    
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_THS_AsyDateSerialPython(thscode.value,jsonIndicators.value,jsonparams.value,globalp.value,begintime.value,endtime.value,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQueryTHS_Snapshot(thscode,jsonIndicator,jsonparam,begintime,endtime,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(jsonIndicator);
                jsonparams=c_char_p(jsonparam);
                begintime=c_char_p(begintime);
                endtime=c_char_p(endtime);
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(jsonIndicator,'gbk'));
                jsonparams=c_char_p(bytes(jsonparam,'gbk'));
                begintime=c_char_p(bytes(begintime,'gbk'));
                endtime=c_char_p(bytes(endtime,'gbk')); 
        else:
            thscode=c_char_p(bytes(thscode,'utf8'));
            jsonIndicators=c_char_p(bytes(jsonIndicator,'utf8'));
            jsonparams=c_char_p(bytes(jsonparam,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));     
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_SnapshotPy(thscode.value,jsonIndicators.value,jsonparams.value,begintime.value,endtime.value,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQueryTHS_EDBQuery(indicators, begintime, endtime,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin):
            if(iFinD.isless3):
                indicators=c_char_p(indicators);
                begintime=c_char_p(begintime);
                endtime=c_char_p(endtime);
            else:
                indicators=c_char_p(bytes(indicators,'gbk'));
                begintime=c_char_p(bytes(begintime,'gbk'));
                endtime=c_char_p(bytes(endtime,'gbk')); 
        else:
            indicators=c_char_p(bytes(indicators,'utf8'));
            begintime=c_char_p(bytes(begintime,'utf8'));
            endtime=c_char_p(bytes(endtime,'utf8'));   
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_EDBQueryPy(indicators.value,begintime.value,endtime.value,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQuanyTHS_iwencai(query,domain,CBResultsFunc,pUser,piQueryID):
        if(iFinD.isWin):
            if(iFinD.isless3):
                indicators=c_char_p(query);
                begintime=c_char_p(domain);
            else:
                indicators=c_char_p(bytes(query,'gbk'));
                begintime=c_char_p(bytes(domain,'gbk')); 
        else:
            indicators=c_char_p(bytes(query,'utf8'));
            begintime=c_char_p(bytes(domain,'utf8')); 
        pIQueryID=c_int(0);
        out=iFinD.c_FTQueryTHS_iwencaiPy(indicators.value,begintime.value,pAsyFunc,pUser,byref(pIQueryID))
        iFinD.c_SetValue(pIQueryID,piQueryID)
        if(out==0):
            global g_FunctionMgr
            global g_Funclock
            g_Funclock.acquire();
            g_FunctionMgr[pIQueryID.value] = CBResultsFunc
            g_Funclock.release()
        return out;

    @staticmethod
    def FTQueryTHS_QuotesPushing(thscode,indicator,Callback):
        import json
        """实时行情"""
        global nRegRTID
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(indicator);
                jsonparams=c_char_p('');
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(indicator,'gbk'));
                jsonparams=c_char_p(bytes('','gbk'));
        else:
            thscode=c_char_p(bytes(thscode,'utf-8'));
            jsonIndicators=c_char_p(bytes(indicator,'utf-8'));
            jsonparams=c_char_p(bytes('','utf-8'));
        add=c_bool(1);
        RegId=c_int32(nRegRTID);
        if(Callback == None):
            out=iFinD.C_FTQueryTHS_AsynRTByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,add,pRealTimeFunc,c_void_p(0),byref(RegId));
        else:
            out=iFinD.C_FTQueryTHS_AsynRTByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,add,Callback,c_void_p(0),byref(RegId));
        nRegRTID=RegId.value;
        return out;

    @staticmethod
    def FTQueryTHS_UnQuotesPushing(thscode,indicator):
        import json
        """实时行情"""
        global nRegRTID
        if(iFinD.isWin):
            if(iFinD.isless3):
                thscode=c_char_p(thscode);
                jsonIndicators=c_char_p(indicator);
                jsonparams=c_char_p('');
            else:
                thscode=c_char_p(bytes(thscode,'gbk'));
                jsonIndicators=c_char_p(bytes(indicator,'gbk'));
                jsonparams=c_char_p(bytes('','gbk'));
        else:
            thscode=c_char_p(bytes(thscode,'utf-8'));
            jsonIndicators=c_char_p(bytes(indicator,'utf-8'));
            jsonparams=c_char_p(bytes('','utf-8'));
        add=c_bool(0);
        RegId=c_int32(nRegRTID);
        out=iFinD.C_FTQueryTHS_AsynRTByJsonPy(thscode.value,jsonIndicators.value,jsonparams.value,add,pRealTimeFunc,c_void_p(0),byref(RegId));
        nRegRTID=RegId.value;
        return out;

    @staticmethod
    def FT_DataStastics():
        """查询流量"""
        import json
        ptr=iFinD.C_FT_ifinDDataStatissticsPy();
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FT_GetErrorInfo(errorcode):
        """查询error"""
        import json
        Error=c_int32(errorcode);
        ptr=iFinD.C_FT_ifinDErrorMsg(Error);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FT_DateQuery(exchange, params, begintime, endtime):
        """查询Datequery"""
        import json
        if(iFinD.isWin):
            if(iFinD.isless3):
                Exchange=c_char_p(exchange);
                Params=c_char_p(params);
                Begintime=c_char_p(begintime);
                Endtime=c_char_p(endtime);
            else:
                Exchange=c_char_p(bytes(exchange,'utf8'))
                Params=c_char_p(bytes(params,'utf8'))
                Begintime=c_char_p(bytes(begintime,'utf8'))
                Endtime=c_char_p(bytes(endtime,'utf8'))
        else:
            Exchange=c_char_p(bytes(exchange,'utf8'))
            Params=c_char_p(bytes(params,'utf8'))
            Begintime=c_char_p(bytes(begintime,'utf8'))
            Endtime=c_char_p(bytes(endtime,'utf8'))
        ptr=iFinD.C_FT_ifinDDateQuery(Exchange.value, Params.value, Begintime.value, Endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FT_DateOffset(exchange, params, endtime):
        """查询Dateoffset"""
        import json
        if(iFinD.isWin):
            if(iFinD.isless3):
                Exchange=c_char_p(exchange);
                Params=c_char_p(params);
                Endtime=c_char_p(endtime);
            else:
                Exchange=c_char_p(bytes(exchange,'gbk'))
                Params=c_char_p(bytes(params,'gbk'))
                Endtime=c_char_p(bytes(endtime,'gbk'))
        else:
            Exchange=c_char_p(bytes(exchange,'utf8'))
            Params=c_char_p(bytes(params,'utf8'))
            Endtime=c_char_p(bytes(endtime,'utf8'))
        ptr=iFinD.C_FT_ifinDDateOffset(Exchange.value, Params.value, Endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;

    @staticmethod
    def FT_DateCount(exchange, params, begintime, endtime):
        """查询DateCount"""
        import json
        if(iFinD.isWin):
            if(iFinD.isless3):
                Exchange=c_char_p(exchange);
                Params=c_char_p(params);
                Begintime=c_char_p(begintime);
                Endtime=c_char_p(endtime);
            else:
                Exchange=c_char_p(bytes(exchange,'gbk'))
                Params=c_char_p(bytes(params,'gbk'))
                Begintime=c_char_p(bytes(begintime,'gbk'))
                Endtime=c_char_p(bytes(endtime,'gbk'))
        else:
            Exchange=c_char_p(bytes(exchange,'utf8'))
            Params=c_char_p(bytes(params,'utf8'))
            Begintime=c_char_p(bytes(begintime,'utf8'))
            Endtime=c_char_p(bytes(endtime,'utf8'))
        ptr=iFinD.C_FT_ifinDDateCount(Exchange.value, Params.value, Begintime.value, Endtime.value);
        out = cast(ptr,c_char_p).value
        out=json.loads(out.decode(iFinD.decodeMethod));
        iFinD.c_DeleteMm(ptr);
        return out;

class w(object):
    @classmethod
    def wsi(cls,thscode, jsonIndicator,begintime, endtime,jsonparam):
       return iFinD.FTQuerySynTHS_HighFrequenceSequence(thscode, jsonIndicator, jsonparam, begintime, endtime);