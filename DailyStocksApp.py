import stocksGetter as sg
# import calcOBV as sa
import calcMACD as macd
import emailPropose as ep


try:
    if (0 != sg.get_store_tickers(4000, 10000000)):
        ep.get_propose_and_email()
    else:
        print("warning: Fail to get any ticker")
except:
    print("Error")