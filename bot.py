import telebot
from telebot.types import Message

TOKEN = '1438159737:AAFrC7GeLkJi_wpKVkl9DB46fgVVmO9elQo'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
	bot.reply_to(message, message)

@bot.message_handler(func=lambda message: True)
def upper(message: Message):
  bot.reply_to(message, message.text.upper())

bot.polling()