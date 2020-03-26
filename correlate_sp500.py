import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import os
import pandas as pd
import pandas_datareader as web
import pickle
import requests
import numpy as np

style.use('ggplot')

''' 
UPDATE: 
* check SP500_JOINT_DATA exists; otherwise, execute './generate_sp500_data.py'
'''
SP500_JOINT_DATA = './Data/sp500_joined_closes.csv'


'''
S&P500 companies correlated to each other
in array-form (500x500-matrix)
'''
def make_correlation_data():
    sp500 = pd.read_csv(SP500_JOINT_DATA)
    sp500_corr = sp500.corr() 		# generate correlation table
    sp500_data = sp500_corr.values	# just data, no headers
    return sp500_data, sp500_corr


'''
Visualize stock correlation-strengths:
	* Red Square = negative
	* intermediaries
	* Green Square = positive
(e.g. if [AAPL, TSLA] = green, they're 
(+)'vely correlated)
'''
def visualize_corr_data(sp500_data, sp500_corr):
    # S&P 500 company correlation table [Youtube: sentdex]
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    heatmap = ax.pcolor(sp500_data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(sp500_data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(sp500_data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    column_labels = sp500_corr.columns
    row_labels = sp500_corr.index
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()
    return sp500_corr


'''
Not 100% sure what we're doing here.
'''
def process_data_for_labels(ticker):
    # predict stock-prices 7-days into future
    hm_days = 7
    sp500 = pd.read_csv(SP500_JOINT_DATA, index_col = 0)
    tickers = sp500.columns.tolist()
    sp500.fillna(0, inplace = True)
    # % change
    for i in range(1, hm_days+1):
        sp500['{}_{}d'.format(ticker, i)] = (
    	    (sp500[ticker].shift(-i) - sp500[ticker])/sp500[ticker])
    # fill in missing values (if any)
    sp500.fillna(0, inplace=True)
    return tickers, sp500


def buy_hold_sell():
    # coding my algorithm won't be any good
    # i'll start using Quantopian instead
    # :P
    print('to-do')


# ...........demo............

sp500_data, sp500_corr = make_correlation_data()
visualize_corr_data(sp500_data, sp500_corr)

# ...........demo............