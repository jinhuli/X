# coding: utf-8
import time

from threading import Thread

from EventEngine import Event


class MarketEngine:
    """行情推送引擎基类"""
    EventType = 'Market'
    PushInterval = 1

    def __init__(self, event_engine, ClockEngine , date):
        self.event_engine = event_engine
        self.clock_engine = ClockEngine
        self.date = date
        self.is_active = True
        self.quotation_thread = Thread(target=self.push_quotation, name="QuotationEngine.%s" % self.EventType)

    def start(self):
        self.quotation_thread.start()

    def stop(self):
        self.is_active = False

    def push_quotation(self):
        while self.is_active:
            try:
                response_data = self.fetch_quotation()
            except:
                self.wait()
                continue
            event = Event(event_type=self.EventType, data=response_data)
            self.event_engine.put(event)
            self.wait()

    def fetch_quotation(self):
        # return your quotation

        return None

    def init(self):
        # do something init
        pass

    def wait(self):
        # for receive quit signal
        for _ in range(int(self.PushInterval) + 1):
            time.sleep(1)


if __name__ == '__main__':
    from WindPy import w
    from EventEngine import Event, EventEngine
    from ClockEngine import ClockEngine
    w.start()
    tradedate = w.tdays("2018-01-01", "2018-04-07", "").Data[0]

    clock = ClockEngine(EventEngine(), tradedate)

    from tools.get_tushare_data import *


    def clockhandel(Event):
        date = Event.data.strftime("%Y-%m-%d")
        bar = tusharebar(date).getOneBar("600008.SH")
        print("传递bar")
        print(bar)



    clock.register(clockhandel)
    clock.start()
    a=clock.event_engine.start()



