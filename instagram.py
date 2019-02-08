from InstagramAPI import InstagramAPI
from telegramFunctions import read_database
from base64 import b64decode



def upload_image(path,caption,chat_id,username):
    data=read_database(chat_id,username)
    password=b64decode(data[3][1:]).decode('utf-8')
    #password=telegramFunctions.decrypt_password(data[3][2:]).decode('utf-8')
    API_Handler=InstagramAPI(data[2],password)
    API_Handler.login() 
    API_Handler.uploadPhoto(path, caption=caption)
