
import telebot 
from telebot import apihelper
import time
import requests
import pandas as pd
import re
import matplotlib.pyplot as plt
import collections
import logging

from currency import main, find_str, history_task

API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

apihelper.proxy = {'https':'socks5h://<your socks5 proxy>'}

telebot.logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(regexp=(r'/list|/lst'))
def list(message):
    my_dict = main()
    new_dict={}
    for k, v in my_dict.items():
        new_dict[k]=round(v,2)
    df = pd.DataFrame(new_dict, index=[''])
    df1=df.T
    df1=df1.to_string(index=True)
    print(new_dict)
    bot.reply_to(message, df1)

@bot.message_handler(commands=['photo'])
def send_photo_test(message):
    photo = open('./my_history.png', 'rb')
    bot.send_photo(message.chat.id, photo)
    
    
@bot.message_handler(regexp=(r'/exchange *\s'))
def regex(message):
    
    # my_dict = {'USD': 1.45, 'EUR': 1.33, 'CAD':1.23}
    text = find_str(message.text)
    print(text)
  
    bot.send_message(message.from_user.id, text)

@bot.message_handler(regexp=(r'/history *\s'))
def make_chart(message):
    history_t = history_task(message.text)
    print(history_t)
    mess = 'No exchange rate data is available for the selected currency.'
    # try:
    if history_t != mess:
        photo = open(history_t, 'rb')
        bot.send_photo(message.from_user.id, photo)
    else:
        bot.send_message(message.from_user.id, mess)
   


if __name__=='__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=2, timeout=20)
        except Exception as ex:
            logging.error(ex)
    
