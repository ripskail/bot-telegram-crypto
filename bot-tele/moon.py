import numpy as np
import pandas as pd
from binance.client import Client
from tqdm import tqdm
import pprint
import ta
import time
import datetime
import datetime as DT
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection)
from datetime import date, datetime, timedelta
import sys
import telebot
import surrogates

cnx = connection.MySQLConnection(user='*******', password='**********',
                                     host='***********',
                                     database='***********')
bot = telebot.TeleBot('***********')

news = ('2022-01-02 18:33:29','2022-02-01 05:45:59','2022-03-02 17:34:44',  '2022-04-01 06:24:22', '2022-04-30 20:28:03', '2022-05-30 11:30:14', '2022-06-29 02:52:13', '2022-07-28 17:54:58', '2022-08-27 08:17:04', '2022-09-25 21:54:31',
'2022-10-25 10:48:40', '2022-11-23 22:57:12', '2022-12-23 10:16:51','2023-01-21 20:53:13', '2023-02-20 07:05:47', '2023-03-21 17:23:05','2023-04-20 04:12:29', '2023-05-19 15:53:13', '2023-06-18 04:37:05', '2023-07-17 18:31:46',
'2023-08-16 09:38:06', '2023-09-15 01:39:44', '2023-10-14 17:55:06', '2023-11-13 09:27:22', '2023-12-12 23:31:59','2024-01-11 11:57:21', '2024-02-09 22:59:07', '2024-03-10 09:00:23', '2024-04-08 18:20:48', '2024-05-08 03:21:52', 
'2024-06-06 12:37:40','2024-07-05 22:57:19','2024-08-04 11:12:58', '2024-09-03 01:55:30', '2024-10-02 18:49:13', '2024-11-01 12:47:06', '2024-12-01 06:21:22', '2024-12-30 22:26:44','2025-01-29 12:35:54', '2025-02-28 00:44:45', '2025-03-29 10:57:46', 
'2025-04-27 19:31:05', '2025-05-27 03:02:17','2025-06-25 10:31:32', '2025-07-24 19:11:06', '2025-08-23 06:06:27','2025-09-21 19:54:03', '2025-10-21 12:25:07','2025-11-20 06:47:13','2025-12-20 01:43:17', '2026-01-18 19:51:54', '2026-02-17 12:01:04',
'2026-03-19 01:23:24', '2026-04-17 11:51:44','2026-05-16 20:00:58', '2026-06-15 02:54:04', '2026-07-14 09:43:31','2026-08-12 17:36:39','2026-09-11 03:26:55', '2026-10-10 15:50:01', '2026-11-09 07:02:03', '2026-12-09 00:51:46', '2027-01-07 20:24:18', 
'2027-02-06 15:56:02', '2027-03-08 09:29:24', '2027-04-06 23:51:05', '2027-05-06 10:58:32', '2027-06-04 19:40:15', '2027-07-04 03:01:58','2027-08-02 10:05:08','2027-08-31 17:41:05', '2027-09-30 02:35:59', '2027-10-29 13:36:28', '2027-11-28 03:24:21', 
'2027-12-27 20:12:14', '2028-01-26 15:12:25', '2028-02-25',  '2028-03-26', '2028-04-24','2028-05-24', '2028-06-22', '2028-07-22', '2028-08-20', '2028-09-18', '2028-10-18', '2028-11-16','2028-12-16','2029-01-14','2029-02-13','2029-03-15',  '2029-04-13',
'2029-05-13', '2029-06-12', '2029-07-11',  '2029-08-10', '2029-09-08', '2029-10-07', '2029-11-06', '2029-12-05', '2030-01-04')

fulls = ('2022-01-17 23:48:25','2022-02-16 16:56:29',  '2022-03-18 07:17:32', '2022-04-16 18:55:00',  '2022-05-16 04:14:07', '2022-06-14 11:51:43', '2022-07-13 18:37:35',  '2022-08-12 01:35:41', '2022-09-10 09:59:00', 
'2022-10-09 20:54:56', '2022-11-08 11:02:07', '2022-12-08 04:08:09', '2023-01-06 23:07:52', '2023-02-05 18:28:31', '2023-03-07 12:40:18',  '2023-04-06 04:34:28','2023-05-05 17:34:00', '2023-06-04 03:41:41', 
'2023-07-03 11:38:38', '2023-08-01 18:31:36', '2023-08-31 01:35:33', '2023-09-29 09:57:29',  '2023-10-28 20:24:00',  '2023-11-27 09:16:16',  '2023-12-27 00:33:10', '2024-01-25 17:53:57', '2024-02-24 12:30:22',
'2024-03-25 07:00:16', '2024-04-23 23:48:55',  '2024-05-23 13:53:05', '2024-06-22 01:07:48',  '2024-07-21 10:17:04', '2024-08-19 18:25:44',  '2024-09-18 02:34:24',  '2024-10-17 11:26:21',  '2024-11-15 21:28:28',  
'2024-12-15 09:01:38',  '2025-01-13 22:26:51',  '2025-02-12 13:53:19',  '2025-03-14 06:54:35',  '2025-04-13 00:22:12',  '2025-05-12 16:55:52','2025-06-11 07:43:45', '2025-07-10 20:36:42',  '2025-08-09 07:54:58',  
'2025-09-07 18:08:49',  '2025-10-07 03:47:33',  '2025-11-05 13:19:15',  '2025-12-04 23:14:00', '2026-01-03 10:02:50',  '2026-02-01 22:09:10', '2026-03-03 11:37:49', '2026-04-02 02:11:54',  '2026-05-01 17:23:06', 
'2026-05-31 08:45:07', '2026-06-29 23:56:35', '2026-07-29 14:35:37', '2026-08-28 04:18:26', '2026-09-26 16:48:57',  '2026-10-26 04:11:44', '2026-11-24 14:53:29', '2026-12-24 01:28:09',  '2027-01-22 12:17:18',  
'2027-02-20 23:23:34', '2027-03-22 10:43:43',  '2027-04-20 22:27:04', '2027-05-20 10:58:55',  '2027-06-19 00:44:14',  '2027-07-18 15:44:48',  '2027-08-17 07:28:35',  '2027-09-15 23:03:26',  '2027-10-15 13:46:55', 
'2027-11-14 03:25:50',  '2027-12-13 16:08:42',  '2028-01-12 04:02:59', '2028-02-10 15:03:40',  '2028-03-11 01:05:59',  '2028-04-09 10:26:31',  '2028-05-08 19:48:50',  '2028-06-07 06:08:41', '2028-07-06 18:10:41',
'2028-08-05 08:09:42',  '2028-09-03 23:47:29', '2028-10-03 16:24:53',  '2028-11-02 09:17:15', '2028-12-02 01:40:08',  '2028-12-31 16:48:25',  '2029-01-30 06:03:30',  '2029-02-28 17:10:09',  '2029-03-30 02:26:18', 
'2029-04-28 10:36:41', '2029-05-27 18:37:22', '2029-06-26 03:22:12','2029-07-25 13:35:37','2029-08-24 01:51:05', '2029-09-22 16:29:11','2029-10-22 09:27:27', '2029-11-21 04:02:51', '2029-12-20 22:46:24',
'2030-01-19 15:54:15')

def izme(st):
    alert = surrogates.decode('\ud83d\udea8')
    money = surrogates.decode('\ud83d\udcb0')
    plus = surrogates.decode('\u2705')
    x = surrogates.decode('\u274c')
    if(st==1):
        send_mess = f"<b>{str(alert)}MOON - ******</b>"
    else:
        send_mess = f"<b>{str(alert)}MOON - ******</b>"
    cnx.reconnect()
    cursor = cnx.cursor()
    sql = "SELECT id_telegram FROM user WHERE strategy2 = 1 and status = 1"
    cursor.execute(sql)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x[0])
        bot.send_message(x[0], send_mess, parse_mode='html')
    cursor.close()

while True:
    current_time = time.time()
    time_to_sleep = 86400 - (current_time % 86400)
    time.sleep(time_to_sleep)
    end = datetime.now()
    te = end.strftime("%Y-%m-%d")
    print(te)
    sep = ' '
    time.sleep(10)
    for new in news:
        new1 = new.split(sep,1)[0]
        if(new1 == te):
            izme(0)
            print('new '+new1)
    for full in fulls:
        full1 = full.split(sep,1)[0]
        if(full1 == te):
            izme(1)
            print('full '+full1)


