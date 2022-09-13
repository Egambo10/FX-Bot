import fxcmpy
import pandas as pd 
import time
import numpy as np
import datetime as dt
import cufflinks as cf
from pylab import plt
from termcolor import colored as cl
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')

def get_historical_data(symbol, start_date, end_date,TOKEN, server='demo', period='D1'):
    con = fxcmpy.fxcmpy(access_token = TOKEN, log_level = 'error', server = server)
    df = con.get_candles(symbol, period=period,
                start=start_date, end=end_date)
    df = df[['askclose']]
    con.close()
    return df

def ema(prices, periods):
    sma = prices.rolling(periods).mean()
    prices_2 = prices.copy()
    prices_2.iloc[0:periods] = sma[0:periods]
    return prices_2.ewm(span=periods, adjust=False).mean()

def macd(prices, slow, fast, smooth):
    ema_fast = ema(prices, fast)
    ema_slow = ema(prices, slow)
    macd = pd.DataFrame(ema_fast - ema_slow).rename(columns = {'askclose':'macd'})
    signal = pd.DataFrame(ema(macd, smooth)).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd']- signal['signal']).rename(columns = {0:'hist'})
    frames = [macd, signal, hist]
    df = pd.concat(frames, join = 'inner', axis = 1)
    return df

def plot_macd(prices, macd, signal, hist):
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)

    ax1.plot(prices)
    ax2.plot(macd, color = 'grey', linewidth = 1.5, label = 'MACD')
    ax2.plot(signal, color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

    for i in range(len(prices)):
        if str(hist[i])[0] == '-':
            ax2.bar(prices.index[i], hist[i], color = '#ef5350')
        else:
            ax2.bar(prices.index[i], hist[i], color = '#26a69a')

    plt.legend(loc = 'lower right')
    
def implement_macd_strategy(prices, data):    
    buy_price = []
    sell_price = []
    macd_signal = []
    signal = 0

    for i in range(len(data)):
        if data['macd'][i] > data['signal'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        elif data['macd'][i] < data['signal'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            macd_signal.append(0)
            
    return buy_price, sell_price, macd_signal