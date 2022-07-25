from db import db_handler
from lib import common

logger = common.get_logger('用户业务')


def register_interface(username, password):
    # 校验用户名是否已存在
    res = db_handler.select(username)
    if res:
        return False, '用户名已存在'
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
    logger.info(f'{username}注册已成功')
    return True, f'{username}注册已成功'


def login_interface(username):
    # 校验用户名是否已存在
    user_data = db_handler.select(username)
    if not user_data:
        return False, '用户名不存在'
    if user_data.get('is_lock'):
        return False, '用户已经锁定,请联系管理员'
    count = 1
    while True:
        password = input('请输入密码>>:').strip()
        password = common.get_md5(password)
        if password != user_data.get('password'):
            if count < 3:
                print('密码输入错误,剩余输入机会%s次' % (3 - count))
                count += 1
                continue
            elif count == 3:
                user_data['is_lock'] = True
                db_handler.save(user_data)
                return False, '密码输入错误超过三次账户被锁定,请联系管理员'
        logger.info('%s登录成功' % username)
        return True, '%s登录成功' % username
