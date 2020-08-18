import pandas as pd

from ib_insync import *

from  configuration.ibtrader_functions import *
from  configuration.ibtrader_settings import * 
from  configuration.ibtrader_stocks import * 
import matplotlib.dates as mpl_dates


for contract in ib_trader_contracts: 

    # WEEKLY  
    file_data = getFile(contract.symbol,SETTINGS_REALPATH_STOCK_DATA_DAY)
    df = pd.read_csv(file_data)
    df_original = df.copy()
    #if necessary convert to datetime
    df.date = pd.to_datetime(df.date)    
    df = df[['date', 'open', 'high', 'low', 'close']]
    df["date"] = df["date"].apply(mpl_dates.date2num)

    support_levels = []
    resistance_levels  = []
    mean_value =  np.mean(df['high'] - df['low'])
    for i in range(2,df.shape[0]-2):
        # Finally, let’s create a list that will contain the levels we find. Each level is a tuple whose first element is the index of the signal candle and the second element is the price value.
        if isSupport(df,i):
            l = df['low'][i]
            if isFarFromLevel(l,support_levels,mean_value):
                support_levels.append((i,l))
        elif isResistance(df,i):
            l = df['high'][i]
            if isFarFromLevel(l,resistance_levels,mean_value):
                resistance_levels.append((i,l))
    print(file_data)
    #print ("Resistances:" )
    #print (resistance_levels)    
    print ("Last Resistances:" )
    print (df_original.iloc[resistance_levels[-1][0]]["date"] + ":" + str(df_original.iloc[resistance_levels[-1][0]]["high"]))
    #print ("Support:")
    #print (support_levels)
    print ("Last Support:" )
    print (df_original.iloc[support_levels[-1][0]]["date"] + ":" +  str(df_original.iloc[support_levels[-1][0]]["low"]))
    

