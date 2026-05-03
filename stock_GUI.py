# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

        # Pre-seed with NVDA so demo flows work without adding a stock first.
        self.stock_list.append(Stock("NVDA", "NVIDIA", 100))

 # This section creates the user interface

        # Create Window
        self.root = Tk()
        self.root.title("Ana's Stock Manager") #Replace with a suitable name for your program


        # Menubar
        self.menubar = Menu(self.root)

        # File Menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load Data",  command=self.load)
        self.filemenu.add_command(label="Save Data",  command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit",       command=self.root.quit)

        # Web Menu 
        self.webmenu = Menu(self.menubar, tearoff=0)
        self.webmenu.add_command(
            label="Scrape Data from Yahoo! Finance...",
            command=self.scrape_web_data,
        )
        self.webmenu.add_command(
            label="Import CSV From Yahoo! Finance...",
            command=self.importCSV_web_data,
        )


        # Chart Menu
        self.chartmenu = Menu(self.menubar, tearoff=0)
        self.chartmenu.add_command(label="Show Chart", command=self.display_chart)
 
        # menus to window 
        self.menubar.add_cascade(label="File",  menu=self.filemenu)
        self.menubar.add_cascade(label="Web",   menu=self.webmenu)
        self.menubar.add_cascade(label="Chart", menu=self.chartmenu)
        self.root.config(menu=self.menubar)      


        # Add heading information
        self.headingLabel = Label(
            self.root,
            text="Select a stock from the list",
            font=("Arial", 14, "bold"),
        )
        self.headingLabel.pack(pady=8)

        # Add stock list
        listFrame = Frame(self.root)
        listFrame.pack(side=LEFT, fill=Y, padx=8, pady=4)
        Label(listFrame, text="Portfolio").pack()
        self.stockList = Listbox(listFrame, width=15, height=25, exportselection=False)
        self.stockList.pack(fill=Y, expand=True)
        self.stockList.bind("<<ListboxSelect>>", self.update_data)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)

        
        # Add Tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(side=RIGHT, fill=BOTH, expand=True, padx=8, pady=4)


        # Set Up Main Tab
        self.mainTab = Frame(self.tabs)
        self.tabs.add(self.mainTab, text="Main")

        addFrame = LabelFrame(self.mainTab, text="Add Stock", padx=8, pady=8)
        addFrame.pack(fill=X, padx=6, pady=6)
        Label(addFrame, text="Symbol:").grid(row=0, column=0, sticky=W)
        self.addSymbolEntry = Entry(addFrame, width=10)
        self.addSymbolEntry.grid(row=0, column=1, padx=4)
        Label(addFrame, text="Name:").grid(row=0, column=2, sticky=W)
        self.addNameEntry = Entry(addFrame, width=20)
        self.addNameEntry.grid(row=0, column=3, padx=4)
        Label(addFrame, text="Shares:").grid(row=0, column=4, sticky=W)
        self.addSharesEntry = Entry(addFrame, width=8)
        self.addSharesEntry.grid(row=0, column=5, padx=4)
        Button(addFrame, text="Add", command=self.add_stock).grid(row=0, column=6, padx=4)

        updateFrame = LabelFrame(self.mainTab, text="Buy / Sell Selected Stock", padx=8, pady=8)
        updateFrame.pack(fill=X, padx=6, pady=6)
        Label(updateFrame, text="Shares:").grid(row=0, column=0, sticky=W)
        self.updateSharesEntry = Entry(updateFrame, width=8)
        self.updateSharesEntry.grid(row=0, column=1, padx=4)
        Button(updateFrame, text="Buy",          command=self.buy_shares).grid(row=0, column=2, padx=4)
        Button(updateFrame, text="Sell",         command=self.sell_shares).grid(row=0, column=3, padx=4)
        Button(updateFrame, text="Delete Stock", command=self.delete_stock).grid(row=0, column=4, padx=12)

        dataFrame = LabelFrame(self.mainTab, text="Add Daily Data Manually", padx=8, pady=8)
        dataFrame.pack(fill=X, padx=6, pady=6)
        Label(dataFrame, text="Date,Price,Volume:").grid(row=0, column=0, sticky=W)
        self.dailyEntry = Entry(dataFrame, width=40)
        self.dailyEntry.grid(row=0, column=1, padx=4)
        self.dailyEntry.insert(0, "m/d/yy,price,volume")
        Button(dataFrame, text="Add", command=self.add_daily_data).grid(row=0, column=2, padx=4)

        # Setup History Tab
        self.historyTab = Frame(self.tabs)
        self.tabs.add(self.historyTab, text="History")
        self.dailyDataList = Text(self.historyTab, wrap="none")
        self.dailyDataList.pack(fill=BOTH, expand=True)

        
        # Setup Report Tab
        self.reportTab = Frame(self.tabs)
        self.tabs.add(self.reportTab, text="Report")
        self.stockReport = Text(self.reportTab, wrap="none")
        self.stockReport.pack(fill=BOTH, expand=True)


        ## Call MainLoop
        self.root.mainloop()

# This section provides the functionality
       
    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data","Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()


    # Display stock price and volume history.
    def display_stock_data(self):
        try:
            symbol = self.stockList.get(self.stockList.curselection())
        except Exception:
            return
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                self.dailyDataList.insert(END,"- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END,"=================================\n")
                for daily_data in stock.DataList:
                    row = daily_data.date.strftime("%m/%d/%y") + "   " +  '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                    self.dailyDataList.insert(END,row)

                #display report
                self.stockReport.insert(END, stock.symbol + "  " + stock.name + "\n")
                self.stockReport.insert(END, "Shares: " + str(stock.shares) + "\n")
                self.stockReport.insert(END, "Daily records: " + str(len(stock.DataList)) + "\n\n")
                if len(stock.DataList) > 0:
                    high = stock.DataList[0]
                    low  = stock.DataList[0]
                    first = stock.DataList[0]
                    last  = stock.DataList[-1]
                    for d in stock.DataList:
                        if d.close > high.close:
                            high = d
                        if d.close < low.close:
                            low = d
                    change = last.close - first.close
                    pct    = (change / first.close) * 100
                    self.stockReport.insert(END,
                        "Date range: " + first.date.strftime("%m/%d/%y")
                        + " to " + last.date.strftime("%m/%d/%y") + "\n")
                    self.stockReport.insert(END,
                        "Starting price: ${:0,.2f}\n".format(first.close))
                    self.stockReport.insert(END,
                        "Ending price:   ${:0,.2f}\n".format(last.close))
                    self.stockReport.insert(END,
                        "Change:         ${:0,.2f}  ({:+.2f}%)\n\n".format(change, pct))
                    self.stockReport.insert(END,
                        "High: ${:0,.2f} on ".format(high.close)
                        + high.date.strftime("%m/%d/%y") + "\n")
                    self.stockReport.insert(END,
                        "Low:  ${:0,.2f} on ".format(low.close)
                        + low.date.strftime("%m/%d/%y") + "\n")
                    portfolio_value = stock.shares * last.close
                    self.stockReport.insert(END,
                        "\nCurrent value of " + str(stock.shares) + " shares: ${:0,.2f}\n".format(portfolio_value))

                    

    
    # Add new stock to track.
    def add_stock(self):
        symbol = self.addSymbolEntry.get().strip().upper()
        name = self.addNameEntry.get().strip()
        shares_str = self.addSharesEntry.get().strip()
        if symbol == "":
            messagebox.showerror("Add Stock", "Symbol required.")
            return
        try:
            shares = float(shares_str) if shares_str != "" else 0
        except ValueError:
            messagebox.showerror("Add Stock", "Shares must be a number.")
            return
        for stock in self.stock_list:
            if stock.symbol == symbol:
                messagebox.showwarning("Add Stock", symbol + " already in portfolio.")
                return
        new_stock = Stock(symbol, name, shares)
        self.stock_list.append(new_stock)
        self.stockList.insert(END, symbol)
        self.addSymbolEntry.delete(0, END)
        self.addNameEntry.delete(0, END)
        self.addSharesEntry.delete(0, END)

    # Buy shares of stock.
    def buy_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Buy Shares","Shares Purchased")
        self.updateSharesEntry.delete(0,END)

    # Sell shares of stock.
    def sell_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Sell Shares","Shares Sold")
        self.updateSharesEntry.delete(0,END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
        try:
            symbol = self.stockList.get(self.stockList.curselection())
        except Exception:
            messagebox.showinfo("Delete", "Select a stock first.")
            return
        if not messagebox.askyesno("Delete Stock", "Delete " + symbol + "?"):
            return
        for stock in self.stock_list[:]:
            if stock.symbol == symbol:
                self.stock_list.remove(stock)
        self.stockList.delete(0, END)
        for s in self.stock_list:
            self.stockList.insert(END, s.symbol)
        self.dailyDataList.delete("1.0", END)
        self.stockReport.delete("1.0", END)
        self.headingLabel['text'] = "Select a stock from the list"

     # Add daily data manually from the Main tab.
    def add_daily_data(self):
        try:
            symbol = self.stockList.get(self.stockList.curselection())
        except Exception:
            messagebox.showinfo("Add Daily Data", "Select a stock first.")
            return
        line = self.dailyEntry.get().strip()
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            messagebox.showerror("Format", "Enter date,price,volume (no spaces).")
            return
        try:
            d  = datetime.strptime(parts[0], "%m/%d/%y")
            px = float(parts[1])
            vl = float(parts[2])
        except ValueError as e:
            messagebox.showerror("Bad data", str(e))
            return
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.add_data(DailyData(d, px, vl))
        self.display_stock_data()

    # Get data from web scraping.
    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Starting Date","Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date","Enter Ending Date (m/d/yy")
        try:
            stock_data.retrieve_stock_web(dateFrom,dateTo,self.stock_list)
        except:
            messagebox.showerror("Cannot Get Data from Web","Check Path for Chrome Driver")
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web","Data Retrieved")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        try:
            symbol = self.stockList.get(self.stockList.curselection())
        except Exception:
            messagebox.showinfo("Import CSV", "Select a stock from the list first.")
            return
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list,symbol,filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete",symbol + " Import Complete")
    
    # Display stock price chart.
    def display_chart(self):
        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list,symbol)


def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()