# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Add Stock ---")
        symbol = input("Enter Ticker Symbol: ").strip().upper()
        name = input("Enter Company Name: ").strip()
        try:
            shares = float(input("Enter Number of Shares: ").strip())
        except ValueError:
            print("Invalid number of shares.")
            input("Press Enter to Continue ")
            continue
        # Check if symbol already exists
        duplicate = False
        for stock in stock_list:
            if stock.symbol == symbol:
                duplicate = True
        if duplicate:
            print(symbol + " already in portfolio.")
        else:
            new_stock = Stock(symbol, name, shares)
            stock_list.append(new_stock)
        option = input("Stock Added - Enter to Add Another Stock or 0 to Stop: ")


        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        option = input("Enter Menu Option: ")
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol + " ",end="")
    print("]")
    symbol = input("Which stock do you want to buy?: ").strip().upper()
    try:
        shares = float(input("How many shares do you want to buy?: "))
    except ValueError:
        print("Invalid number.")
        input("Press Enter to Continue ")
        return
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            stock.buy(shares)
            found = True
            print("Bought " + str(shares) + " shares of " + symbol + ".")
    if not found:
        print("Symbol not found.")
    input("Press Enter to Continue ")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol + " ",end="")
    print("]")
    symbol = input("Which stock do you want to sell?: ").strip().upper()
    try:
        shares = float(input("How many shares do you want to sell?: "))
    except ValueError:
        print("Invalid number.")
        input("Press Enter to Continue ")
        return
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            if shares > stock.shares:
                print("Cannot sell " + str(shares) + "; only own " + str(stock.shares) + ".")
            else:
                stock.sell(shares)
                print("Sold " + str(shares) + " shares of " + symbol + ".")
    if not found:
        print("Symbol not found.")
    input("Press Enter to Continue ")

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---")
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol + " ",end="")
    print("]")
    symbol = input("Which stock do you want to delete?: ").strip().upper()
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            stock_list.remove(stock)
            found = True
            print(symbol + " deleted.")
    if not found:
        print("Symbol not found.")
    input("Press Enter to Continue ")


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("Stock List ----")
    print("SYMBOL          NAME                     SHARES")
    print("==================================================")
    for stock in stock_list:
        print(f"{stock.symbol:<15} {stock.name:<24} {stock.shares}")
    print()
    input("Press Enter to Continue ***")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data -----")
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol + " ",end="")
    print("]")
    symbol = input("Which stock do you want to use?: ").strip().upper()
    target = None
    for stock in stock_list:
        if stock.symbol == symbol:
            target = stock
    if target is None:
        print("Symbol not found.")
        input("Press Enter to Continue ")
        return
    print("Ready to add data for: ", target.symbol)
    print("Enter Data Separated by Commas - Do Not use Spaces")
    print("Enter a Blank Line to Quit")
    print("Enter Date,Price,Volume")
    print("Example: 1/15/25,135.91,250000000")
    while True:
        line = input("Enter Date,Price,Volume: ").strip()
        if not line:
            break
        parts = line.split(",")
        if len(parts) != 3:
            print("Need exactly 3 values.")
            continue
        try:
            d  = datetime.strptime(parts[0], "%m/%d/%y")
            px = float(parts[1])
            vl = float(parts[2])
            target.add_data(DailyData(d, px, vl))
        except ValueError as e:
            print("Invalid input:", e)

# Display Report for All Stocks
def display_report(stock_data):
    clear_screen()
    print("Stock Report ---")
    for stock in stock_data:
        print("Report for: " + stock.symbol + " " + stock.name)
        print("Shares: " + str(stock.shares))
        if len(stock.DataList) == 0:
            print("*** No daily history.")
        else:
            print(f"  {'Date':<12}{'Close':>12}{'Volume':>18}")
            for daily_data in stock.DataList:
                print(f"  {daily_data.date.strftime('%Y-%m-%d'):<12}"
                      f"{daily_data.close:>12.2f}"
                      f"{int(daily_data.volume):>18,}")
        print()
    print("--- Report Complete ---")
    input("Press Enter to Continue ")


  


# Display Chart
def display_chart(stock_list):
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol + " ",end="")
    print("]")
    symbol = input("Which stock do you want to use?: ").strip().upper()
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
    if not found:
        print("Symbol not found.")
        input("Press Enter to Continue ")
        return
    display_stock_chart(stock_list, symbol)

# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Data to Database")
        print("2 - Load Data from Database")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")
        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("--- Data Saved to Database ---")
            input("Press Enter to Continue ")
        elif option == "2":
            stock_data.load_stock_data(stock_list)
            sortStocks(stock_list)
            print("--- Data Loaded from Database ---")
            input("Press Enter to Continue ")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)


# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieving Stock Data from Yahoo! Finance ---")
    print("This will retrieve data from all stocks in your stock list.")
    if len(stock_list) == 0:
        print("Portfolio is empty. Add a stock first.")
        input("Press Enter to Continue ")
        return
    dateStart = input("Enter starting date: (MM/DD/YY): ").strip()
    dateEnd   = input("Enter ending date:   (MM/DD/YY): ").strip()
    try:
        count = stock_data.retrieve_stock_web(dateStart, dateEnd, stock_list)
        print("Records Retrieved:  " + str(count))
    except Exception as e:
        print("Failed to retrieve:", e)
    input("Press Enter to Continue ")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import CSV file from Yahoo! Finance---")
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol + " ",end="")
    print("]")
    symbol = input("Which stock do you want to use?: ").strip().upper()
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
    if not found:
        print("Symbol not in portfolio. Add it first.")
        input("Press Enter to Continue ")
        return
    filename = input("Enter filename: ").strip()
    try:
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
        print("CSV File Imported")
    except Exception as e:
        print("Import failed:", e)
    input("Press Enter to Continue ")

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()