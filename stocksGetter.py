# List of the stocks we are interested in analyzing. At the time of writing this, 
# it narrows the list of stocks down to 44. 
# If you have a list of your own you would like to use just create a new list instead of using this, 
# for example: tickers = ["FB", "AMZN", ...]
# Necessary Libraries

def get_store_tickers(_mktcap_min = 1200000, _mktcap_max = 10000000):
    import yfinance as yf, pandas as pd, os, time, shutil
    from get_all_tickers import get_tickers as gt
    import calcMACD as macd

    new_data = [] #  This will be a 2D array to hold our stock name and the required action
    # Define a folder to hold the tickers
    macd_dir = os.getcwd()+"/MACD/"
    print(macd_dir)
    if (os.path.isdir(macd_dir)):
        shutil.rmtree(macd_dir)
    os.mkdir(macd_dir)

    tickers = gt.get_tickers_filtered(mktcap_min = _mktcap_min, mktcap_max = _mktcap_max)
    # Check that the amount of tickers isn't more than 1800
    print("The amount of stocks chosen to observe: " + str(len(tickers)))
    # Remove the old folder and create a new one
    # These two lines remove the Stocks folder and then recreate it in order to remove old stocks.
    # if (os.path.isdir(os.getcwd()+Folder)):
    #     shutil.rmtree(os.getcwd()+Folder)
    # os.mkdir(os.getcwd()+Folder)
    # Holds the amount of API calls we executed
    Amount_of_API_Calls = 0
    # This while loop is reponsible for storing the historical data for each ticker in our list. Note that yahoo finance sometimes incurs json.decode errors and because of this we are sleeping for 2 seconds after each iteration, also if a call fails we are going to try to execute it again. Also, do not make more than 2,000 calls per hour or 48,000 calls per day or Yahoo Finance may block your IP. The clause "(Amount_of_API_Calls < 1800)" below will stop the loop from making too many calls to the yfinance API.Prepare for this loop to take some time. It is pausing for 2 seconds after importing each stock.
    Stock_Failure = 0  # Used to make sure we don't waste too many API calls on one Stock ticker that could be having issues
    Stocks_Not_Imported = 0
    # Used to iterate through our list of tickers
    i=0
    print("Saving the required date:")
    while (i < len(tickers)) and (Amount_of_API_Calls < 1800):
        try:
            stock = tickers[i]  # Gets the current stock ticker
            stockName = str(stock)
            temp = yf.Ticker(stockName)
            print(i+1, "out of", str(len(tickers)), "-", stockName)
            result = macd.macdAnalysis(temp.history(period="max"))
            # Check if needs to sell or buy
            if 1 == result:
                new_data.append([stockName, "Sell"])
            elif 2 == result:
                new_data.append([stockName, "Buy"])
            # Pauses the loop for two seconds so we don't cause issues with Yahoo Finance's backend operations
            time.sleep(1)
            Amount_of_API_Calls += 1 
            Stock_Failure = 0
            i += 1  # Iteration to the next ticker
        except ValueError:
            print("Yahoo Finance Backend Error, Attempting to Fix")  # An error occured on Yahoo Finance's backend. We will attempt to retreive the data again
            if Stock_Failure > 5:  # Move on to the next ticker if the current ticker fails more than 5 times
                i+=1
                Stocks_Not_Imported += 1
            Amount_of_API_Calls += 1
            Stock_Failure += 1
    print("The amount of stocks we successfully imported: " + str(i - Stocks_Not_Imported))

    # Prepare the data and write it to csv.
    df = pd.DataFrame(new_data, columns = ['Stock', 'Action'])  # Creates a new dataframe from the new_data list
    df.to_csv(macd_dir+"MACD.csv", index = False)  # Save the dataframe to a csv without the index column

    return i - Stocks_Not_Imported


    