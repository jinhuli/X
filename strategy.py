

from EventEngine import *

class strategy(Event):
    def __init__(self,market,context,bar_data):
        self.data=market
        self.context=context
        Event.__init__(self)


    def handle_data(self,bar_datetime, context, bar_data):
        pass

    def my_schedule(self,bar_datetime, context, bar_data):
        pass



