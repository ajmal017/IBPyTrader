import pandas as pd

from ib_insync import *

from  configuration.ibtrader_functions import *
from  configuration.ibtrader_settings import * 
from  configuration.ibtrader_stocks import * 
import matplotlib.dates as mpl_dates
import pandas_ta as ta

# DATOS 
# SYMBOL
# SUPPORT
# RESISTANCE
# LAST_PRICE
# SMA           ¿200?
# PERIOD DAILY WEEKLY O MONTHLY
# DIVERGENCE_TYPE  BAJISTA O ALCISTA 
# DIVERGENCE_DATE1
# DIVERGENCE_DATE2
# DIVERGENCE_MACD    (S/N)
# DIVERGENCE_INDICATOR  RSI (S/N)
# MACD_VALUE    (S/N)
# RSI_VALUE    (S/N)



# solo si hay divergencias 
dfIBTrader =  pd.DataFrame(columns=['SYMBOL','SUPPORT','SUPPORT_DATE','RESISTANCE','RESISTANCE_DATE','LAST_PRICE', 'SMA','PERIOD','DIVERGENCE_MAC_TYPE','DIVERGENCE_RSI_TYPE',
'DIVERGENCE_MACD_DATE1', 'DIVERGENCE_MACD_DATE2','DIVERGENCE_RSI_DATE1', 'DIVERGENCE_RSI_DATE2', 'MACD_VALUE','RSI_VALUE'])


# https://compraraccionesdebolsa.com/formacion/tecnico/indicadores/divergencias-ocultas/
for contract in ib_trader_contracts: 

    # WEEKLY  
    file_data = getFile(contract.symbol,SETTINGS_REALPATH_STOCK_DATA_WEEK)
    dfWeekly = pd.read_csv(file_data)
    dfWeekly_original = dfWeekly.copy()
    #if necessary convert to datetime
    dfWeekly.date = pd.to_datetime(dfWeekly.date)    
    dfWeekly = dfWeekly[['date', 'open', 'high', 'low', 'close']]
    dfWeekly["date"] = dfWeekly["date"].apply(mpl_dates.date2num)

     # DAILY  
    file_data = getFile(contract.symbol,SETTINGS_REALPATH_STOCK_DATA_DAY)
    dfDaily = pd.read_csv(file_data)
    dfDaily_original = dfDaily.copy()
    #if necessary convert to datetime
    dfDaily.date = pd.to_datetime(dfDaily.date)    
    dfDaily = dfDaily[['date', 'open', 'high', 'low', 'close']]
    dfDaily["date"] = dfDaily["date"].apply(mpl_dates.date2num)


    #resistance_levels_weekly, support_levels_weekly  = getSupportResistances(dfWeekly)
    resistance_levels_daily, support_levels_daily = getSupportResistances(dfDaily)

    last_daily_resistance_value  = dfDaily_original.iloc[resistance_levels_daily[-1][0]]["high"]
    last_daily_resistance_date  = dfDaily_original.iloc[resistance_levels_daily[-1][0]]["date"]
    last_daily_support_value  = dfDaily_original.iloc[support_levels_daily[-1][0]]["high"]
    last_daily_support_date  = dfDaily_original.iloc[support_levels_daily[-1][0]]["date"]
   
   
    last_daily_price   = dfDaily_original.close.iat[-1]  
    period = "DAILY"
    divergence_macd_type = ""   
    divergence_macd_date1 = ""
    divergence_macd_date2 = ""
    divergence_rsi_type = ""   
    divergence_rsi_date1 = ""
    divergence_rsi_date2 = ""
    bDivergence_macd = False
    bDivergence_rsi  = False
    daily_sma = ""
    daily_macd_value = ""
    daily_rsi_value = ""
    #print (dfWeekly_original.iloc[resistance_levels_weekly[-1][0]]["date"] + ":" + str(dfWeekly_original.iloc[resistance_levels_weekly[-1][0]]["high"]))
    #print (dfDaily_original.iloc[resistance_levels_daily[-1][0]]["date"] + ":" + str(dfDaily_original.iloc[resistance_levels_daily[-1][0]]["high"]))

    #print (support_levels_weekly)  
    #print ("Last Support, WEEKLY, DAILY for :"  + contract.symbol)
    #print (dfWeekly_original.iloc[support_levels_weekly[-1][0]]["date"] + ":" +  str(dfWeekly_original.iloc[support_levels_weekly[-1][0]]["low"]))
    #print (dfDaily_original.iloc[support_levels_daily[-1][0]]["date"] + ":" +  str(dfDaily_original.iloc[support_levels_daily[-1][0]]["low"]))

    # pd.DataFrame().ta.indicators()
    
    # DAILY 
    dfsma_daily =  dfDaily.ta.sma(length=200, append=True)
    macddf_daily = dfDaily.ta.macd(fast=12, slow=26, signal=9, min_periods=None, append=True)
    rsidf_daily =  dfDaily.ta.rsi(length=14, append=True)
    #efidf =  dfDaily.ta.efi(length=2, append=True)
    #print ("Sma daily:for :"  + contract.symbol    + " " +  str(dfsma_daily[dfsma_daily.size-1]))  
    #print ("macddf daily:"+ str( macddf_daily[-1:]["MACD_12_26_9"])  )
    #print ("rsidf daily:"+ str( rsidf_daily[rsidf_daily.size-1]))  
    peak_levels_macd,valley_levels_macd = getIndicatorPeaksValleys(macddf_daily,"MACDH_12_26_9")  #  MACD_12_26_9

    daily_sma = dfsma_daily[dfsma_daily.size-1]
    # For example, MACD(fast=12, slow=26, signal=9) will return a DataFrame with columns: ['MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9'].
    daily_macd_value = macddf_daily.MACD_12_26_9.iat[-1]  # AQUI SACAMOS EL MACD , DIVERGENCIA POR HISTOGRAMA

    daily_rsi_value = rsidf_daily[rsidf_daily.size-1]

    dfDivergenceUpperMACD = getIndexUpperDivergence(dfDaily_original,support_levels_daily,valley_levels_macd)
    dfDivergenceLowerMACD = getIndexLowerDivergence(dfDaily_original,resistance_levels_daily,peak_levels_macd)


    if not dfDivergenceUpperMACD.empty:
        bDivergence_macd = True    
        divergence_macd_type = "UPPER"
        print ("Daily listInxDivergenceUpperMACD "  + contract.symbol    + " " )
        # SOLO HASTA EL VALOR N-1
        print ("Last daily resistance :" + str(last_daily_resistance_value))           
        print ("Last daily resistance date :" + str(last_daily_resistance_date))   

        # NOS QUEDAMOS CON LA ULTIMA DIVERGENCIA        
        divergence_macd_date1 = dfDivergenceUpperMACD.DIVERG_DATE1.iat[-1]  
        divergence_macd_date2 = dfDivergenceUpperMACD.DIVERG_DATE2.iat[-1]  

        for i in range(len(dfDivergenceUpperMACD)):       
           print ("########")           
           print (dfDivergenceUpperMACD["DIVERG_DATE1"][i])        
           print (dfDivergenceUpperMACD["DIVERG_DATE2"][i])
           print (dfDivergenceUpperMACD["DIVERG_PRCE1"][i])
           print (dfDivergenceUpperMACD["DIVERG_PRCE2"][i])
    if not dfDivergenceLowerMACD.empty:
        divergence_macd_type = "LOWER"
        bDivergence_macd = True   
        print ("Daily dfDivergenceLowerMACD "  + contract.symbol    + " " )
        print ("Last daily support :" + str(last_daily_support_value))           
        print ("Last daily support date :" + str(last_daily_support_date))       
        # SOLO HASTA EL VALOR N-1
        # NOS QUEDAMOS CON LA ULTIMA DIVERGENCIA 
        divergence_macd_date1 = dfDivergenceLowerMACD.DIVERG_DATE1.iat[-1]  
        divergence_macd_date2 = dfDivergenceLowerMACD.DIVERG_DATE2.iat[-1]  


        for i in range(len(dfDivergenceLowerMACD)):       
           print ("########")           
           print (dfDivergenceLowerMACD["DIVERG_DATE1"][i])        
           print (dfDivergenceLowerMACD["DIVERG_DATE2"][i]) 
           print (dfDivergenceLowerMACD["DIVERG_PRCE1"][i])
           print (dfDivergenceLowerMACD["DIVERG_PRCE2"][i])

    # RSI series 
    dfRSI = pd.DataFrame(rsidf_daily,columns=['RSI_14'])
    
    peak_levels_rsi,valley_levelsrsi = getIndicatorPeaksValleys(dfRSI,"RSI_14")
    #print (support_levels_daily)
    #print (valley_levels_macd)
    dfDivergenceUpperRSI = getIndexUpperDivergence(dfDaily_original,support_levels_daily,valley_levelsrsi)
    dfDivergenceLowerRSI = getIndexLowerDivergence(dfDaily_original,resistance_levels_daily,peak_levels_rsi)

    if not dfDivergenceUpperRSI.empty:
        bDivergence_rsi =  True
        divergence_rsi_type = "UPPER"
        print ("Daily dfDivergenceUpperRSI "  + contract.symbol    + " " )
        # SOLO HASTA EL VALOR N-1
        # NOS QUEDAMOS CON LA ULTIMA DIVERGENCIA 
        divergence_rsi_date1 = dfDivergenceUpperRSI.DIVERG_DATE1.iat[-1]  
        divergence_rsi_date2 = dfDivergenceUpperRSI.DIVERG_DATE2.iat[-1]  
        for i in range(len(dfDivergenceUpperRSI)):       
           print ("########")           
           print (dfDivergenceUpperRSI["DIVERG_DATE1"][i])        
           print (dfDivergenceUpperRSI["DIVERG_DATE2"][i])
           print (dfDivergenceUpperRSI["DIVERG_PRCE1"][i])
           print (dfDivergenceUpperRSI["DIVERG_PRCE2"][i])
    if not dfDivergenceLowerRSI.empty:
        bDivergence_rsi =  True
        divergence_rsi_type = "LOWER"
        print ("Daily dfDivergenceLowerRSI "  + contract.symbol    + " " )
        # SOLO HASTA EL VALOR N-1
        # NOS QUEDAMOS CON LA ULTIMA DIVERGENCIA 
        divergence_rsi_date1 = dfDivergenceLowerRSI.DIVERG_DATE1.iat[-1]  
        divergence_rsi_date2 = dfDivergenceLowerRSI.DIVERG_DATE2.iat[-1]  
        for i in range(len(dfDivergenceLowerRSI)):       
           print ("########")           
           print (dfDivergenceLowerRSI["DIVERG_DATE1"][i])        
           print (dfDivergenceLowerRSI["DIVERG_DATE2"][i])
           print (dfDivergenceLowerRSI["DIVERG_PRCE1"][i])
           print (dfDivergenceLowerRSI["DIVERG_PRCE2"][i])        

    if bDivergence_macd or bDivergence_rsi:
        # solo si hay divergencias 
        #dfIBTrader =  pd.DataFrame(columns=['SYMBOL','SUPPORT','RESISTANCE','LAST_PRICE', 'SMA','PERIOD','DIVERGENCE_MAC_TYPE','DIVERGENCE_RSI_TYPE',
        #'DIVERGENCE_MACD_DATE1', 'DIVERGENCE_MACD_DATE2','DIVERGENCE_RSI_DATE1', 'DIVERGENCE_RSI_DATE2', 'MACD_VALUE','RSI_VALUE'])

        dfIBTrader = dfIBTrader.append({'SYMBOL': contract.symbol, 'SUPPORT': last_daily_support_value, 'SUPPORT_DATE': last_daily_support_date,
                'RESISTANCE' : last_daily_resistance_value, 'RESISTANCE_DATE' : last_daily_resistance_date , 'LAST_PRICE': last_daily_price,
                'SMA' : daily_sma,'PERIOD' :period,'DIVERGENCE_MAC_TYPE' :divergence_macd_type,'DIVERGENCE_RSI_TYPE' :divergence_rsi_type
                ,'DIVERGENCE_MACD_DATE1' :divergence_macd_date1,'DIVERGENCE_MACD_DATE2' :divergence_macd_date2,
                'DIVERGENCE_RSI_DATE1' :divergence_rsi_date1,'DIVERGENCE_RSI_DATE2' :divergence_rsi_date2,
                'MACD_VALUE' :daily_macd_value
                ,'RSI_VALUE' :daily_rsi_value}, ignore_index=True)

    dfIBTrader.to_csv("c:\\IBTRADER_SIGNALS.csv")
   

    # WEEKLY  
    resistance_levels_weekly, support_levels_weekly = getSupportResistances(dfWeekly)

    last_weekly_resistance_value  = dfWeekly_original.iloc[resistance_levels_weekly[-1][0]]["high"]
    last_weekly_resistance_date  = dfWeekly_original.iloc[resistance_levels_weekly[-1][0]]["date"]
    last_weekly_support_value  = dfWeekly_original.iloc[support_levels_weekly[-1][0]]["high"]
    last_weekly_support_date  = dfWeekly_original.iloc[support_levels_weekly[-1][0]]["date"]
   
   
    last_weekly_price   = dfWeekly_original.close.iat[-1]  
    period = "WEEKLY"
    divergence_macd_type = ""   
    divergence_macd_date1 = ""
    divergence_macd_date2 = ""
    divergence_rsi_type = ""   
    divergence_rsi_date1 = ""
    divergence_rsi_date2 = ""
    bDivergence_macd = False
    bDivergence_rsi  = False
    weekly_sma = ""
    weekly_macd_value = ""
    weekly_rsi_value = ""
    #print (dfWeekly_original.iloc[resistance_levels_weekly[-1][0]]["date"] + ":" + str(dfWeekly_original.iloc[resistance_levels_weekly[-1][0]]["high"]))
    #print (dfweekly_original.iloc[resistance_levels_weekly[-1][0]]["date"] + ":" + str(dfweekly_original.iloc[resistance_levels_weekly[-1][0]]["high"]))

    #print (support_levels_weekly)  
    #print ("Last Support, WEEKLY, weekly for :"  + contract.symbol)
    #print (dfWeekly_original.iloc[support_levels_weekly[-1][0]]["date"] + ":" +  str(dfWeekly_original.iloc[support_levels_weekly[-1][0]]["low"]))
    #print (dfweekly_original.iloc[support_levels_weekly[-1][0]]["date"] + ":" +  str(dfweekly_original.iloc[support_levels_weekly[-1][0]]["low"]))

    # pd.DataFrame().ta.indicators()
    
    # weekly 
    dfsma_weekly =  dfWeekly.ta.sma(length=200, append=True)
    macddf_weekly = dfWeekly.ta.macd(fast=12, slow=26, signal=9, min_periods=None, append=True)
    rsidf_weekly =  dfWeekly.ta.rsi(length=14, append=True)
    #efidf =  dfweekly.ta.efi(length=2, append=True)
    #print ("Sma weekly:for :"  + contract.symbol    + " " +  str(dfsma_weekly[dfsma_weekly.size-1]))  
    #print ("macddf weekly:"+ str( macddf_weekly[-1:]["MACD_12_26_9"])  )
    #print ("rsidf weekly:"+ str( rsidf_weekly[rsidf_weekly.size-1]))  
    peak_levels_macd,valley_levels_macd = getIndicatorPeaksValleys(macddf_weekly,"MACDH_12_26_9")  #  MACD_12_26_9

    weekly_sma = dfsma_weekly[dfsma_weekly.size-1]
    # For example, MACD(fast=12, slow=26, signal=9) will return a DataFrame with columns: ['MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9'].
    weekly_macd_value = macddf_weekly.MACD_12_26_9.iat[-1]  # AQUI SACAMOS EL MACD , DIVERGENCIA POR HISTOGRAMA

    weekly_rsi_value = rsidf_weekly[rsidf_weekly.size-1]

    dfDivergenceUpperMACD = getIndexUpperDivergence(dfWeekly_original,support_levels_weekly,valley_levels_macd)
    dfDivergenceLowerMACD = getIndexLowerDivergence(dfWeekly_original,resistance_levels_weekly,peak_levels_macd)


    if not dfDivergenceUpperMACD.empty:
        bDivergence_macd = True    
        divergence_macd_type = "UPPER"
        print ("weekly listInxDivergenceUpperMACD "  + contract.symbol    + " " )
        # SOLO HASTA EL VALOR N-1
        print ("Last weekly resistance :" + str(last_weekly_resistance_value))           
        print ("Last weekly resistance date :" + str(last_weekly_resistance_date))   

        # NOS QUEDAMOS CON LA ULTIMA DIVERGENCIA        
        divergence_macd_date1 = dfDivergenceUpperMACD.DIVERG_DATE1.iat[-1]  
        divergence_macd_date2 = dfDivergenceUpperMACD.DIVERG_DATE2.iat[-1]  

        for i in range(len(dfDivergenceUpperMACD)):       
           print ("########")           
           print (dfDivergenceUpperMACD["DIVERG_DATE1"][i])        
           print (dfDivergenceUpperMACD["DIVERG_DATE2"][i])
           print (dfDivergenceUpperMACD["DIVERG_PRCE1"][i])
           print (dfDivergenceUpperMACD["DIVERG_PRCE2"][i])
    if not dfDivergenceLowerMACD.empty:
        divergence_macd_type = "LOWER"
        bDivergence_macd = True   
        print ("weekly dfDivergenceLowerMACD "  + contract.symbol    + " " )
        print ("Last weekly support :" + str(last_weekly_support_value))           
        print ("Last weekly support date :" + str(last_weekly_support_date))       
        # SOLO HASTA EL VALOR N-1
        # NOS QUEDAMOS CON LA ULTIMA DIVERGENCIA 
        divergence_macd_date1 = dfDivergenceLowerMACD.DIVERG_DATE1.iat[-1]  
        divergence_macd_date2 = dfDivergenceLowerMACD.DIVERG_DATE2.iat[-1]  


        for i in range(len(dfDivergenceLowerMACD)):       
           print ("########")           
           print (dfDivergenceLowerMACD["DIVERG_DATE1"][i])        
           print (dfDivergenceLowerMACD["DIVERG_DATE2"][i]) 
           print (dfDivergenceLowerMACD["DIVERG_PRCE1"][i])
           print (dfDivergenceLowerMACD["DIVERG_PRCE2"][i])

    # RSI series 
    dfRSI = pd.DataFrame(rsidf_weekly,columns=['RSI_14'])
    
    peak_levels_rsi,valley_levelsrsi = getIndicatorPeaksValleys(dfRSI,"RSI_14")
    #print (support_levels_weekly)
    #print (valley_levels_macd)
    dfDivergenceUpperRSI = getIndexUpperDivergence(dfWeekly_original,support_levels_weekly,valley_levelsrsi)
    dfDivergenceLowerRSI = getIndexLowerDivergence(dfWeekly_original,resistance_levels_weekly,peak_levels_rsi)

    if not dfDivergenceUpperRSI.empty:
        bDivergence_rsi =  True
        divergence_rsi_type = "UPPER"
        print ("weekly dfDivergenceUpperRSI "  + contract.symbol    + " " )
        # SOLO HASTA EL VALOR N-1
        # NOS QUEDAMOS CON LA ULTIMA DIVERGENCIA 
        divergence_rsi_date1 = dfDivergenceUpperRSI.DIVERG_DATE1.iat[-1]  
        divergence_rsi_date2 = dfDivergenceUpperRSI.DIVERG_DATE2.iat[-1]  
        for i in range(len(dfDivergenceUpperRSI)):       
           print ("########")           
           print (dfDivergenceUpperRSI["DIVERG_DATE1"][i])        
           print (dfDivergenceUpperRSI["DIVERG_DATE2"][i])
           print (dfDivergenceUpperRSI["DIVERG_PRCE1"][i])
           print (dfDivergenceUpperRSI["DIVERG_PRCE2"][i])
    if not dfDivergenceLowerRSI.empty:
        bDivergence_rsi =  True
        divergence_rsi_type = "LOWER"
        print ("weekly dfDivergenceLowerRSI "  + contract.symbol    + " " )
        # SOLO HASTA EL VALOR N-1
        # NOS QUEDAMOS CON LA ULTIMA DIVERGENCIA 
        divergence_rsi_date1 = dfDivergenceLowerRSI.DIVERG_DATE1.iat[-1]  
        divergence_rsi_date2 = dfDivergenceLowerRSI.DIVERG_DATE2.iat[-1]  
        for i in range(len(dfDivergenceLowerRSI)):       
           print ("########")           
           print (dfDivergenceLowerRSI["DIVERG_DATE1"][i])        
           print (dfDivergenceLowerRSI["DIVERG_DATE2"][i])
           print (dfDivergenceLowerRSI["DIVERG_PRCE1"][i])
           print (dfDivergenceLowerRSI["DIVERG_PRCE2"][i])        

    if bDivergence_macd or bDivergence_rsi:
        # solo si hay divergencias 
        #dfIBTrader =  pd.DataFrame(columns=['SYMBOL','SUPPORT','RESISTANCE','LAST_PRICE', 'SMA','PERIOD','DIVERGENCE_MAC_TYPE','DIVERGENCE_RSI_TYPE',
        #'DIVERGENCE_MACD_DATE1', 'DIVERGENCE_MACD_DATE2','DIVERGENCE_RSI_DATE1', 'DIVERGENCE_RSI_DATE2', 'MACD_VALUE','RSI_VALUE'])

        dfIBTrader = dfIBTrader.append({'SYMBOL': contract.symbol, 'SUPPORT': last_weekly_support_value, 'SUPPORT_DATE': last_weekly_support_date,
                'RESISTANCE' : last_weekly_resistance_value, 'RESISTANCE_DATE' : last_weekly_resistance_date , 'LAST_PRICE': last_weekly_price,
                'SMA' : weekly_sma,'PERIOD' :period,'DIVERGENCE_MAC_TYPE' :divergence_macd_type,'DIVERGENCE_RSI_TYPE' :divergence_rsi_type
                ,'DIVERGENCE_MACD_DATE1' :divergence_macd_date1,'DIVERGENCE_MACD_DATE2' :divergence_macd_date2,
                'DIVERGENCE_RSI_DATE1' :divergence_rsi_date1,'DIVERGENCE_RSI_DATE2' :divergence_rsi_date2,
                'MACD_VALUE' :weekly_macd_value
                ,'RSI_VALUE' :weekly_rsi_value}, ignore_index=True)

    dfIBTrader.to_csv("c:\\IBTRADER_SIGNALS.csv")

    #efidf =  dfDaily.ta.efi(length=2, append=True)
    
