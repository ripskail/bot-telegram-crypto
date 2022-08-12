import json
import tabnanny
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

coins = ('AAVEUSDT','ETHUSDT','ATOMUSDT','ETCUSDT','MATICUSDT','LTCUSDT','NEARUSDT','SOLUSDT','UNIUSDT','AVAXUSDT')
#client = Client('******************', '*****************',testnet = True)
client = Client('*********************', '************************************')
cnx = database.connect(user='********', password='********',
                                    host='*********',
                                    database='*********')
bot = telebot.TeleBot('*****************')
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
                                              limit=1500))
            except:
                time.sleep(50)
                continue
            frame =frame.iloc[:,:6]
            frame.columns = ['Time', 'Open', 'High', 'Low', 'Close','Volume']
            frame = frame.set_index('Time')
            frame.index = pd.to_datetime(frame.index,unit='ms')
            frame = frame.astype(float)
            return frame
#upex = hsma * (1 + coif / 100)
#dnex = lsma * (1 - coif / 100)
#low[1] - atr[1] * atr_mult
def func_1(a):
    return a * (1+(-1.7/100))
def func_2(a):
    return a * (1-(-1.7/100))
def func_3(a,b):
    return a - b * 6

def ind(df):
    df['emah'] = taa.rma(df.High, length=100)
    df['emal'] = taa.rma(df.Low, length=100)
    df['hi'] = func_1(df.emah)
    df['lo'] =  func_2(df.emal)
    df['atr'] = taa.atr(df.High, df.Low, df.Close, length=100)
    df['ema'] = taa.ema(df.Close, length=30)
    df['stop'] = func_3(df.Low.shift(6),df.atr.shift(1))
    #df['sar_d'] = ta.trend.psar_down(df.High,df.Low,df.Close,step = 0.02,max_step = 0.2,fillna = False)
    #df['sar_u'] = ta.trend.psar_up(df.High,df.Low,df.Close,step = 0.02,max_step = 0.2,fillna = False)
    #df['kama1'] = ta.momentum.kama(df.Close,window = 14,pow1= 2, pow2 = 20)
    #df['kama1d'] = func_1(df.kama1,df.kama1.shift(1))
    #df['std1'] =  func_2(1,taa.stdev(df.kama1d,length=14))
    #df['sma'] = taa.sma(df.Open, length=10)
    #df['ema8'] = taa.ema(df.Close, length = 8)
    #df['ema14'] = taa.ema(df.Close, length = 14)
    #df['ema50'] = taa.ema(df.Close, length = 50)
    #df['sma2'] = ta.trend.sma_indicator(df.Close, window = 1)
    #df['atr'] =ta.volatility.average_true_range(df.High,df.Low,df.Close,window = 14)
    #df['K'] = ta.momentum.stoch(df.High,df.Low,df.Close,window = 14,smooth_window =3)
    #df['D'] = df['K'].rolling(3).mean()
    #df['rsi'] = ta.momentum.rsi(df.Close,window =14)
    #df['stoch'] = ta.momentum.stoch_signal(df.High,df.Low,df.Close,window = 400,smooth_window = 100)
    #df['kst'] = ta.trend.kst(df.Close,roc1=100,roc2=150,roc3=200,roc4=300,window1 =100,window2 =100,window3 =100,window4 =150)
    #df['wma'] = taa.hma(df.Close,length=600)
    #df['cop'] = taa.coppock(df.Close,length=10, fast=11, slow=14)
    df.dropna(inplace=True)

 #when=close>ema and close[1] < upex and close > upex

class Signalss:

    def __init__(self,df,lags):
        self.df =df
        self.lags = lags

    """ def gettri(self):
        dfx = pd.DataFrame()
        for i in range(self.lags+1):
            mask = (self.df['K'].shift(i)<100) & (self.df['D'].shift(i)<100)
            dfx = dfx.append(mask,ignore_index=True)
        return dfx.sum(axis=0) """

    def decide(self):
        self.df['Buy'] = np.where(
        (*************)&
        (*************)&
        (*************),1,0)
        self.df['Sell'] = np.where(
        (***********) |
        (***********),1,0)
""" for coin in tqdm(coins):
        df = get(coin,'1m','1')
        ind(df)
        inst = Signalss(df,0)
        inst.decide()
        #print(df)
        print(df.loc[df['Buy'] == 1])
#print(df.loc[df['Sell'] == 1])
 """
def idd():
    cnx.reconnect()
    cursor = cnx.cursor()
    sqlid = "SELECT MAX(ID) FROM min1"
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
    send_mess = f"<b>Стратегия EMA Таймфрейм: 1 min\n{str(money)}{str(coin)}\nЦена входа: {str(buyprice)}</b>"
    #send_mess = f"<b>Стратегия KAMA\n{str(money)}{str(coin)}\n Цена входа: {str(buyprice)}\n{str(plus)}Профит 3%: {str(sell)}\n{str(x)}Стоп 1%: {str(stop)}</b>"
    #mas = f"Номер: {str(idi)}\nМонета: {str(coin)}\nЦена: {str(buyprice)}\nДата: {str(dt_string)}\nПрофит 9%: {str(sell)}\nСтоп 3%: {str(stop)}"
    cnx.reconnect()
    cursor = cnx.cursor()
    print("---------------")
    sql = "SELECT id_telegram FROM user WHERE strategy3 = 1"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        bot.send_message(x[0], send_mess, parse_mode='html')
    add = ("INSERT INTO min1 (COIN, BUY, STOP, SELL, STATUS, DATE_BUY, DATE_SELL) VALUES (%s, %s, %s, %s, %s, %s, %s)")
    buytr = buyprice * 1.1
    profitt = buyprice * 1.2
    data = (coin, buyprice, stop, profitt, 0, dt_string, 0)
    cursor.execute(add, data)
    emp_no = cursor.lastrowid
    cnx.commit()
    cursor.close()

def exitt(coin,sell):
    money = surrogates.decode('\ud83d\udcb0')
    plus = surrogates.decode('\u2705')
    xw = surrogates.decode('\u274c')
    send_messs = f"<b>Стратегия EMA - закрытие позиции\n{str(money)}{str(coin)}\nЦена выхода: {str(sell)}</b>"
    cnx.reconnect()
    cursor = cnx.cursor()
    print("---------------")
    sql = "SELECT id_telegram FROM user WHERE strategy3 = 1"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        bot.send_message(x[0], send_messs, parse_mode='html')
    cursor.close()


def proverka():
    send_mess = f"<b>ПРОВЕРКА</b>"
    cnx.reconnect()
    cursor = cnx.cursor()
    sql = "SELECT id_telegram FROM user WHERE strategy3 = 1 and status = 1"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        bot.send_message(x[0], send_mess, parse_mode='html')
def zak():
    global coinexit,pos
    print('coinexit',coinexit)
    df = get(coinexit,'1m','1')
    ind(df)
    inst = Signalss(df,0)
    inst.decide()
    print(df)
    #if(df.Low<(df.atrstop))&(df.Close.iloc[-1]>df.lo|df.Close<df.lo):
    if(df.Sell.iloc[-1] == 1):
        tr = float(df.Close.iloc[-1])
        exitt(coinexit,round(tr,4))
        pos = False
    else:
        pos = True
coinexit = ''
pos = False
def strategy():
    global pos,coinexit
    for coin in tqdm(coins):
        df = get(coin,'1m','1')
        print('5')
        ind(df)
        print(coin)
        inst = Signalss(df,0)
        inst.decide()
        #print(df)
        #time.sleep(300)
        #proverka()
        if (df.Buy.iloc[-1] == 1):
            coinexit = coin
            print("11111111111111")
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
            pos = True

while True:
        print(pos)
        current_time = time.time()
        time_to_sleep = 60 - (current_time % 60)
        time.sleep(time_to_sleep)
        if(pos == True):
           zak()
        else:
           strategy()
        print('pos ',pos)





