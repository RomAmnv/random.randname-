import telebot
from telebot import types
import config
import mysql.connector

bot = telebot.TeleBot(config.TOKEN)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=config.PASSWORD,
    port="3306",
    database="mydatabase"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
#mycursor.execute("CREATE TABLE users (first_name VARCHAR(255), last_name VARCHAR(255), role VARCHAR(255))")
#mycursor.execute("ALTER TABLE users ADD COLUMN (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT UNIQUE)")


user_dict = {}


class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ""
        self.role = None


@bot.message_handler(commands=['start'])
def main(message):
    msg = bot.send_message(message.chat.id, "First name")
    bot.register_next_step_handler(msg, process_firstname_step)


def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_dict[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, "Last name")
        bot.register_next_step_handler(msg, process_lastname_step)


    except Exception as e:
        bot.reply_to(message, "error: " + str(e))


def process_lastname_step(message):
    try:
        user_id = message.from_user.id
        user = user_dict[user_id]
        user.last_name = message.text

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Student', 'Teacher')
        msg = bot.send_message(message.chat.id, "Select your role", reply_markup=markup)
        bot.register_next_step_handler(msg, process_role_step)


    except Exception as e:
        bot.reply_to(message, "error: " + str(e))


def process_role_step(message):
    try:
        user_id = message.from_user.id
        role = message.text
        user = user_dict[user_id]
        if (role == u'Student') or (role == u'Teacher'):
            user.role = role
        else:
            raise Exception("Unknown role")
        bot.send_message(user_id,
                         'Nice to meet you ' + user.first_name + " " + user.last_name + '\n Role: ' + user.role)
        sql = "INSERT INTO users (first_name, last_name, role, user_id) VALUES (%s, %s, %s, %s)"
        val = (user.first_name, user.last_name, user.role, user_id)
        mycursor.execute(sql, val)
        mydb.commit()
    except Exception as e:
        #bot.reply_to(message, "error: " + str(e))
        bot.reply_to(message, "Error, you are already registered in the system")


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
