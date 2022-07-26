from db import db_handler
from conf import settings
import os
from lib import common

logger = common.get_logger('管理员业务')


def check_admin(username):
    user_data = db_handler.select(username)
    if user_data['is_admin']:
        logger.info(f'欢迎{username}管理员')
        return True, f'欢迎{username}管理员'
    return False, f'{username}你不是管理员'


def lock_user(all_user):
    username = input('请输入需要锁定的用户>>:').strip()
    if username not in all_user:
        return False, '当前输入用户不存在'
    user_data = db_handler.select(username)
    user_data['is_lock'] = True
    db_handler.save(user_data)
    logger.info(f"{username}用户已被管理员锁定")
    return True, f"{username}用户已被管理员锁定"


def reset_pwd(all_user):
    username = input('请输入需要重置密码的用户>>:').strip()
    if username not in all_user:
        return False, '输入的用户不存在'
    user_data = db_handler.select(username)
    password = input('请输入密码>>:').strip()
    confirm_password = input('请再次输入密码>>:').strip()
    # 判断两次密码是否一致
    if not password == confirm_password:
        return False, '两次密码不一致'
    user_data['password'] = common.get_md5(password)
    db_handler.save(user_data)
    logger.info(f"管理员成功重置用户{username}密码")
    return True, f"管理员成功重置用户{username}密码"


def clear_user(all_user):
    username = input('请输入您要清理的用户>>:').strip()
    if username not in all_user:
        return False, '当前输入用户不存在'
    user_db = settings.USER_DB_PATH
    user_path = os.path.join(user_db, username)
    os.remove(user_path)
    logger.info(f"管理员成功删除了{username}用户")
    return True, f"管理员成功删除了{username}用户"
