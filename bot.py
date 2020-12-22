import telebot
from tzlocal import get_localzone
from datetime import datetime
from telebot.types import Message
from apscheduler.schedulers.background import BackgroundScheduler


TOKEN = '1438159737:AAFrC7GeLkJi_wpKVkl9DB46fgVVmO9elQo'
bot = telebot.TeleBot(TOKEN)
body_scheme_photo_id = 'AgACAgIAAxkBAAOXX95mA4r7tTKG0l6SKkl0JfQTTs0AAnqtMRuanlFKpCPw2klIdqFLfteWLgADAQADAgADeQADkq0AAh4E'

# background scheduler
sched = BackgroundScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour=1, minute=5, second=0, timezone=get_localzone())
def timed_job():
  bot.send_photo(116733030, photo=body_scheme_photo_id, caption="Пора ширнуться!")

sched.start()

# message handlers

@bot.message_handler(commands=['start', 'help'])
def message_props(message: Message):
	bot.reply_to(message, datetime.now())

@bot.message_handler(commands=['stz'])
def message_props(message: Message):
	bot.reply_to(message, datetime.now())

@bot.message_handler(commands=['ltz'])
def message_props(message: Message):
	bot.reply_to(message, get_localzone())

@bot.message_handler(content_types=['photo'])
def photo_props(message: Message):
	bot.reply_to(message, message)

@bot.message_handler(func=lambda message: True)
def upper(message: Message):
  bot.reply_to(message, message.text.upper())

bot.polling()