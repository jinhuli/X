# coding: utf-8
from iFinDPy import *
from datetime import *
import pandas as pd
import numpy as np
from collections import OrderedDict #保持Key的顺序
thsLogin= THS_iFinDLogin("cfzq267", "592935")

THS_DateSerial(",".join(A_stocks_list[0:10]),'ths_trading_status_stock;ths_listed_days_stock',';','Days:Tradedays,Fill:Previous,Interval:D','2018-07-15','2018-08-15')


def get_stocks(trDate):
    #股票-股票市场类-全部A股(非ST):001005150
    A_stocks= THS_DataPool('block',trDate+";001045011006004",'date:Y,thscode:Y,security_name:Y')  #提取非ST，非PT的全部A股
    A_stocks_list=list(THS_Trans2DataFrame(A_stocks)["THSCODE"])
    status= THS_DateSerial(",".join(A_stocks_list),'ths_trading_status_stock;ths_listed_days_stock',';','Days:Tradedays,Fill:Previous,Interval:D',trDate,trDate)
    #提取股票的交易状态和首发上市日期
    status_pd=THS_Trans2DataFrame(status)
    trade_codes=list(status_pd[(status_pd['ths_trading_status_stock']=='交易')&(status_pd['ths_listed_days_stock']>=900)]["thscode"])  #选取交易且上市时间超过12月的股票,并将index转换成list格式
    return trade_codes

def get_trade_date(start_date, end_date, period='M'):
    data=THS_DateQuery('SSE', 'dateType:0,period:'+period+',dateFormat:0', start_date, end_date)
    return data["tables"]["time"]


#获取因子测试时间段
start_date='20160101'
end_date='20180630'
dates=get_trade_date(start_date, end_date, period='M')

class factor:
    def __init__(self,dates,codeList):
        self.dates=dates
        self.codeList=codeList

    #################估值因子######################
    ##    EP_TTM	净利润TTM/总市值
    ##    EP_LYR	净利润（最新年报）/总市值
    ##    BP_LF	净资产TTM/总市值
    ##    BP_LYR	净资产（最新年报）/总市值
    ##    NCF_TTM	净现金流TTM/总市值
    ##    OCF_TTM	经营性现金流TTM/总市值
    ##    SP_TTM	营业收入TTM/总市值
    ##    SP_LYR	营业收入（最新年报）/总市值
    ##    FCFP_LYR	自由现金流TTM/总市值
    ##    PEG	市盈率/净利润同比增长率 * 100
    ##    EV/EBITDA	企业价值倍数
    ##    DYR	近12个月股息率

    ########################################

    def get_values_factor(self):
        dict_df = OrderedDict()
        factors_value = THS_DateSerial(",".join(trade_codes), 'ths_or_yoy_stock', '',
                       'Days:Tradedays,Fill:Previous,Interval:D','2018-01-22', '2018-08-22')
            # 估值因子value_factor
        factors_value = THS_Trans2DataFrame(factors_value)

        dict_df[date] = factors_value

        factors_values = pd.concat(dict_df.values(), keys=dict_df.keys())
        return factors_values

    ################################################
    ##            规模因子
    # 获取规模因子：对数总市值、对数流通市值

    ################################################
    def get_size_factor(self):
        dict_df = OrderedDict()
        for i in range(len(self.dates) - 1):
            date = self.dates[i]
            A_stocks = get_stocks(date)  # 获取当前时点满足条件的全部A股
            size_factors = w.wss(A_stocks, "val_lnmv,val_lnfloatmv", "tradeDate=" + date)
            factors_names = ['LN_MV', 'LN_FLOAT_MV']
            size_factors = pd.DataFrame(size_factors.Data, index=factors_names, columns=size_factors.Codes).T
            dict_df[date] = size_factors.iloc[:, :]
            # print(dict_df.values())
            # print(dict_df.keys())
        size_factors = pd.concat(dict_df.values(), keys=dict_df.keys())
        return size_factors

    #########################成长因子###########################
    ##       sales_gr_TTM	             营业收入增长率_TTM同比
    ##       net_asset_gr_TTM          	 净资产增长率_TTM同比
    ##       gross_margin_gr_TTM	     毛利率增长率_TTM同比
    ##       net_profit_gr_TTM	         净利润增长率_TTM同比
    ##       total_asset_gr_TTM	         总资产增长率_TTM同比
    ##       net_cash_flow_gr_TTM	     净现金流增长率_TTM同比
    ##       invest_cash_flow_gr_TTM	 资活动产生的现金流量净额增长率_TTM同比
    ##       inance_cash_folw_gr_TTM	 资活动产生的现金流量净额增长率_TTM同比
    ##       operate_cash_flow_gr_TTM	 营活动产生的现金流量净额增长率_TTM同比
    ##       operete_profit_gr_TTM	     营业利润增长率_TTM同比
    ############################################################

    # 获取成长因子
    def get_growth_factors(self):
        dict_df = OrderedDict()
        for i in range(len(self.dates) - 1):
            date = self.dates[i]
            A_stocks = get_stocks(date)  # 获取当前时点满足条件的全部A股
            factors_codes = "fa_orgr_ttm,fa_nagr,fa_gpmgr_ttm,fa_npgr_ttm,fa_tagr,fa_ncgr_ttm,fa_cfigr_ttm,fa_cffgr_ttm,fa_cfogr_ttm,fa_oigr_ttm"
            factors_names = ['sales_gr_TTM', 'net_asset_gr_TTM', 'gross_margin_gr_TTM', 'net_profit_gr_TTM',
                             'total_asset_gr_TTM', 'net_cash_flow_gr_TTM', 'invest_cash_flow_gr_TTM',
                             'finance_cash_folw_gr_TTM', 'operate_cash_flow_gr_TTM', 'operete_profit_gr_TTM']
            growth_factors = w.wss(A_stocks, factors_codes, "tradeDate=" + date)
            growth_factors = pd.DataFrame(growth_factors.Data, index=factors_names, columns=growth_factors.Codes).T
            # growth_factors['eps_growth_TTM']=w.wss(A_stocks, "yoyeps_basic","rptDate="+date+";N=1").Data[0]  #基本每股收益同比增长率
            # growth_factors['roe_growth_TTM']=w.wss(A_stocks, "growth_roe","rptDate="+date+";N=1").Data[0]  #净资产收益率N年同比增长率
            dict_df[date] = growth_factors
        growth_factors = pd.concat(dict_df.values(), keys=dict_df.keys())
        return growth_factors


#############################质量因子#####################################
##      ROE_TTM	净资产收益率
##      ROA_TTM	资产回报率
##      GORSS_PROFIT_MARGIN_TTM	销售毛利率
##      ROC_TTM	资本报酬率
##      NET_PROFIT_MARGIN_TTM	销售净利率
##      TOTAL_ASSETS_TURNOVER_TTM	总资产周转率
##      FIXED_ASSETS_TURNOVER_TTM	固定资产周转率
##      CURRENT_SAAENTS_TURNOVER_TTM	流动资产周转率
#########################################################################
