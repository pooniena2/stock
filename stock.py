import yfinance as yf
import math
import requests
import sys
from colorama import init
from termcolor import cprint 
from pyfiglet import figlet_format
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


# -----------------------------------------------------------
# function: get_name
#
# parameter: symbol1 
# 
#Using the stock code and look up the company full name by using
#the API of finance yahoo. Return full name of the company
# 
#return: x['name']
# -----------------------------------------------------------
def get_name(symbol1):
    symbol = symbol1.upper()
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:

            return x['name']


# -----------------------------------------------------------
# function: stock_info
#
# parameter: data
# 
#Validate if the company exist
#Using the stock code to look up the stock information by using
#yfinance API
# 
#return: stock_price, date, stock_volume if the company exists
#        -1,-1,-1 if the company doesn't exist 
# -----------------------------------------------------------
def stock_info(data):
    stock = yf.Ticker(data)
# get historical market data
    df = stock.history(period="1y",interval="1mo")
    if not df.empty :
        stock_price = []
        date = []
        stock_volume = []
        for i in range (len(df["Close"])):
            if math.isnan(df["Close"][i]):
                pass
            else:
                stock_price.append(df["Close"][i])
                date.append(df.index[i])
                stock_volume.append(df["Volume"][i])
        return stock_price, date, stock_volume
    else:
        print("Wrong stock code!! Please enter again!")
        return -1, -1, -1

def recommendations (data, rec):
    stock = yf.Ticker(data)
    recommendation = stock.recommendations
    if rec == True:
        try:
            print("----------------------------------------------------------------------")
            for i in range (3):
                print("Firm: " + recommendation["Firm"][-i])
                print("To Grade: " + recommendation["To Grade"][-i])
                print("Date: " + str(recommendation.index[-i]))
                print("Action: " + recommendation["Action"][-i])
                print("----------------------------------------------------------------------")
        except:
            print("Cannot fetch stock recommendation")



# -----------------------------------------------------------
# function: stock_graph
#
# parameter: stock_price, date, data, company
# 
#Visualize stock price and stock volume by creating a line graph
#
# 
# -----------------------------------------------------------
def stock_graph(stock_price,date,stock_volume,company):
    graph = make_subplots(rows=2, cols=2,
                    specs=[[{"secondary_y": True}, {"secondary_y": True}],
                           [{"secondary_y": True}, {"secondary_y": True}]])
    graph.add_trace(
    go.Scatter(x=date, y=stock_price, name="stock price"),secondary_y=False)
    graph.add_trace(
    go.Scatter(x=date, y=stock_volume, name="stock volume"),secondary_y=True,)    
    #graph.update_xaxes(title_text="Date")
    graph.update_yaxes(title_text="Stock Price", secondary_y=False)
    graph.update_yaxes(title_text="Stock Volume", secondary_y=True)
    graph.update_layout(
    title_text = company,
    font_family="Courier New",
    font_size = 30,
    font_color="blue",
    title_font_family="Times New Roman",
    title_font_color="red",
    legend_title_font_color="green",
)
    graph.show()

# -----------------------------------------------------------
#print Welcome when user first open the program!!
# -----------------------------------------------------------
def main():
    init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
    cprint(figlet_format('Welcome', font='starwars'), attrs=['bold'])
    data = input("Enter Stock Code: ")
    while data != "exit":
        while True:
            recommendation = input("Do you want to see latest 3 recommendations (Y/N): ")
            if recommendation == "Y":
                rec = True
                break
            elif recommendation == "N":
                rec = False
                break
            else:
                print("Invalid command! Please try to Enter again!")
        stock_price, date, stock_volume = stock_info(data)
        if stock_price != -1 and date != -1 and stock_volume != -1:
            recommendations(data, rec) 
            company = get_name(data)
            stock_graph(stock_price,date,stock_volume,company)
        data = input("Enter Stock Code or type exit to quit the program: ") 


if __name__ == '__main__':
    main()