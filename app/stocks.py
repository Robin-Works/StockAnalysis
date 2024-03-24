import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime, timedelta
import yfinance as yf
import time

# Function to fetch S&P500 data from wikipedia
def fetchSPData() -> pd.DataFrame:
    # Grabs S&P500 table from the wikipedia page
    table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    df = table[0]
    sp500 = df[["Symbol", "Security"]]
    
    return sp500

def preprocessOptionsData(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.dropna(subset=["impliedVolatility"])
    filtered = filtered[filtered["impliedVolatility"] > 0.1]
    
    return filtered

# Symbol is the stock symbol you want data about, tradeType is either "calls" or "puts"
def fetchCallPutData(symbol: str, tradeType="calls") -> pd.DataFrame:
    stock = yf.Ticker(symbol)
    
    # Get today's date plus 6 months from now for relevant options data I want
    today = datetime.today()
    sixMonths = today + timedelta(days=182)
    
    # List 
    optionsDates = [date for date in stock.options if datetime.strptime(date, "%Y-%m-%d") <= sixMonths]
    returnData = pd.DataFrame()
    
    for date in optionsDates:
        opts = stock.option_chain(date)
        tempData = getattr(opts, tradeType)
        tempData["expiration_date"] = date
        returnData = pd.concat([returnData, tempData])
        
    returnData["midpoint"] = (returnData["bid"] + returnData["ask"]) / 2
    returnData = returnData.drop(columns=['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate', 'lastPrice'])
        
    return returnData

# DEPRECATED: Just used for testing :D
def fetchOptionData(sp500Data: pd.DataFrame) -> pd.DataFrame:
    # Grab symbol for options data in sp500 data frame
    symbol = sp500Data.at[0, "Symbol"]
    stock = yf.Ticker(symbol)
    stockData = stock.history(period="1m")
    
    # Get today's date plus 6 months from now for relevant options data I want
    today = datetime.today()
    sixMonths = today + timedelta(days=182)
    
    optionsDates = [date for date in stock.options if datetime.strptime(date, "%Y-%m-%d") <= sixMonths]
    optionsData = pd.DataFrame()
    
    relevantCols = ["contractSymbol", "strike", "lastPrice", "bid", "ask", "percentChange", "volume", "openInterest", "impliedVolatility", "inTheMoney"]
    
    for date in optionsDates:
        optChain = stock.option_chain(date)
        
        # Only grab call and puts where volume is greater than 5
        relevantCalls = optChain.calls[optChain.calls["volume"] > 5].copy()
        relevantPuts = optChain.puts[optChain.puts["volume"] > 5].copy()
        relevantCalls["contract_type"] = "call"
        relevantPuts["contract_type"] = "put"
        
        filteredRelCols = [col for col in relevantCols if col in relevantCalls.columns and col in relevantPuts.columns]
        
        relevantCalls = relevantCalls[filteredRelCols]
        relevantPuts = relevantPuts[filteredRelCols]
        
        combinedData = pd.concat([relevantCalls, relevantPuts], keys=["calls", "puts"])
        combinedData["expiration_date"] = date
        optionsData = pd.concat([optionsData, combinedData])
        
    return optionsData