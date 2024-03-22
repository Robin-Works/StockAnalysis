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
    
    relevantCols = ["contractSymbol", "strike", "lastPrice", "bid", "ask", "percentChange", "volume", "openInterest", "impliedVolatility", "inTheMoney", "delta", "gamma", "theta", "vega"]
    
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

# Currently pytrends doesn't work so this will have to hold off :(
def fetchTrendData(sp500Data: pd.DataFrame) -> dict:
    # Default pytrend initialization
    trends = TrendReq()
    
    # Time for fetching trend data
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    timeframe = f'{yesterday} {yesterday}'
    
    trendsDict = {}
    
    companies = sp500Data.at[0, "Security"]
    trends.build_payload(kw_list=[companies], timeframe=timeframe)
    
    trendDat = trends.interest_over_time()
    return trendDat.to_dict()
    
    
    # for i in range(0, len(sp500Data), 5):
    #     batch = sp500Data[i:i+5]
    #     companies = batch["Security"].tolist()
    #     trends.build_payload(kw_list=companies, timeframe=timeframe)
        
    #     try:
    #         trendDat = trends.interest_over_time()
    #         for symbol, name in zip(batch["Symbol"], companies):
    #             if name in trendDat.columns:
    #                 trendsDict[symbol] = trendDat[name].iloc[0]
    #             else:
    #                 trendsDict[symbol] = None
    #     except Exception as e:
    #         print(f"Error retrieving data for batch starting at index {i}, {e}")
    #         for symbol in batch["Symbol"]:
    #             trendsDict[symbol] = None
                
    #     time.sleep(60)
    
    # return trendsDict