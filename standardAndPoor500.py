import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader as web


def serialize_sp500_tickers():
    # Wikipedia maintains list of S&P500
    wiki = requests.get(
    	'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    wikiXML = bs.BeautifulSoup(wiki.text, "lxml")
    sp500tableData = wikiXML.find('table', {'class':'wikitable sortable'})
    sp500tickers = []
    for row in sp500tableData.findAll('tr')[1:]: # first row is header
        ticker = row.findAll('td')[0].text
        ticker = ticker[:-1]
        sp500tickers.append(ticker)
    # Maintaining a local-copy for subsequent stock-data extraction 
    with open("Data/sp500tickers.pickle", "wb") as f:
        pickle.dump(sp500tickers, f)
        print('pickle-file made')
    return sp500tickers


''' 
Downloading stock-data 
takes a while, so save it 
'''
def save_sp500_stockdata(
	update_sp500=False, 
	update_sp500_stockdata=False):
    # S&P500 list changes often
    if update_sp500:
        sp500tickers = serialize_sp500_tickers()
        update_sp500_stockdata = True
    else:
        with open("Data/sp500tickers.pickle", "rb") as f:
        	sp500tickers = pickle.load(f)
        if not os.path.exists('Data/stock_data'):
    	    os.makedirs('Data/stock_data')
    # Download to data-dir
    start = dt.datetime(2018,3,20)
    end = dt.datetime(2020,3,20)
    if update_sp500_stockdata:
        skipped_compaies = [] # if any
        for company in sp500tickers:
            if not os.path.exists('Data/stock_data/{}.csv'.format(company)):
                # corrupt data will crash program
                try:
                    tickerData = web.DataReader(company, 'yahoo', start, end)
                    tickerData.to_csv('Data/stock_data/{}.csv'.format(company))
                    print(company)
                except:
                    skipped_compaies.append(company)
                    print('Skipping {} because something went wrong'.format(company))
            else:
                print('We already have Data/stock_data/{}.csv'.format(company))
        print('stock-data download complete\nskipped: ',
         ' '.join(skipped_compaies))

'''
Build one SP500 dataframe,
where each col represents a company
via its `adjusted-close`
'''
def build_sp500_dataframe():
    with open("Data/sp500tickers.pickle","rb") as f:
	    sp500tickers = pickle.load(f)
    
    sp500_df = pd.DataFrame
    for count, ticker in enumerate(sp500tickers):
        if count % 6 == 0:
    	    print(count)
        try:
        	# Just 'adj close' of each company will be used
            stock_col = pd.read_csv('Data/stock_data/{}.csv'.format(ticker))
            stock_col.set_index('Date', inplace=True)
            stock_col.rename(columns = {'Adj Close':ticker}, inplace=True)
            stock_col.drop(
            	['Open','High',
            	'Low','Close',
            	'Volume'], 1, 
            	inplace=True)
            # Merge with SP500 data structure
            if sp500_df.empty:
                sp500_df = stock_col
            else:
                sp500_df = sp500_df.join(stock_col, how='outer')
        
        except FileNotFoundError:
            print('skipping {} because {}.csv is \
            	missing/corrupt'.format(ticker, ticker))
        
    sp500_df.to_csv('Data/sp500_joined_closes.csv')


build_sp500_dataframe()