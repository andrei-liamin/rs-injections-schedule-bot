import telebot
from tzlocal import get_localzone
from datetime import datetime
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = '1438159737:AAFrC7GeLkJi_wpKVkl9DB46fgVVmO9elQo'
my_chat_id = 116733030
txt_done = "Готово"
txt_postpone = "Напомни позже"

bot = telebot.TeleBot(TOKEN)
body_scheme_photo_id = 'AgACAgIAAxkBAAOXX95mA4r7tTKG0l6SKkl0JfQTTs0AAnqtMRuanlFKpCPw2klIdqFLfteWLgADAQADAgADeQADkq0AAh4E'

# background scheduler
daily_sched = BackgroundScheduler()
hourly_sched = BackgroundScheduler()

@daily_sched.scheduled_job('cron', day_of_week='mon-sun', hour=20, minute=0, second=0)
def daily_job():
	markup = types.ReplyKeyboardMarkup()
	btn_done = types.KeyboardButton(txt_done)
	btn_postpone = types.KeyboardButton(txt_postpone)
	markup.add(btn_done, btn_postpone)

	@hourly_sched.scheduled_job('interval', minutes=1)
	def hourly_job():
		bot.send_photo(my_chat_id, photo=body_scheme_photo_id, caption="Пора ширнуться!", reply_markup=markup)
	hourly_sched.start()

daily_sched.start()

# message handlers

@bot.message_handler(commands=['start', 'help'])
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