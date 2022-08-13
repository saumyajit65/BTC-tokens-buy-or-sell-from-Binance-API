import ccxt
#import seaborn as sns
import pplyr
import config
import pandas as pd
import psutil
pd.set_option("display.max_rows", None, "display.max_columns", None) #to set no limit for columns and rows
import streamlit as st
import warnings
import altair as alt
warnings.filterwarnings('ignore')

#Binance details
#from binance import Client
from binance.spot import Spot
from binance.spot import Spot as Pilent
BINANCE_API_KEY1 = '' #put the api keys from your account here...No brackets or codes needed
BINANCE_SECRET_KEY1 = '' #put the api keys from your account here...No brackets or codes needed

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib.animation import FuncAnimation
from matplotlib import interactive
import numpy as np
from datetime import datetime
import time


#Data extraction 1 declarations
exchange = ccxt.binance({  #this is not binanceus but only binance
    "apiKey": config.BINANCE_API_KEY,
    "secret": config.BINANCE_SECRET_KEY
})
asset = 'BTC/BUSD'

#Data extraction 1 for Volume and price
def getdataextraction1():
    Data = exchange.fetch_ohlcv(asset, timeframe='1m', limit=60, params={})
    df = pd.DataFrame(Data[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Europe/Berlin')
    df['Avg price'] = (df['high'] + df['low']) / 2
    df['difference'] = df['close'] - df['open']
    # df['difference'] = df['Avg price'].diff()
    df['abs_difference'] = abs(df['difference'])
    df['factor'] = df['difference'] / df['abs_difference']
    df = df.fillna(1)
    df['volume'] = df['volume'] * df['factor']
    pd.set_option('expand_frame_repr', False)  # to print dataframe in one line
    df = df.set_index('timestamp')
    df = df.astype(float)
    return df

#For plotting the prices
plt.style.use('ggplot')

def dataplot1(i):
    data1_volume = getdataextraction1()
    plt.cla()  # clear the axes to avoid getting graphs for every step
    colors = ['g' if m > 0 else 'r' for m in data1_volume['volume']]
    plt.plot(data1_volume.index, data1_volume['volume'])
    plt.xlabel("Timestamp of 60 minutes window (Update every 60 seconds)... Remember fibonacci retracement, a fall after a big pump ")
    plt.ylabel("Coins Bought or Sold ('BTC/BUSD')")
    plt.title(f"LIVE BTC Coins traded ('BTC/BUSD')... Take risk during huge volume pump")
    plt.tight_layout()

f1 = plt.figure(2)
Dataplot_show1 = FuncAnimation(plt.gcf(),dataplot1,8000)
plt.tight_layout()
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
plt.show()

