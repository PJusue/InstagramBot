import instagram
import telebot
from PIL import Image
from config import TOKEN,URL,PATH
from telegramFunctions import download_from_telegram,insert_data,read_database
TOKEN = TOKEN
URL = URL
bot = telebot.TeleBot(token=TOKEN)
chat_id = 0
path = PATH
caption_input = False
waiting = True
caption = ""
helpString = "This bot allows the user to upload photos on instagram only by sending the photo. If you want to upload the photo, send it to the bot"
# When the bot receives a photo from the user this function is called and
# it will download the photo from the Telegram API,


@bot.message_handler(content_types=['photo'])
def upload_image(message):
    global caption_input, waiting, caption
    caption_input = True
    chat_id = message.chat.id
    file_name = download_from_telegram(
        message, bot, TOKEN, path)
    bot.send_message(chat_id, "Photo received")
    bot.send_message(chat_id, 'Add the caption')
    while(waiting):
        pass
    instagram.upload_image(path+file_name, caption,message.chat.id,message.chat.username)
    waiting = True
    bot.send_message(chat_id, "Photo uploaded")



@bot.message_handler(commands=['prueba'])
def prueba(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, message.text)


@bot.message_handler(commands=['login'])
def login(message):
    index = message.text.find('@')
    index1 = message.text.find(' ')
    ok = insert_data(
        message.chat.id, message.chat.username, message.text[index1+1:index], message.text[index+1:])
    if ok == 0:
        bot.send_message(message.chat.id, "The login was succesful")
    else:
        pass


@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, helpString)


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Hello "+message.chat.username +
                     " this is the demo version")
    exist = read_database(
        message.chat.id, message.chat.username)
    if exist == None:
        bot.send_message(
            chat_id, "Use the /login username@password command to create your account")
    else:
        bot.send_message(chat_id, "You are logged in")


@bot.message_handler(func=lambda message: True)
def caption_handler(message):
    global caption_input
    global waiting
    global caption
    if caption_input:
        caption = message.text
        caption_input = False
        waiting = False
    else:
        pass


# Upon calling this function, TeleBot starts polling the Telegram servers for new messages.
# - none_stop: True/False (default False) - Don't stop polling when receiving an error from the Telegram servers
# - interval: True/False (default False) - The interval between polling requests
#           Note: Editing this parameter harms the bot's response time
# - timeout: integer (default 20) - Timeout in seconds for long polling.
if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0, timeout=20)
