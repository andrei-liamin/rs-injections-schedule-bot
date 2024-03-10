import os
import math
import telebot
import time
from datetime import datetime, date
from telebot import types
from ids import body_scheme_photo_ids

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.environ.get("BOT_TOKEN")
my_chat_id = 116733030
txt_done = "Готово"
txt_postpone = "Напомни через 2 часа"

bot = telebot.TeleBot(TOKEN)

# Задаем расписание отправки картинок
# Понедельник, среда и пятница с 11 утра до полуночи
schedule_days = [0, 2, 4]
start_hour = 11
end_hour = 24

# answer buttons
markup = types.ReplyKeyboardMarkup()
btn_done = types.KeyboardButton(txt_done)
btn_postpone = types.KeyboardButton(txt_postpone)
markup.add(btn_done, btn_postpone)

# Глобальная переменная для хранения состояния бота
is_paused = False

# Время паузы в секундах (2 часа)
pause_duration = 2 * 60 * 60

# Get photo id
@bot.message_handler(content_types=['photo'])
def get_photo_id(message):
    file_id = message.photo[-1].file_id
    bot.send_message(message.chat.id, file_id)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я телеграм-бот, который отправляет картинки каждые полчаса с понедельника по пятницу с 11 утра до полуночи. Нажмите кнопку 'Готово', чтобы остановить отправку на текущий день, или 'Пауза на 2 часа', чтобы сделать паузу в отправке.")

# cleanup buttons
markup_clear = types.ReplyKeyboardRemove()

# Обработчик кнопки "Готово"
@bot.message_handler(func=lambda message: message.text == "Готово")
def stop_sending(message):
    global is_paused
    is_paused = True
    bot.send_message(message.chat.id, "Отправка картинок остановлена на текущий день.", reply_markup=markup_clear)

# Обработчик кнопки "Пауза на 2 часа"
@bot.message_handler(func=lambda message: message.text == "Пауза на 2 часа")
def pause_sending(message):
    global is_paused
    is_paused = True
    bot.send_message(message.chat.id, "Отправка картинок приостановлена на следующие два часа.", reply_markup=markup_clear)
    time.sleep(pause_duration)
    is_paused = False
    bot.send_message(message.chat.id, "Пауза завершена. Продолжаем отправку картинок.", reply_markup=markup_clear)

# Функция для отправки картинок
def send_image():
    while True:
        if not is_paused:
            week_int = math.floor((datetime.now().date() - date(2024, 4, 2)).days / 7) % 8
            week = str(week_int + 1)
            week_day = datetime.now().strftime("%A")
            caption = week + " " + week_day
            body_scheme_photo_id = body_scheme_photo_ids[week_int][schedule_days.index(now.weekday)]
            now = datetime.now()
            if now.weekday() in schedule_days and start_hour <= now.hour < end_hour:
                # Отправляем картинку (замените на свой код)
                # bot.send_photo(chat_id, photo=open('image.jpg', 'rb'))
                bot.send_photo(my_chat_id, photo=body_scheme_photo_id, caption=caption, reply_markup=markup)
                pass
        time.sleep(1800)  # Пауза 30 минут

# Запускаем поток для отправки картинок
import threading
threading.Thread(target=send_image).start()

# Запускаем бота
bot.polling()
