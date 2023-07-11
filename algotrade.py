import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas_datareader import data as pdr
from sklearn.cluster import KMeans



selected = ["SPY", "QQQ", "IEI", "GLD",'AAPL', 'AMZN', 'MSFT', 'GOOGL', 'FB', 'TSLA', 'NVDA', 'NFLX', 'JPM', 'JNJ',
           'KO', 'PG', 'V', 'MA', 'WMT', 'HD', 'INTC', 'DIS', 'BAC', 'PFE',
           'ADBE', 'CRM', 'ABT', 'NKE', 'PYPL', 'VZ', 'CMCSA', 'UNH', 'T', 'CSCO',
           'ABBV', 'MDT', 'AMGN', 'COST', 'PEP', 'MCD', 'WFC', 'XOM', 'CVX', 'BA',
           'GS', 'MMM', 'HON', 'IBM', 'CAT', 'AAP', 'LMT', 'BA', 'RTX', 'GE',
           'ADSK', 'TMUS', 'BMY', 'ZM', 'ZTS', 'UNP', 'NOW', 'AMD', 'CI', 'AXP',
           'SPG', 'LOW', 'DISCK', 'C', 'ORCL', 'BLK', 'VRTX', 'FIS', 'DHR', 'ADI',
           'SCHW', 'ANTM', 'MO', 'DUK', 'TMO', 'PM', 'UPS', 'CRM', 'COF', 'MMM',
           'SPGI', 'BMY', 'BKNG', 'FDX', 'TMUS', 'AMAT', 'EBAY', 'GM', 'MDLZ', 'ISRG',
           'MET', 'SO', 'PNC', 'ADP', 'PLD', 'LRCX', 'COF', 'HPQ', 'TFC', 'D', 'MMC',
           'SO', 'CTSH', 'COP', 'GD', 'TWTR', 'NEM', 'VRTX', 'CB', 'CCI', 'REGN',
           'FDX', 'TJX', 'AON', 'CHTR', 'MMC', 'NOW', 'USB', 'WBA', 'MCO', 'CI',
           'IQV', 'APD', 'GILD', 'ILMN', 'CTAS', 'LIN', 'EBAY', 'STZ', 'ETSY', 'AMCR',
           'EBAY', 'FISV', 'MO', 'SYF', 'BAX', 'VLO', 'SYK', 'EA', 'REGN', 'NCLH',
           'QRVO', 'CXO', 'PAYX', 'XEL', 'DTE', 'RCL', 'EXPE', 'AMD', 'MKTX', 'BSX',
           'CDNS', 'KEYS', 'SNPS', 'DG', 'OKE', 'BIO', 'RMD', 'EOG', 'FCX', 'CCL',
           'ED', 'IRM', 'GPN', 'DAL', 'LVS', 'CDW', 'CTXS', 'OTIS', 'EXR', 'RF',
           'UAL', 'AFL', 'ARE', 'MNST', 'ES', 'TSN', 'ALGN', 'MRO', 'PRU', 'HLT',
           'DXCM', 'BRK.B', 'DLTR', 'WLTW', 'WDC', 'DLR', 'LEN', 'PAYC', 'MCK',
           'REG', 'ECL', 'MTB']

#print(len(selected))
#print(selected)

def extract_symbols_from_csv(path):
    df = pd.read_csv(path)
    symbols = df["Symbol"].values.tolist()
    return symbols
path = "C:\\Users\\Win10\\Downloads\\nasdaq_screener_1686496792130.csv"

selected = extract_symbols_from_csv(path)

#selected = selected[4087:]
leng = len(selected)




start_year = '2016-12-01'
end_year = '2023-06-16'

yf.pdr_override()
frame = {}
for stock in selected:
        try:
                print(stock)
                data_var = pdr.get_data_yahoo(stock, start_year, end_year)['Adj Close']
                data_var.to_frame()
                frame.update({stock: data_var})
        except Exception as e:
                   print("An error occurred:", str(e))


table = pd.DataFrame(frame)
pd.DataFrame(frame).to_csv('check_Out.csv')

#df = pd.DataFrame()

return_daily =  table.pct_change()





return_daily.to_csv('check_out1.csv')
x = return_daily.mean()*100
print(x)
print(return_daily.std())
return_anuual = (((1+return_daily.mean())**254)-1)
return_anuual.to_csv('check_return_annual.csv')
std_daily_return = return_daily.std()
std_daily_return = std_daily_return*(254**0.5)




