from ib_insync import *
from  configuration.ibtrader_functions import *
from  configuration.ibtrader_settings import * 
from  configuration.ibtrader_stocks import * 
import os, time
import datetime

from dateutil.relativedelta import relativedelta



#/* BY YEAR 
#  BY MONTH 
#   BY WEEK
#   BY DAY 
#   BY 5 MINUTES
#   REALTIME 

 



# 10 AÑOS MAXIMO 
#years = 10
#days_per_year = 365
#now = datetime.datetime.now()
#start = datetime.datetime.now() + relativedelta(years=-5)
end =  datetime.datetime.now()


ib = IB()
ib.connect('127.0.0.1', 7497, clientId=11)

for contract in ib_trader_contracts: 

    # monthly 
    dt_last = ''
    barsList = []
    formatted_end = ""

    while True:
        bars = ib.reqHistoricalData(
            contract,
            endDateTime=end,
            durationStr='5 Y',
            barSizeSetting='1 month',
            whatToShow='TRADES',
            useRTH=getRTH(contract),
            formatDate=1)

        #print  (bars)
        if not bars or dt_last == bars[len(bars)-1].date:
            break
        barsList.append(bars)       
        dt_ini = bars[0].date
        dt_last = bars[len(bars)-1].date       
        formatted_end = dt_last.strftime("%Y_%m_%d")

    # save to CSV file    
    allBars = [b for bars in reversed(barsList) for b in bars]
    df = util.df(allBars)
    print(SETTINGS_REALPATH_STOCK_DATA_MONTH + contract.symbol + "_" + formatted_end + '.csv')

    df.to_csv(SETTINGS_REALPATH_STOCK_DATA_MONTH + contract.symbol + "_" + formatted_end + '.csv')

     # WEEKLY  
    dt_last = ''
    barsList = []
    formatted_end = ""
    while True:
        bars = ib.reqHistoricalData(
            contract,
            endDateTime=end,
            durationStr='5 Y',
            barSizeSetting='1 week',
            whatToShow='TRADES',
            useRTH=getRTH(contract),
            formatDate=1)
        if not bars or dt_last == bars[len(bars)-1].date:
            break
      
        barsList.append(bars)       
        dt_ini = bars[0].date
        dt_last = bars[len(bars)-1].date       
        formatted_end = dt_last.strftime("%Y_%m_%d")


    # save to CSV file
    allBars = [b for bars in reversed(barsList) for b in bars]
    df = util.df(allBars)
    print(SETTINGS_REALPATH_STOCK_DATA_WEEK + contract.symbol + "_" +  formatted_end + '.csv')
    df.to_csv(SETTINGS_REALPATH_STOCK_DATA_WEEK + contract.symbol + "_" +  formatted_end + '.csv')


     # DAILY  
    dt_last = ''
    formatted_end = ""
    barsList = []
    while True:
        bars = ib.reqHistoricalData(
            contract,
            endDateTime=end,
            durationStr='5 Y',
            barSizeSetting='1 day',
            whatToShow='TRADES',
            useRTH=getRTH(contract),
            formatDate=1)
        if not bars or dt_last == bars[len(bars)-1].date:
            break
      
        barsList.append(bars)       
        dt_ini = bars[0].date
        dt_last = bars[len(bars)-1].date       
        formatted_end = dt_last.strftime("%Y_%m_%d")

    # save to CSV file
    allBars = [b for bars in reversed(barsList) for b in bars]
    df = util.df(allBars)
    df.to_csv(SETTINGS_REALPATH_STOCK_DATA_DAY + contract.symbol + "_" + formatted_end + '.csv')


ib.disconnect()