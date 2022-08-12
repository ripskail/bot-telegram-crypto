import json
import threading
import websocket
import requests
import numpy as np
import pandas as pd
from binance.client import Client
import pprint
import ta
import time
import mysql.connector as database
from datetime import date, datetime, timedelta
from tqdm import tqdm
import pandas_ta as taa
import telebot
import surrogates

coins = ('ETHUSDT','XRPUSDT','ADAUSDT','BNBUSDT','SOLUSDT','ICPUSDT','FTTUSDT','RUNEUSDT','LINKUSDT','BTCUSDT')

#client = Client('**************', '***************',testnet = True)
client = Client('**********', '************')
cnx = database.connect(user='**********', password='*********',
                                    host='*************',
                                    database='*********')
bot = telebot.TeleBot('***************')
# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
 
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
 
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)
def get(symbol,interval,since):
        while True:
            #time.sleep(2)
            try:
                frame = pd.DataFrame(client.get_klines(symbol=symbol,
                                               interval={'1h':Client.KLINE_INTERVAL_1HOUR,
                                                         '1m':Client.KLINE_INTERVAL_1MINUTE,
                                                         '3m':Client.KLINE_INTERVAL_3MINUTE,
                                                         '15m':Client.KLINE_INTERVAL_15MINUTE,
                                                         '1d':Client.KLINE_INTERVAL_1DAY,
                                                         '5m':Client.KLINE_INTERVAL_5MINUTE}[interval],
                                              limit=1000))
            except:
                time.sleep(50)
                continue
            frame =frame.iloc[:,:6]
            frame.columns = ['Time', 'Open', 'High', 'Low', 'Close','Volume']
            frame = frame.set_index('Time')
            frame.index = pd.to_datetime(frame.index,unit='ms')
            frame = frame.astype(float)
            return frame
def func_1(a,b):
    return a - b
def func_2(a,b):
    return a * b

def ind(df):
    df['sar_d'] = ta.trend.psar_down(df.High,df.Low,df.Close,step = 0.02,max_step = 0.2,fillna = False)
    df['sar_u'] = ta.trend.psar_up(df.High,df.Low,df.Close,step = 0.02,max_step = 0.2,fillna = False)
    df['kama1'] = ta.momentum.kama(df.Close,window = 14,pow1= 2, pow2 = 20)
    df['kama1d'] = func_1(df.kama1,df.kama1.shift(1))
    df['std1'] =  func_2(1,taa.stdev(df.kama1d,length=14))
    #df['%K'] = ta.momentum.stoch(df.High,df.Low,df.Close,window = 14,smooth_window =3)
    #df['%D'] = df['%K'].rolling(3).mean()
    #df['rsi'] = ta.momentum.rsi(df.Close,window =14)
    #df['stoch'] = ta.momentum.stoch_signal(df.High,df.Low,df.Close,window = 400,smooth_window = 100)
    #df['kst'] = ta.trend.kst(df.Close,roc1=100,roc2=150,roc3=200,roc4=300,window1 =100,window2 =100,window3 =100,window4 =150)
    #df['wma'] = taa.hma(df.Close,length=600)
    #df['cop'] = taa.coppock(df.Close,length=10, fast=11, slow=14)
    #df.dropna(inplace=True)

class Signalss:

    def __init__(self,df,lags):
        self.df =df
        self.lags = lags

    def gettri(self):
        dfx = pd.DataFrame()
        for i in range(self.lags+1):
            mask = (self.df['%K'].shift(i)<20) & (self.df['%D'].shift(i)<20)
            dfx = dfx.append(mask,ignore_index=True)
        return dfx.sum(axis=0)

    def decide(self):
        self.df['Buy'] = np.where(
        #((self.df.rsi<50)),1,0)
        (***********************),1,0)

def idd():
    cnx.reconnect()
    cursor = cnx.cursor()
    sqlid = "SELECT MAX(ID) FROM day1"
    cursor.execute(sqlid)
    myresult = cursor.fetchall()
    for x in myresult:
        if(x[0] is None):
           idm = 1
        else:
           idm = x[0]+1
    cnx.commit()
    cursor.close()
    return idm

def otp(coin,buyprice,dt_string,sell,stop,alert,idi):
    money = surrogates.decode('\ud83d\udcb0')
    plus = surrogates.decode('\u2705')
    x = surrogates.decode('\u274c')
    send_mess = f"<b>Стратегия KAMA Таймфрейм: 1 day\n{str(money)}{str(coin)}\nЦена входа: {str(buyprice)}\n{str(x)}Стоп 10%: {str(stop)}</b>"
    #send_mess = f"<b>Стратегия KAMA\n{str(money)}{str(coin)}\n Цена входа: {str(buyprice)}\n{str(plus)}Профит 3%: {str(sell)}\n{str(x)}Стоп 1%: {str(stop)}</b>"
    #mas = f"Номер: {str(idi)}\nМонета: {str(coin)}\nЦена: {str(buyprice)}\nДата: {str(dt_string)}\nПрофит 9%: {str(sell)}\nСтоп 3%: {str(stop)}"
    cnx.reconnect()
    cursor = cnx.cursor()
    sql = "SELECT id_telegram FROM user WHERE strategy1 = 1"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        bot.send_message(x[0], send_mess, parse_mode='html')
    add = ("INSERT INTO day1 (COIN, BUY, STOP, PROFIT, STATUS, DATE_BUY, DATE_SELL, PRICE_TR,STATUS_TR) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)")
    buytr = buyprice * 1.1
    profitt = buyprice * 1.2
    data = (coin, buyprice, stop, profitt, 0, dt_string, 0,buytr,0)
    cursor.execute(add, data)
    emp_no = cursor.lastrowid
    cnx.commit()
    cursor.close()

def proverka():
    send_mess = f"<b>ПРОВЕРКА</b>"
    cnx.reconnect()
    cursor = cnx.cursor()
    sql = "SELECT id_telegram FROM user WHERE strategy1 = 1 and status = 1"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        bot.send_message(x[0], send_mess, parse_mode='html')

def strategy():
    for coin in coins:
    #for coin in tqdm(coins):
        df = get(coin,'1d','1')
        ind(df)
        print(coin)
        inst = Signalss(df,0)
        inst.decide()
        #print(df.loc[df['Buy'] == 1])
        df['Buy1'] = np.where(
        ( (df.Buy.shift(1) ==0) & (df.Buy.shift(2) ==0) & (df.Buy.shift(3) ==0)
         & (df.Buy.shift(4) ==0)& (df.Buy.shift(5) ==0)& (df.Buy.shift(6) ==0)
         & (df.Buy.shift(7) ==0)& (df.Buy.shift(8) ==0)
         & (df.Buy == 1)),1,0)
        #proverka()
        #print(df.loc[df['Buy1'] == 1])
        if (df.Buy1.iloc[-1] == 1):

            idi = idd()
            tomorrow = datetime.now() -  timedelta(minutes=180)
            dt_string = tomorrow.strftime("%Y-%m-%d %H:%M:%S")
            buyprice = float(df.Close.iloc[-1])
            sell = buyprice * 1.03
            stop = buyprice * 0.9
            alert = buyprice * 1.02
            #mas = f"Монета: {str(coin)}\nЦена: {str(buyprice)}\nДата: {str(dt_string)}\nПрофит: {str(sell)}\nСтоп: {str(stop)}"
            ##---------------------------------------------------
            otp(coin,round(buyprice,4),dt_string,round(sell,4),round(stop,4),round(alert,4),idi)
while True:
        #current_time = time.time()
        #time_to_sleep = 60 - (current_time % 60)
        #time.sleep(time_to_sleep)
        current_time = time.time()
        time_to_sleep = 86400 - (current_time % 86400)
        time.sleep(time_to_sleep)
        strategy()





