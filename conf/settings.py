import logging.config
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'db')
USER_DB_PATH = os.path.join(DB_PATH, 'user_db')
LOG_PATH = os.path.join(BASE_DIR, 'log')
if not os.path.exists(USER_DB_PATH):
    os.mkdir(USER_DB_PATH)

MONEY_RATE = 0.01

# 定义日志输出格式 开始
STANDARD_FORMAT = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'  # 其中name为getlogger指定的名字
SIMPLE_FORMAT = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

# 自定义文件路径
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
LOGFILE_PATH = os.path.join(LOG_PATH, 'log')
# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': STANDARD_FORMAT
        },
        'simple': {
            'format': SIMPLE_FORMAT
        },
    },
    'filters': {},  # 过滤日志
    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        # 打印到文件的日志,收集info及以上的日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': LOGFILE_PATH,  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },  # 当键不存在的情况下 (key设为空字符串)默认都会使用该k:v配置
        # '购物车记录': {
        #     'handlers': ['default','console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
        #     'level': 'WARNING',
        #     'propagate': True,  # 向上（更高level的logger）传递
        # },  # 当键不存在的情况下 (key设为空字符串)默认都会使用该k:v配置
    },
}
