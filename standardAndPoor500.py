import bs4 as bs
import pickle
import requests

def save_sp500_tickers():
	resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = bs.BeautifulSoup(resp.text, "lxml")
	tableData = soup.find('table', {'class':'wikitable sortable'})
	tickers = []

	# parse TABLE from S&P webpage
	for row in tableData.findAll('tr')[1:]: # first row is header
		ticker = row.findAll('td')[0].text
		tickers.append(ticker)
	# pickle file
	with open("sp500tickers.pickle", "wb") as f:
		pickle.dump(tickers, f)
	# human readable
	with open("sp500tickers.txt", "wb") as f:
		for ticker in tickers:
			f.write(ticker.encode())
	return tickers

save_sp500_tickers()