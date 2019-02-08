from urllib import request
import keyManager
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import mysql.connector
from  base64 import b64encode
from config import PASSWORD,HOST,DATABASE,USER
def download_from_telegram(message, bot, TOKEN, path):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_name = file_info.file_path[7:]
    request.urlretrieve(
        'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path), path+file_name)
    return file_name


def encrypt_password(password):

    public_key = keyManager.open_public_Key()
    encrypted = public_key.encrypt(
        password,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted


def decrypt_password(encrypt_password):
    private_key = keyManager.open_private_key()
    original_message = private_key.decrypt(
        encrypt_password,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message

def read_database(chat_id,username):
    exist=False
    cnx = mysql.connector.connect(
        user=USER, password=PASSWORD, host=HOST, database=DATABASE,auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM user WHERE telegram_user='{0}' and chat_id={1}".format(username,chat_id))
    for row in cursor:
        exist=True
        answer=row
    if exist:
        cursor.close() 
        cnx.close()
    else:
        answer=None
        pass
    
    return answer


def insert_data(chat_id,telegram_user,username,identifier):
    cnx = mysql.connector.connect(user='bot', password='P8Bz43XxF1Ea7au94fY4r1uVi2WjWbGHz17n9NL8tvBP82t81ERwM2a5nPNnVCj8', host='127.0.0.1', database='ig_users')
    cursor = cnx.cursor()
    identifier=base64.b64encode(identifier.encode('utf-8'))
    #identifier=encrypt_password(identifier.encode('utf-8'))
    try:
        cursor.execute("INSERT INTO  user (chat_id,telegram_user,username,identifier) VALUES(%s,%s,%s,%s)",(chat_id,telegram_user,username,str(identifier)))
        id = cursor.lastrowid

    except Exception:
        id=-1
    cnx.commit()
    cursor.close()
    cnx.close()
    return id
if __name__ == "__main__":
    insert_data(101231,'prueba','username','identifier')