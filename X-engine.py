
from queue import Queue, Empty
from collections import defaultdict
from threading import Thread
from FeedEngine import MarketEngine
from EventEngine import *
from ClockEngine import ClockEngine


class XEngine:
    """回测事件驱动引擎"""
    def __init__(self):
        """初始化事件引擎"""
        # 事件队列
        self.queue = Queue()


        # 事件引擎开关
        self.__active = False

        # 事件引擎处理线程
        self.__thread = Thread(target=self.__run, name="EventEngine.__thread")

        # 事件字典，key 为时间， value 为对应监听事件函数的列表
        self.__handlers = defaultdict(list)
        self.context = {}
        self.clock = ClockEvent("clock",self.context["date"])

        self.marketevent=MarketEvent()

        self.portfolio = None
        self.MarketEngine = MarketEngine(EventEngine(),ClockEngine(EventEngine()))
        self.strategy_list = []


    def __run(self):
        """启动引擎"""
        while self.__active:
            try:
                event = self.queue.get(block=True, timeout=1)
                #handle_thread = Thread(target=self.__process, name="EventEngine.__process", args=(event,))
                #handle_thread.start()
                self.__process(event)
            except Empty:
                feed.load_all_feed(self.feed_list)
                print()



    def __process(self, event):
        """事件处理"""
        # 检查该事件是否有对应的处理函数
        if event.event_type in self.__handlers:
            # 若存在,则按顺序将时间传递给处理函数执行
            for handler in self.__handlers[event.event_type]:
                handler(self,event)



    def start(self):
        """引擎启动"""
        self.__active = True
        self.__thread.start()

    def stop(self):
        """停止引擎"""
        self.__active = False
        self.__thread.join()

    def register(self, event_type, handler):
        """注册事件处理函数监听"""
        if handler not in self.__handlers[event_type]:
            self.__handlers[event_type].append(handler)

    def unregister(self, event_type, handler):
        """注销事件处理函数"""
        handler_list = self.__handlers.get(event_type)
        if handler_list is None:
            return
        if handler in handler_list:
            handler_list.remove(handler)
        if len(handler_list) == 0:
            self.__handlers.pop(event_type)

    def put(self, event):
        self.queue.put(event)

    @property
    def queue_size(self):
        return self.queue.qsize()

    def marketHander(self,event):
        print("把市场事件放到队列中")
        self.queue.put(event)
        print("处理市场事件")
        self._pass_to_market(self,event)

    def _pass_to_market(self, marketevent):
        """因为Strategy模块用到的是marketevent，所以通过marketevent传进去"""
        m = marketevent
        m.fill = self.fill
        self.portfolio.fill = self.fill
        self.broker.fill = self.fill
        m.target = self.target

