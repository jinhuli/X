
# coding: utf-8
from threading import Thread

from EventEngine import Event, EventEngine

def IsTradeDate(date):
    if date in tradedate:
        return 1
    else:
        return 0


class ClockEngine():
    """
    时间推送引擎
    1. 提供bar序列.
    """
    def __init__(self, EventEngine,ClockEvent):
        """
        :param clockEvent:
        :return:
        """
        self.event_engine = EventEngine
        self.clock_engine_thread = Thread(target=self.clocktick, name="ClockEngine")
        self.sleep_time = 1
        self.date=ClockEvent.data
        self.EventType = ClockEvent.event_type

    def start(self):
        self.clock_engine_thread.start()

    def clocktick(self):
        for i in self.date:
            self.push_clock_event(i)
            print("传递时间%s" %i)


    def push_clock_event(self,date):
        event = Event(event_type=self.EventType, data=date)
        self.event_engine.put(event)

    def stop(self):
        self.is_active = False

    def register(self,handle):
        self.event_engine.register(self.EventType,handle)





