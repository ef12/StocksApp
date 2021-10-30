# Financial
Python scripts for share analysis

### Importing Necessary Libraries
Here is a breakdown of the use-case for each library:
* yfinance: Gather historical/ relevant data on each stock.
* pandas_ta: A library to calculate the MACD
* Pandas: Work with large sets of data.
* Shutil, Glob, and OS: Accessing folders/files on the computer.
* Time: Forcing the program to pause for a period of time.
* Smtplib and SSL: Sending a report over email.
* Get_All_Tickers: Filter through all stocks to get the list you desire.

* Run 
pip install pydirectory

### Email and password
You need to supplay a python file called emailInfo.py with your email and password
This file is added to the git ignore so that the data will not show in the repository.
The file shall contain:
  EMAIL = <your email  address>
  PASSWORD= <your password>