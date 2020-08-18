from ib_insync import *
from  configuration.ibtrader_functions import *
from  configuration.ibtrader_settings import * 
from  configuration.ibtrader_stocks import * 
import os, time
import datetime

from dateutil.relativedelta import relativedelta


end = ""


ib = IB()
ib.connect('127.0.0.1', 7497, clientId=12)

def onBarUpdate(bars, hasNewBar):
    print(bars[-1])

for contract in ib_trader_contracts: 
    
    bars = ib.reqRealTimeBars(contract, 5, 'MIDPOINT', False)
    bars.updateEvent += onBarUpdate

    ib.sleep(30)
    ib.cancelRealTimeBars(bars)


ib.disconnect()