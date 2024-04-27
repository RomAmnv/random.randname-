import telebot
#from app.Function import recognizeAudio
from telebot import types
#from pydub import AudioSegment
import config
import mysql.connector
import os
import wave
import requests
import subprocess
#from __init__ import cursor
#from pydub import AudioSegment

#AudioSegment.preferred_ffmpeg = "avprobe"
bot = telebot.TeleBot(config.TOKEN)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=config.PASSWORD,
    port="3306",
    database="mydatabase"
)

mycursor = mydb.cursor()
user_dict = {}
# mycursor.execute("CREATE TABLE users (first_name VARCHAR(255), last_name VARCHAR(255), role VARCHAR(255))")
# mycursor.execute("ALTER TABLE users ADD COLUMN (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT UNIQUE)")
# mycursor.execute("ALTER TABLE users ADD COLUMN (second_name VARCHAR(255))")

class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.second_name = ""
        self.last_name = ""
        self.email = ""
        self.role = None



@bot.message_handler(commands=['start'])
def main(message):
    msg = bot.send_message(message.chat.id, "First name")
    bot.register_next_step_handler(msg, process_firstname_step)


def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_dict[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, "Second name")
        bot.register_next_step_handler(msg, process_secondname_step)


    except Exception as e:
        print("firstname step",e)
        bot.reply_to(message, "error: " + str(e))


def process_secondname_step(message):
    try:
        user_id = message.from_user.id
        user = user_dict[user_id]
        user.second_name = message.text

        msg = bot.send_message(message.chat.id, "Last name")
        bot.register_next_step_handler(msg, process_lastname_step)


    except Exception as e:
        print("secondname step",e)
        bot.reply_to(message, "error: " + str(e))

def process_lastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_dict[user_id]
        user.last_name = message.text

        msg = bot.send_message(message.chat.id, "Your email")
        bot.register_next_step_handler(msg, process_email_step)


    except Exception as e:
        print("lastname step",e)
        bot.reply_to(message, "error: " + str(e))


def process_email_step(message):
    try:
        user_id = message.from_user.id
        user = user_dict[user_id]
        user.email = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Student', 'Teacher')
        msg = bot.send_message(message.chat.id, "Select your role", reply_markup=markup)
        bot.register_next_step_handler(msg, process_role_step)

    except Exception as e:
        print("email step",e)
        bot.reply_to(message, "error: " + str(e))

def process_role_step(message):
    try:
        user_id = message.from_user.id
        role = message.text
        print(role)
        user = user_dict[user_id]
        if (role == u'Student') or (role == u'Teacher'):
            user.role = role
        else:
            raise Exception("Unknown role")
        bot.send_message(user_id,
                         'Nice to meet you, ' + user.second_name + " " + user.first_name + " " + user.last_name + "\nEmail: " + user.email + '\nRole: ' + user.role)
        if (role == u'Student'): id_st = "id_student"
        else:pass
        if (role == u'Teacher'): id_st = "id_teacher"
        else:pass
        sql = f"INSERT INTO {user.role} (first_name, second_name, last_name, email, {id_st}) VALUES (%s,%s,%s,%s,%s)"
        val = (user.first_name, user.second_name, user.last_name, user.email, user_id)
        mycursor.execute(sql,val)
        mydb.commit()
    except Exception as e:
        print("Role step",e)
        bot.reply_to(message, "Error, you are already registered in the system")


class Webinar:
    def __init__(self, name, date):
        self.name = name
        self.date = date


@bot.message_handler(commands=['add_webinar'])
def add_webinar_info(message):
    try:
        user_id = message.from_user.id
        sql = "SELECT id_teacher FROM teacher WHERE id_teacher = %s"
        val = (user_id,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()

        if result:
            msg = bot.send_message(message.chat.id, "Enter the webinar name")
            bot.register_next_step_handler(msg, process_webinar_name_step)
        else:
            bot.reply_to(message, "You are not authorized to use this command")
    except Exception as e:
        print("add_webinar command", e)
        bot.reply_to(message, "Error: " + str(e))


def process_webinar_name_step(message):
    try:
        user_id = message.from_user.id
        webinar_name = message.text
        if webinar_name.lower() == "/stop":
            # Остановить ввод вебинаров
            bot.reply_to(message, "Input of webinars stopped")
        else:
            # Проверяем наличие атрибута 'webinars' в объекте пользователя
            if user_id in user_dict:
                user_dict[user_id].webinars = []
                user_dict[user_id].webinars.append(Webinar(webinar_name, ""))

                msg = bot.send_message(message.chat.id, "Enter the webinar date (YYYY-MM-DD)")
                bot.register_next_step_handler(msg, process_webinar_date_step)
            else:
                bot.reply_to(message, "User not found")
    except Exception as e:
        print("webinar name step", e)
        bot.reply_to(message, "Error: " + str(e))


def process_webinar_date_step(message):
    try:
        user_id = message.from_user.id
        webinar_date = message.text
        user_dict[user_id].webinars[-1].date = webinar_date

        sql = "INSERT INTO vebinar (name_vebinar, date_vebinar) VALUES (%s, %s)"
        val = (user_dict[user_id].webinars[-1].name, user_dict[user_id].webinars[-1].date)
        mycursor.execute(sql, val)
        mydb.commit()

        bot.send_message(message.chat.id, "Webinar information added successfully")

        # Добавить возможность добавления следующего вебинара
        msg = bot.send_message(message.chat.id, "Enter the next webinar name")
        bot.register_next_step_handler(msg, process_webinar_name_step)
    except Exception as e:
        print("webinar date step", e)
        bot.reply_to(message, "Error: " + str(e))


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)