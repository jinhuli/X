#-------------------------------------------------------------------
# encoding: UTF-8
from EventEngine import *
from ClockEngine import ClockEngine
from FeedEngine import MarketEngine
from strategy import strategy
from queue import Queue, Empty
#策略名称  某某策略
EVENT_ARTICAL = "Event_Artical"
calendar = []
from WindPy import w

import tushare as ts
ts.get_hist_data('600848.sh'[0:6],"2018-6-10","2018-6-14")
w.start()
tradedate=w.tdays("2018-01-01", "2018-08-07", "").Data[0]

def DataHandler():
    print("启动市场事件处理引擎")

def Strategy():
    print("启动策略事件处理引擎")

def Portfolio():
    print("启动组合事件处理引擎")

def ExecutionHandler():
    print("启动执行事件处理引擎")



class go(object):
    def __init__(self):
        self.date_list=[]
        self.feed_list = []
        self.portfolio_list=[]
        self.strategy_list = []
        self.order_list=[]
        self.context={}
        self.clock = ClockEngine(EventEngine(), tradedate)
        self.Market = MarketEngine(EventEngine(),self.clock)
        self.strategy= strategy()

    def run(self):
        # run_once function
        # Declare the components with respective parameters
        bars = DataHandler()
        strategy = Strategy()
        port = Portfolio()
        broker = ExecutionHandler()
        eventengine = EventEngine()
        while True:
            eventengine.put(event)
        while True:
            try:

                event = events.get(False)
            except queue.Empty:
                break

            else:
                if event.type is 'Market':
                    strategy.calculate_signals(event)
                    port.update_timeindex(event)

                elif event.type is 'Signal':
                    port.update_signal(event)

                elif event.type is 'Order':
                    broker.execute_order(event)

                elif event.type is 'Fill':
                    port.update_fill(event)


    def setContext(self,context={}):

        ##__________________________________________

        context["capital"]    = 10000000  # 回测的初始资金
        context["securities"] = ['000001.SZ']  # 回测标的
        context["start_date"] = "2018-1-1"  # 回测开始时间
        context["end_date"]   = "2018-6-1"  # 回测结束时间
        context["period"]     = 'd'  # 'd' 代表日, 'm'代表分钟   表示行情数据的频率
        context["pos"]        = 1  # 这里可以传一些自己定义的变量  这个表示的是组合1
        context["benchmark"]  = '000906.SH'
        ##___________________________________________
        self.context=context


################### In Loop #######################
    def _check_pending_order(self):
        for f in self.feed_list:    # 判断属于哪个feed_list
            self.fill.check_trade_list(f)
            self.fill.check_order_list(f)


    def _pass_to_market(self,marketevent):
        """因为Strategy模块用到的是marketevent，所以通过marketevent传进去"""
        m = marketevent
        m.fill = self.fill
        self.portfolio.fill = self.fill
        self.broker.fill = self.fill
        m.target = self.target

    def _check_finish_backtest(self,feed_list):
        # if finish, sum(backtest) = 0 + 0 + 0 = 0 -> False
        backtest = [i.continue_backtest for i in feed_list]
        return not sum(backtest)


################### before #######################
    def _adddata(self, feed_list):
        [self.feed_list.append(data) for data in feed_list]

    def _set_portfolio(self, portfolio):
        self.portfolio = portfolio

    def _addstrategy(self, strategy_list):
        [self.strategy_list.append(st) for st in strategy_list]

    def _set_broker(self,broker):
        self.broker = broker()

    def _set_target(self,target):
        self.broker.target = target   # 将target传递给broker使用
        for f in self.feed_list:
            f.target = target

    def set_backtest(self, feed_list,strategy_list,
                        portfolio,broker,target='Forex'):

        # check target
        if target not in ['Forex', 'Futures', 'Stock']:
            raise SyntaxError('Target should be one of "Forex","Futures","Stock"')

        if not isinstance(feed_list,list): feed_list = [feed_list]
        if not isinstance(strategy_list,list): strategy_list = [strategy_list]

        # 因为各个模块之间相互引用，所以要按照顺序add和set模块
        self.target = target
        self._adddata(feed_list)
        self._set_portfolio(portfolio)
        self._addstrategy(strategy_list)
        self._set_broker(broker)
        self._set_target(target)

        self.live_mode=False

    def set_commission(self,commission,margin,mult,commtype='FIX'):
        """
        Forex: commission 表示点差，如commission = 2，表示点差为2
               commtype 默认为固定FIX，不可修改
               margin 表示每手需要多少保证金，如某平台，400倍杠杆每手EUR/USD需要325美金
               mult 处理pips，比如EUR/USD 为1.1659，每pips为0.0001，则 mult=10**5，
                    因为 10**5*0.0001 = 10美金，表示每盈利一个pips，每手赚10美金


        Futures： commission 手续费，可为 ‘FIX’ 或者 ’PCT‘
                  commtype 分为 ‘FIX’ 或者 'PCT',即固定或者按百分比收
                           比如‘FIX’情况下，commission = 12表示每手卖出或者买入，收12元
                              'PCT'情况下，commission = 0.01 表示每手收取 1%
                  margin 表示保证金比率，比如为0.08，表示保证金率为8%
                  mult 表示每个合约的吨数，用于盈亏计算

        Stock： commission 手续费
                comtype 默认为百分比 ‘PCT’，不可修改。
                        比如 commission = 0.01 表示收取购买总市值的 1%
                margin 无
                mult 无
        """
        if self.live_mode:
            raise SyntaxError("Can't set commission in live_mode")
        self.broker.commission = commission
        self.broker.commtype = commtype
        self.broker.margin = margin
        self.broker.mult = mult
        self.fill._mult = mult

        if self.target is 'Futures':
            self.fill.margin = margin  # 期货保证金率比较特殊，要传到fill计算

        for st in self.strategy_list:
            st._mult = mult

    def set_pricetype(self,pricetype ='close'):
        for st in self.strategy_list:
            st.pricetype = pricetype
        self.fill.pricetype = pricetype

    def set_cash(self,cash=100000):
        self.fill.initial_cash = cash

    def set_hedge(self,on=True):
        self.hedge_mode = True

    def set_notify(self,onoff=True):
        self.broker._notify_onoff = onoff


################### after #######################
    def _output_summary(self):
        total = pd.DataFrame(self.fill.total_list)
        total.set_index('date',inplace=True)
        pct_returns = total.pct_change()
        total = total/self.fill.initial_cash
        md,du = create_drawdowns(total['total'])
        d = OrderedDict()
        d['Final_Value'] = round(self.fill.total_list[-1]['total'],3)
        d['Total_return'] = round(d['Final_Value']/self.fill.initial_cash-1,5)
        d['Total_return'] = str(d['Total_return']*100)+'%'
        d['Max_Drawdown'],d['Duration']= md, du
        d['Max_Drawdown'] = str(d['Max_Drawdown']*100)+'%'
        d['Sharpe_Ratio'] = round(create_sharpe_ratio(pct_returns),3)
        print(dict_to_table(d))


    def get_tlog(self):
        completed_list = self.fill.completed_list
        return create_trade_log(completed_list,self.target,
                                self.broker.commtype,
                                self.broker.mult)

    def get_analysis(self,instrument):
        # pd.set_option('display.max_rows', len(x))
        ts=pd.DataFrame(self.feed_list[0].bar_dict[instrument])
        ts.set_index('date',inplace=True)
        ts.index = pd.DatetimeIndex(ts.index)

        dbal=pd.DataFrame(self.fill.total_list[1:])
        dbal.set_index('date',inplace=True)
        dbal.index = pd.DatetimeIndex(dbal.index)

        start = dbal.index[0]
        end = dbal.index[-1]
        capital = self.fill.initial_cash
        tlog = self.get_tlog()
        tlog = tlog[tlog['size'] != 0]
        tlog.reset_index(drop=True,inplace=True)
        st = stats(ts,tlog,dbal,start,end,capital)
        print(dict_to_table(st))

    def oldplot(self,name,instrument=None):
        if instrument is None:
            instrument = self.feed_list[0].instrument
        fig = plotter.matplotlib(self.fill)
        fig.plot(name,instrument)


    def plot(self,instrument,engine='plotly',notebook=False):
        data = plotter.plotly(instrument = instrument,
                        feed_list = self.feed_list,
                        fill = self.fill)
        data.plot(instrument=instrument,engine=engine,notebook=notebook)


