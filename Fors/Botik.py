from email import message 
import types 
import typing 
import telebot 
 
bot = telebot.TeleBot("7176581010:AAGKWDgsAGAWxtceI749Hql_w9Elugzdxd4") 
name = ' ' 
surname = ' ' 
a = ' ' 
 
 
    
@bot.message_handler(commands=['start', 'help']) 
def send_welcome(message): 
 bot.reply_to(message, "ntbgrvfec") 
  
  
@bot.message_handler(commands=['verf']) 
def send_welcome(message): 
 bot.reply_to(message, "brgvfec") 
 
 
 
@bot.message_handler(commands=['как_дела']) 
def send_welcome(message): 
 bot.reply_to(message, ",muyjnthbrgv") 
 
 
 
@bot.message_handler(commands=['сам_иди']) 
def send_welcome(message): 
 bot.reply_to(message, ",myntb") 
    
    
 
 
 
 
 
bot.infinity_polling()
