import os
import json
from conf import settings


def save(user_data):
    username = user_data.get('username')
    file_path = os.path.join(settings.USER_DB_PATH, username)
    with open(file_path, 'w', encoding='utf8') as f:
        json.dump(user_data, f, ensure_ascii=False)


def select(username):
    file_list = os.listdir(settings.USER_DB_PATH)
    file_path = os.path.join(settings.USER_DB_PATH, username)
    if username in file_list:
        with open(file_path,'r',encoding='utf8') as f:
            return json.load(f)
