
# coding: utf-8
from WindPy import w

from collections import deque
from threading import Thread

import pandas as pd
import arrow
from dateutil import tz
from datetime import datetime
import time
from EventEngine import Event, EventEngine

w.start()
tradedate=w.tdays("2018-01-01", "2018-08-07", "").Data[0]
date=w.tdays("2018-01-01", "2018-08-07", "Days=Alldays").Data[0]
def IsTradeDate(date):
    if date in tradedate:
        return 1
    else:
        return 0


for i in date:
    clock={}
    clock[i]=IsTradeDate(i)


class ClockEngine():
    """
    时间推送引擎
    1. 提供bar序列.
    """
    EventType = 'clock_time'
    def __init__(self, event_engine,data):
        """
        :param event_engine:
        :return:
        """
        self.event_engine = event_engine
        self.clock_engine_thread = Thread(target=self.clocktick, name="ClockEngine")
        self.sleep_time = 1
        self.data=data
        self.EventType = "clock_time"

    def start(self):
        self.clock_engine_thread.start()

    def clocktick(self):
        for i in self.data:
            self.push_clock_event(i)
            print("传递时间%s" %i)


    def push_clock_event(self,data):
        event = Event(event_type=self.EventType, data=data)
        self.event_engine.put(event)

    def stop(self):
        self.is_active = False
def h(a):
    print(a)

