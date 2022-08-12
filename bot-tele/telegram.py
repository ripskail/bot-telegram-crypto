import bs4
import parser
import telebot
from telebot import types
import mysql.connector as database
from datetime import date, datetime, timedelta
#main variables
bot = telebot.TeleBot('***************')
cnx = database.connect(user='*********', password='************',
                                    host='************',
                                    database='**************')
#handlers message.from_user.username message.chat.id

@bot.message_handler(commands=['help'])
def help(message):
    send_mess = f"<b> /start - вкл оповещений!\n/stop - выкл оповещений\n/menu - Показать меню</b>"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')

@bot.message_handler(commands=['stop'])
def stop(message):
    cnx.reconnect()
    mycursor = cnx.cursor()
    sql = "UPDATE user SET status = 0  WHERE id_telegram ="+str(message.chat.id)
    mycursor.execute(sql)
    cnx.commit()
    mycursor.close()
    send_mess = f"<b> Вы отписались от сигналов!\n{str(message.from_user.first_name)} {message.from_user.last_name}!</b>"
    bot.send_message(message.chat.id, send_mess, parse_mode='html')

@bot.message_handler(commands=['start'])
def start(message):
    cnx.reconnect()
    mycursor = cnx.cursor()
    sql = "SELECT * FROM user WHERE id_telegram ="+str(message.chat.id)
    mycursor.execute(sql)
    mycursor.fetchall()
    count = mycursor.rowcount
    if(count==0):
        tomorrow = datetime.now()
        dt_string = tomorrow.strftime("%Y-%m-%d %H:%M:%S")
        cnx.reconnect()
        cursor = cnx.cursor()
        add = ("INSERT INTO user "
                    "(id_telegram, username, date, status) "
                    "VALUES (%s, %s, %s, %s)")
        if(message.from_user.username is None):
            name = "no"
        else:
            name = message.from_user.username
        data = (message.chat.id,name, dt_string, 1)
        cursor.execute(add, data)
        emp_no = cursor.lastrowid
        cnx.commit()
        cursor.close()
        send_mess = f"<b> Добро пожаловать!, {message.from_user.first_name} {message.from_user.last_name}!</b>"
        bot.send_message(message.chat.id, send_mess, parse_mode='html')
    else:
        cnx.reconnect()
        mycursor = cnx.cursor()
        sql = "UPDATE user SET status = 1  WHERE id_telegram ="+str(message.chat.id)
        mycursor.execute(sql)
        cnx.commit()
        mycursor.close()
        send_mess = f"<b> Вы подписаны на сигналы!\n{str(message.from_user.first_name)} {message.from_user.last_name}!</b>"
        bot.send_message(message.chat.id, send_mess, parse_mode='html')

@bot.message_handler(commands=['menu'])
def func(message):
     cnx.reconnect()
     cursor = cnx.cursor()
     query = ("SELECT strategy1,strategy2,strategy3 FROM user WHERE id_telegram = %s")
     cursor.execute(query,(message.chat.id,))
     myresult = cursor.fetchall()
     for (strategy1,strategy2,strategy3) in myresult:
         markup = types.ReplyKeyboardMarkup()
         btn1 = types.KeyboardButton("Стратегия - KAMA ")
         btn2 = types.KeyboardButton("Стратегия - MOON ")
         btn3 = types.KeyboardButton("Стратегия - 1min ")
         back = types.KeyboardButton("Exit")
         markup.add(btn1, btn2, btn3,back)
         send_mess = f"<b> \nЗдесь вы можете выбрать на какие стратегии вам будут приходить сигналы! \nСтратегия - KAMA ({strategy1})\nСтратегия2 ({strategy2})\nСтратегия3 ({strategy3})</b>"
         bot.send_message(message.chat.id, send_mess,parse_mode='html' ,reply_markup=markup)
def strat(text,number,id):
         cnx.reconnect()
         cursor = cnx.cursor()
         query = ("SELECT "+str(number)+" FROM user WHERE id_telegram = %s")
         cursor.execute(query,(id,))
         myresult = cursor.fetchone()
         for strategy in myresult:
             if(strategy == 1):
                 sms = f"<b>{text} ---> ВЫКЛ</b>"
                 st = 0
             else:
                 st = 1
                 sms = f"<b>{text} ---> ВКЛ</b>"
             cnx.reconnect()
             mycursor = cnx.cursor()
             sql = "UPDATE user SET "+str(number)+" ="+str(st)+" WHERE id_telegram ="+str(id)
             mycursor.execute(sql)
             cnx.commit()
             mycursor.close()
             bot.send_message(message.chat.id, sms ,parse_mode='html')

@bot.message_handler(content_types=['text'])
def text(message):
     if (message.text=="Exit"):
         markup = types.ReplyKeyboardRemove(selective=False)
         send_mess = f"<b> Меню скрыто, чтобы открыть меню - /menu</b>"
         bot.send_message(message.chat.id, send_mess,parse_mode='html' ,reply_markup=markup)
     if (message.text=="Стратегия - KAMA"):
         strat(message.text,'strategy1',message.chat.id)
     if (message.text=="Стратегия - MOON"):
         strat(message.text,'strategy2',message.chat.id)
     if (message.text=="Стратегия - 1min"):
         strat(message.text,'strategy3',message.chat.id)

bot.polling(none_stop=True)
