import stocksGetter as sg
import calcMACD as macd
import emailPropose as ep

try:
    if (0 != sg.get_store_tickers(100000, 10000000)):
        macd.macdCalc()
        ep.get_propose_and_email()
    else:
        print("warning: Fail to get any ticker")
except:
   print("Error")
