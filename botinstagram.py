import instagram
import telebot
import requests
from PIL import Image
import urllib
#TOKEN=
#URL = 'http://api.telegram.org/bot{0}/getUpdates'.format(TOKEN)
#bot = telebot.TeleBot(token=TOKEN)
chat_id = 0
#path=
caption_input=False
waiting=True
caption=""

helpString="This bot allows the user to upload photos on instagram only by sending the photo. If you want to upload the photo, send it to the bot"
@bot.message_handler(content_types=['photo'])
def upload_image(message):
    global caption_input
    global waiting
    global caption
    caption_input=True
    chat_id = message.chat.id
    print(chat_id)
    file_id = message.photo[-1].file_id
    print('The file id is'+file_id)
    file_info = bot.get_file(file_id)
    file_name=file_info.file_path[7:]
    urllib.request.urlretrieve('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path),path+file_name)
    bot.send_message(chat_id,"Photo received")
    bot.send_message(chat_id,'Add the caption')
    while(waiting):
        pass
    
    instagram.upload_image(path+file_name,caption)
    waiting=True
    bot.send_message(chat_id,"Photo uploaded")

@bot.message_handler(commands=['help'])
def help(message):
    chat_id=message.chat.id
    bot.send_message(chat_id,helpString)
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    print(chat_id)
    bot.send_message(chat_id, "Hello "+message.chat.last_name+" this is the demo version")

@bot.message_handler(func=lambda message: True)
def caption_handler(message):
    global caption_input
    global waiting
    global caption
    if caption_input:
        caption=message.text
        caption_input=False
        waiting=False
    else:
        pass




# Upon calling this function, TeleBot starts polling the Telegram servers for new messages.
# - none_stop: True/False (default False) - Don't stop polling when receiving an error from the Telegram servers
# - interval: True/False (default False) - The interval between polling requests
#           Note: Editing this parameter harms the bot's response time
# - timeout: integer (default 20) - Timeout in seconds for long polling.
if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0,timeout=20)

