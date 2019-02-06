from InstagramAPI import InstagramAPI
import os
user=input('Introduce the user: ')
password=input('Introduce the password: ')
API_Handler=InstagramAPI(user,password)
API_Handler.login() 


def upload_image(path,caption):
    API_Handler.uploadPhoto(path, caption=caption)