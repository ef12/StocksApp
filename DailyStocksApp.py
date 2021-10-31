import stocksGetter as sg
import emailPropose as ep


if (0 != sg.get_store_tickers(30000, 10000000)):
	ep.get_propose_and_email()
else:
        print("warning: Fail to get any ticker")
