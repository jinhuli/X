

from EventEngine import *

class strategy(Event):
    def __init__(self):
        Event.__init__(self)


    def HandleData(self,context):
        pass


    def MySchedule(self,bar_datetime,context,bardata):
        pass

