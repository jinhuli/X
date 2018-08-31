
# coding: utf-8
from WindPy import w

from threading import Thread

import pandas as pd

import arrow

from dateutil import tz

from datetime import datetime

import time
w.start()
from EventEngine import Event, EventEngine
from ClockEngine import ClockEngine
from tools.get_tushare_data import *
w.start()
tradedate=w.tdays("2018-01-01", "2018-04-07", "").Data[0]
date=w.tdays("2018-01-01", "2018-04-01", "Days=Alldays").Data[0]

clock=ClockEngine(EventEngine(),tradedate)

from tools.get_tushare_data import *

def clockhandel(Event):
    date=Event.data.strftime("%Y-%m-%d")
    bar=tusharebar(date).getOneBar("600008.SH")
    print("传递bar")
    print(bar)

Event=Event( 'clock_time',date[1])
clockhandel(aa)


clock.register(clockhandel)
clock.start()
clock.event_engine.start()