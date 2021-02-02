import os
import math
import telebot
from tzlocal import get_localzone
from datetime import datetime, date
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.environ.get("BOT_TOKEN")
my_chat_id = 116733030
txt_done = "Готово"
txt_postpone = "Напомни позже"

bot = telebot.TeleBot(TOKEN)
body_scheme_photo_id = 'AgACAgIAAxkBAAOXX95mA4r7tTKG0l6SKkl0JfQTTs0AAnqtMRuanlFKpCPw2klIdqFLfteWLgADAQADAgADeQADkq0AAh4E'

week = str(math.ceil((datetime.now().date() - date(2021, 1, 10)).days % 28 / 7))
week_day = datetime.now().strftime("%A")
caption = week + " " + week_day

# background scheduler
daily_sched = BackgroundScheduler()
hourly_sched = BackgroundScheduler()

# buttons
markup = types.ReplyKeyboardMarkup()
btn_done = types.KeyboardButton(txt_done)
btn_postpone = types.KeyboardButton(txt_postpone)
markup.add(btn_done, btn_postpone)

@daily_sched.scheduled_job('cron', day_of_week='mon-sun', hour=7, minute=30, second=0)
# @daily_sched.scheduled_job('cron', start_date="2021-02-02T00:31:00", minute="*/2", second=0)
def daily_job():
	@hourly_sched.scheduled_job('interval', minutes=30)
	# @hourly_sched.scheduled_job('interval', seconds=5)
	def hourly_job():
		bot.send_photo(my_chat_id, photo=body_scheme_photo_id, caption=caption, reply_markup=markup)
	hourly_sched.start()
daily_sched.start()

# test

# print(type((date(2021, 1, 7) - date(2021, 1, 4)).days))
# print(math.ceil((datetime.now().date() - date(2021, 1, 10)).days % 28 / 7))
# print(caption)
# print(datetime.now().strftime("%A"))

# message handlers

@bot.message_handler(commands=['time'])
def message_props(message: types.Message):
	bot.reply_to(message, datetime.now())

markup_clear = types.ReplyKeyboardRemove()

@bot.message_handler(func=lambda message: message.text == txt_done)
def success(message: types.Message):
	hourly_sched.shutdown()
	bot.send_message(my_chat_id, "Красавчик!", reply_markup=markup_clear)

@bot.message_handler(func=lambda message: message.text == txt_postpone)
def postpone(message: types.Message):
  bot.send_message(my_chat_id, "ок, подождём...", reply_markup=markup_clear)

bot.polling()