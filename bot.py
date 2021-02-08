import os
import math
import telebot
from datetime import datetime, date
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
from ids import body_scheme_photo_ids

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.environ.get("BOT_TOKEN")
my_chat_id = 116733030
txt_done = "Готово"
txt_postpone = "Напомни позже"

bot = telebot.TeleBot(TOKEN)

# background scheduler
daily_sched = BackgroundScheduler()
hourly_sched = BackgroundScheduler()

# buttons
markup = types.ReplyKeyboardMarkup()
btn_done = types.KeyboardButton(txt_done)
btn_postpone = types.KeyboardButton(txt_postpone)
markup.add(btn_done, btn_postpone)

@daily_sched.scheduled_job('cron', day_of_week='mon-sun', hour=8, minute=0, second=0)
def daily_job():
	week_int = math.floor((datetime.now().date() - date(2021, 1, 11)).days / 7) % 4
	week_day_int = datetime.now().weekday()

	week = str(week_int + 1)
	week_day = datetime.now().strftime("%A")
	caption = week + " " + week_day

	body_scheme_photo_id = body_scheme_photo_ids[week_int][week_day_int]

	@hourly_sched.scheduled_job('interval', minutes=30, next_run_time=datetime.now())
	def hourly_job():
		bot.send_photo(my_chat_id, photo=body_scheme_photo_id, caption=caption, reply_markup=markup)
	hourly_sched.start()
daily_sched.start()

@daily_sched.scheduled_job('cron', day_of_week='mon-sun', hour=23, minute=59, second=0)
def daily_job():
	hourly_sched.shutdown()

# message handlers

@bot.message_handler(commands=['current_time'])
def message_props(message: types.Message):
	bot.reply_to(message, datetime.now())

@bot.message_handler(commands=['resume'])
def message_props(message: types.Message):
	if hourly_sched.state == 2:
		hourly_sched.resume()

markup_clear = types.ReplyKeyboardRemove()

@bot.message_handler(func=lambda message: message.text == txt_done)
def success(message: types.Message):
	if hourly_sched.state == 1:
		hourly_sched.pause()
		bot.send_message(my_chat_id, "Красавчик!", reply_markup=markup_clear)

@bot.message_handler(func=lambda message: message.text == txt_postpone)
def postpone(message: types.Message):
	if hourly_sched.state == 1:
		bot.send_message(my_chat_id, "ок, подождём...", reply_markup=markup_clear)

@bot.message_handler(func=lambda message: message.text == "state")
def postpone(message: types.Message):
  bot.send_message(my_chat_id, hourly_sched.state, reply_markup=markup_clear)

# @bot.message_handler(content_types=['photo'])
# def image_id(message: types.Message):
#   bot.send_message(my_chat_id, message.photo[0].file_id)

bot.polling()