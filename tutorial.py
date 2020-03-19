'''
"Basic Stock data Manipulation" 
by sentdex on YouTube
'''

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

# finance
# from matplotlib.finance import candlestick_ohlc <== depreciated
import mplfinance as mpf
import matplotlib.dates as mdates

style.use('ggplot')

def main():
	# INO: 2019 -> 2020  
	TICKER, TICKERcsv = 'INO', 'INO.csv'  
	generateCSV(TICKER, TICKERcsv, dt.datetime(2017,1,1), dt.datetime(2020,3,17))
	stockData = pd.read_csv(TICKERcsv, parse_dates = True, index_col = 0)
	ohlcCandleStick(stockData, '30d')


# Generate CSV Stock Data (Yahoo)
# i.e. generateCSV('TSLA', 'TSLA.csv', dt.datetime(2017,1,1), dt.datetime(2020,3,17))
def generateCSV(ticker, filename, start, end):
	try:
		f = open(ticker+'.csv')
		print(ticker+'.csv already exists; delete it to overwrite')
		return
	except:
		print('creating ' + ticker + '.csv')
	df = web.DataReader(ticker, 'yahoo', start, end)
	df.to_csv(ticker+'.csv')

# 30 Moving Avg & Volume 
# i.e. volumeAnd30ma(panda-dataframe-csv-object)
def volumeAnd30ma(csv):
	ax1 = plt.subplot2grid((6,1), (0,0), rowspan=4, colspan=1)
	ax2 = plt.subplot2grid((6,1), (4,0), rowspan=3, colspan=1, sharex=ax1)	# sharex syncs the axes when we zoom-in
	ax1.plot(csv.index, csv['Adj Close'])
	ax1.plot(csv.index, csv['30ma'])
	ax2.plot(csv.index, csv['Volume'])
	# plt.title("30-Day Moving Avg & Volume", loc='center')
	plt.show()

# Plot Candlestick
# takes ohlc dataframe
def ohlcCandleStick(stockData, resampleRate='10d'):
	stockData_ohlc = stockData['Adj Close'].resample(resampleRate).ohlc() # open high low close
	stockData_ohlc.reset_index(inplace=True)
	stockData_ohlc.index = pd.to_datetime(stockData_ohlc.index)

	# default keynames are lower-case, but API uses capitalized keynames
	stockData_ohlc['Open'] = stockData_ohlc.pop('open')
	stockData_ohlc['High'] = stockData_ohlc.pop('high')
	stockData_ohlc['Low'] = stockData_ohlc.pop('low')
	stockData_ohlc['Close'] = stockData_ohlc.pop('close')

	mpf.plot(stockData_ohlc, type='candle')

if __name__ == '__main__':
	main()