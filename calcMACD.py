# OBV Analysis, feel free to replace this section with your own analysis -------------------------------------------------------------------------
import pandas as pd, os, glob, shutil
import pandas_ta as ta
# Define a folder to hold the tickers
Data_length = 52
Folder = "/Daily_Stock_Report/"

def macdCalc():
    Path = os.getcwd() + Folder

    macd_dir = Path+"MACD\\"
    if (os.path.isdir(macd_dir)):
        shutil.rmtree(macd_dir)
    os.mkdir(macd_dir)

    list_files = glob.glob(Path + "*.csv") # Creates a list of all csv filenames in the stocks folder
    new_data = [] #  This will be a 2D array to hold our stock name and OBV score
    interval = 0  # Used for iteration

    while interval < len(list_files):
        # Gets the last Data_length days of trading for the current stock in iteration
        Data = pd.read_csv(list_files[interval]).tail(Data_length)
        # Conver the Data to MACD indicator
        Data.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

        # Get the last values from the macd and the macd signal.
        macd_prev_sample = Data['MACD_12_26_9'].array[Data_length-2]
        macd_current_sample = Data['MACD_12_26_9'].array[Data_length-1]
        macd_signal_prev_sample = Data['MACDs_12_26_9'].array[Data_length-2]
        macd_signal_current_sample = Data['MACDs_12_26_9'].array[Data_length-1]

        Stock_Name = ((os.path.basename(list_files[interval])).split(".csv")[0])  # Get the name of the current stock we are analyzing

        if (macd_current_sample > 0) and (macd_signal_current_sample > 0):
            # detect a selling point
            if 1 == crossDetect(macd_signal_prev_sample, macd_signal_current_sample, macd_prev_sample, macd_current_sample):
                new_data.append([Stock_Name, "Sell"])
        if ((macd_current_sample < 0) and (macd_signal_current_sample < 0)):
            #detect a buying point 
            if 1 == crossDetect(macd_prev_sample, macd_current_sample, macd_signal_prev_sample, macd_signal_current_sample):
                new_data.append([Stock_Name, "Buy"])
        #Go to next stock
        interval += 1
    # Prepare the data and write it to csv.
    df = pd.DataFrame(new_data, columns = ['Stock', 'Action'])  # Creates a new dataframe from the new_data list
    df.to_csv(Path+"MACD/"+"MACD.csv", index = False)  # Save the dataframe to a csv without the index column

# detects if trajectory a crosses trajectory b from bellow to above
def crossDetect(a_previous, a_current, b_previous, b_current):
    if(a_previous < b_previous) and (a_current > b_current):
        isCross = 1
    else:
        isCross = 0
    return isCross