import pandas as pd

def fetchSPData():
    table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    df = table[0]
    sp500 = df[["Symbol", "Security"]]
    
    return sp500