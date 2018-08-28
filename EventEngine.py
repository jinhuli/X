from collections import defaultdict
from queue import Queue, Empty
from threading import Thread


class Event:
    """事件对象"""

    def __init__(self, event_type, data=None):
        self.event_type = event_type
        self.data = data


class EventEngine:
    """事件驱动引擎"""

    def __init__(self):
        """初始化事件引擎"""
        # 事件队列
        self.__queue = Queue()

        # 事件引擎开关
        self.__active = False

        # 事件引擎处理线程
        self.__thread = Thread(target=self.__run, name="EventEngine.__thread")

        # 事件字典，key 为时间， value 为对应监听事件函数的列表
        self.__handlers = defaultdict(list)

    def __run(self):
        """启动引擎"""
        while self.__active:
            try:
                event = self.__queue.get(block=True, timeout=1)
                handle_thread = Thread(target=self.__process, name="EventEngine.__process", args=(event,))
                handle_thread.start()
            except Empty:
                pass

    def __process(self, event):
        """事件处理"""
        # 检查该事件是否有对应的处理函数
        if event.event_type in self.__handlers:
            # 若存在,则按顺序将时间传递给处理函数执行
            for handler in self.__handlers[event.event_type]:
                handler(event)

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
        self.__queue.put(event)

    @property
    def queue_size(self):
        return self.__queue.qsize()


class ProcessWrapper(object):
    def __init__(self, strategy):
        """
        @:param
            strategy 策略
        """
        self.__strategy = strategy
        # 事件队列
        self.__event_queue = mp.Queue(10000)
        # 时钟队列
        self.__clock_queue = mp.Queue(10000)
        # 包装进程
        self.__proc = mp.Process(target=self._process)
        self.__proc.start()

    def stop(self):
        """
        停止
        """
        self.__event_queue.put(0)
        self.__clock_queue.put(0)
        self.__proc.join()

    def on_event(self, event):
        """
        推送消息
        """
        # print(event)
        self.__event_queue.put(event)

    def on_clock(self, event):
        """
        推送时钟
        """
        self.__clock_queue.put(event)

    def _process_event(self):
        """
        处理事件
        """
        while True:
            try:
                event = self.__event_queue.get(block=True)
                # 退出
                if event == 0:
                    break
                self.__strategy.run(event)
            except:
                pass

    def _process_clock(self):
        """
        处理时间
        """
        while True:

            try:
                event = self.__clock_queue.get(block=True)
                # 退出
                if event == 0:
                    break
                self.__strategy.clock(event)
            except:
                pass

    def _process(self):
        """
        启动进程
        """
        event_thread = Thread(target=self._process_event, name="ProcessWrapper._process_event")
        event_thread.start()
        clock_thread = Thread(target=self._process_clock, name="ProcessWrapper._process_clock")
        clock_thread.start()

        event_thread.join()
        clock_thread.join()



class MarketEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.type_ = 'Market'


class StrategyEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.type_ = 'strategy'


class PositionEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.type = 'position'
