
def macdAnalysis(data):
    import pandas as pd, os, glob, shutil
    import pandas_ta as ta
    # Define a folder to hold the tickers
    Data_length = 52
    retVal = 0
    
    if data:
        # Conver the Data to MACD indicator
        data.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
        # Get the last values from the macd and the macd signal.
        macd_prev_sample = data['MACD_12_26_9'].array[Data_length-2]
        macd_current_sample = data['MACD_12_26_9'].array[Data_length-1]
        macd_signal_prev_sample = data['MACDs_12_26_9'].array[Data_length-2]
        macd_signal_current_sample = data['MACDs_12_26_9'].array[Data_length-1]

        if (macd_current_sample > 0) and (macd_signal_current_sample > 0):
            # detect a selling point
            if 1 == crossDetect(macd_signal_prev_sample, macd_signal_current_sample, macd_prev_sample, macd_current_sample):
                retVal = 1 # Sell
        if ((macd_current_sample < 0) and (macd_signal_current_sample < 0)):
            #detect a buying point 
            if 1 == crossDetect(macd_prev_sample, macd_current_sample, macd_signal_prev_sample, macd_signal_current_sample):
                retVal = 2 # Buy

    return retVal


# detects if trajectory a crosses trajectory b from bellow to above
def crossDetect(a_previous, a_current, b_previous, b_current):
    if(a_previous < b_previous) and (a_current > b_current):
        isCross = 1
    else:
        isCross = 0
    return isCross
