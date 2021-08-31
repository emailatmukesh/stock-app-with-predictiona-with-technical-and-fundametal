import yfinance as yf
import streamlit as st
from datetime import date
import numpy as np
import matplotlib.pyplot as plt

today = date.today()

st.write("""
#  Stock Price App with technical indicators and fundamental analysis

Shown are the stock closing price and volume of ticker!

Ticker name should be from **Yahoo finance website** like AAPL, MSFT, GOGL.
For Indian stock, please enter like this BRITANNIA.NS, HEROMOTOCO.NS as mentioned in Yahoo Financial website

""")

tickerSymbol = st.text_input("Enter any ticker symbol", value='HEROMOTOCO.NS')
tickerSymbol.upper()
#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
DF = tickerData.history(period='1d', start='2010-5-31', end=today)
# Open	High	Low	Close	Volume	Dividends	Stock Splits



def moving_avg(DF,a,b):
    """function to calculate MACD
       typical values a = 12; b =26, c =9"""
    df = DF.copy()
    df["Moving_avg-200 days"]=df["Close"].ewm(span=a,min_periods=a).mean()
    df["Moving_avg-50 days"]=df["Close"].ewm(span=b,min_periods=b).mean()
    
    df.dropna(inplace=True)
    return df


df3= moving_avg(DF,200,50)
DF2=df3[['Close',"Moving_avg-200 days","Moving_avg-50 days"]]

st.subheader(f'Chart of {tickerSymbol} with 200 MA and 50 MA')
st.line_chart(DF2)

def BollBnd(DF,n):
    "function to calculate Bollinger Band"
    df = DF.copy()
    df["MA"] = df['Close'].rolling(n).mean()
    df["BB_up"] = df["MA"] + 2*df['Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_dn"] = df["MA"] - 2*df['Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)
    return df

    
dfr=BollBnd(DF,50)
DFR=dfr[['Close',"BB_up","BB_dn", "MA"]]

st.subheader(f'Chart of {tickerSymbol} with Bollinger band')
st.line_chart(DFR)


def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["daily_ret"] = DF["Close"].pct_change()
    df["cum_return"] = (1 + df["daily_ret"]).cumprod()
    n = len(df)/252
    CAGR = ((df["cum_return"][-1])**(1/n) - 1)
    return CAGR



def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    df["daily_ret"] = DF["Close"].pct_change()
    vol = df["daily_ret"].std() * np.sqrt(252)
    return vol

def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["daily_ret"] = DF["Close"].pct_change()
    df["cum_return"] = (1 + df["daily_ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd
    
    

def sharpe(DF,rf):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    df = DF.copy()
    sr = (CAGR(df) - rf)/volatility(df)
    return sr
 

st.sidebar.subheader('Coumpound annual growth return (CARG) from 2010')

st.sidebar.write(CAGR(DF)*100)


st.sidebar.subheader('Annual Volatility  from 2010')

st.sidebar.write(volatility(DF)*100)


st.sidebar.subheader('Maximum drawdown')

st.sidebar.write(max_dd(DF)*100)

st.sidebar.subheader('Sharpe ratio')

st.sidebar.write(sharpe(DF,8))

