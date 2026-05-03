#Helper Functions

import matplotlib.pyplot as plt

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    ## Sort the stock list
    stock_list.sort(key=lambda s: s.symbol)


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key=lambda d: d.date)

# Function to create stock chart
def display_stock_chart(stock_list,symbol):
    for stock in stock_list:
        if stock.symbol == symbol:
            if not stock.DataList:
                print(f"No daily data for {symbol}.")
                return
            # Make sure the data is in chronological order before plotting.
            data = sorted(stock.DataList, key=lambda d: d.date)
            dates  = [d.date  for d in data]
            prices = [d.close for d in data]
            plt.figure()
            plt.plot(dates, prices)
            plt.title(stock.name)
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.gcf().autofmt_xdate()
            plt.show()
            return
    print(f"Symbol {symbol} not found.")