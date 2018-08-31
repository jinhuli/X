# coding: utf-8
#

import multiprocessing as mp
from threading import Thread

import aiohttp
import easyquotation

import time



class DataEngine(object):
    EventType = 'custom'
    PushInterval = 15

    def __init__(self, event_engine, clock_engine, watch_stocks=None, s='sina'):

        self.watch_stocks = watch_stocks
        self.s = s
        self.source = None
        self.is_active=False
        self.__queue = mp.Queue(1000)
        self.is_pause = not clock_engine.is_tradetime_now()
        self._control_thread = Thread(target=self._process_control, name="DataEngine._control_thread")
        self._control_thread.start()
        super(DataEngine, self).__init__(event_engine, clock_engine)

    def _process_control(self):

        while True:
            try:
                msg = self.__queue.get(block=True)
                if msg == "pause":
                    self.is_pause = True
                else:
                    self.is_pause = False
            except:
                pass

    def pause(self):
        self.__queue.put("pause")

    def work(self):
        self.__queue.put("work")

    def init(self):
        # 进行相关的初始化操作
        self.source = 0

    def fetch_quotation(self):
        # 返回行情
        return self.source.stocks(self.watch_stocks)

    def push_quotation(self):
        while self.is_active:
            if self.is_pause:
                time.sleep(1)
                continue
            try:
                response_data = self.fetch_quotation()
            except aiohttp.errors.ServerDisconnectedError:
                time.sleep(self.PushInterval)
                continue
            event = Event(event_type=self.EventType, data=response_data)
            self.event_engine.put(event)
            time.sleep(self.PushInterval)



