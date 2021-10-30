# OBV Analysis, feel free to replace this section with your own analysis -------------------------------------------------------------------------
import pandas as pd, os, glob
# Define a folder to hold the tickers
Folder = "/Daily_Stock_Report/"

def obvCalc():
    Path = os.getcwd() + Folder
    list_files = (glob.glob(Path + "*.csv")) # Creates a list of all csv filenames in the stocks folder
    new_data = [] #  This will be a 2D array to hold our stock name and OBV score
    interval = 0  # Used for iteration
    while interval < len(list_files):
        Data = pd.read_csv(list_files[interval]).tail(10)  # Gets the last 10 days of trading for the current stock in iteration
        pos_move = []  # List of days that the stock price increased
        neg_move = []  # List of days that the stock price decreaced
        OBV_Value = 0  # Sets the initial OBV_Value to zero
        count = 0
        while (count < 10):  # 10 because we are looking at the last 10 trading days
            if Data.iloc[count,1] < Data.iloc[count,4]:  # True if the stock increased in price
                pos_move.append(count)  # Add the day to the pos_move list
            elif Data.iloc[count,1] > Data.iloc[count,4]:  # True if the stock decreased in price
                neg_move.append(count)  # Add the day to the neg_move list
            count += 1
        count2 = 0
        for i in pos_move:  # Adds the volumes of positive days to OBV_Value, divide by opening price to normalize across all stocks
            OBV_Value = round(OBV_Value + (Data.iloc[i,5]/Data.iloc[i,1]))
        for i in neg_move:  # Subtracts the volumes of negative days from OBV_Value, divide by opening price to normalize across all stocks
            OBV_Value = round(OBV_Value - (Data.iloc[i,5]/Data.iloc[i,1]))
        Stock_Name = ((os.path.basename(list_files[interval])).split(".csv")[0])  # Get the name of the current stock we are analyzing
        new_data.append([Stock_Name, OBV_Value])  # Add the stock name and OBV value to the new_data list
        interval += 1
    df = pd.DataFrame(new_data, columns = ['Stock', 'OBV_Value'])  # Creates a new dataframe from the new_data list
    df["Stocks_Ranked"] = df["OBV_Value"].rank(ascending = False)  # Rank the stocks by their OBV_Values
    df.sort_values("OBV_Value", inplace = True, ascending = False)  # Sort the ranked stocks
    df.to_csv(Path+"OBV_Ranked.csv", index = False)  # Save the dataframe to a csv without the index column
