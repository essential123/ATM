import hashlib
import logging.config
from conf import settings
import logging
import logging.config


def auth_user(func_name):
    def inner(*args, **kwargs):
        from core import src
        if src.user_status.get('is_login'):
            res = func_name(*args, **kwargs)
            return res
        else:
            print('用户未登录，请先登录')
            src.login()

    return inner


def get_md5(password):
    md5 = hashlib.md5()
    md5.update('密码'.encode('utf8'))
    md5.update(password.encode('utf8'))
    return md5.hexdigest()


def get_logger(title):
    logging.config.dictConfig(settings.LOGGING_DIC)
    logger1 = logging.getLogger(title)
    return logger1
