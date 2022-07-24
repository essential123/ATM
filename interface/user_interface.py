import json
from db import db_handler
from core import src
from lib import common
logger = common.get_logger('用户业务')


def register_interface(username, password):
    # 校验用户名是否已存在
    res = db_handler.select(username)
    if res:
        return '用户名已存在'
    password = common.get_md5(password)
    # 构造用户数据字典
    user_data = {
        'username': username,
        'password': password,
        'shopping_cards': {},
        'balance': 15000,
        'flow': [],
        'is_lock': False,
        'is_admin': False,
    }
    db_handler.save(user_data)
    logger.debug(f'{username}注册已成功')
    return f'{username}注册已成功'


def login_interface(username):
    # 校验用户名是否已存在
    user_data = db_handler.select(username)
    if not user_data:
        return '用户名不存在'
    if user_data.get('is_lock'):
        return '用户已经锁定,请联系管理员'
    count = 1
    while True:
        password = input('请输入密码>>:').strip()
        password = common.get_md5(password)
        if not password == user_data.get('password'):
            if count < 3:
                print('密码输入错误,剩余输入机会%s次' % (3 - count))
                count +=1
                continue
            elif count == 3:
                user_data['is_lock'] = True
                db_handler.save(user_data)
                return '密码输入错误超过三次，账户被锁定请联系管理员'
        else:
            src.user_status['is_login'] = True
            src.user_status['username'] = username
            logger.debug('%s登录成功' % username)
            return '%s登录成功' % username






