from db import db_handler
from lib import common
from conf import settings

logger = common.get_logger('银行业务')


def check_balance_interface(username):
    user_data = db_handler.select(username)
    if user_data:
        logger.info(f'{username}查看了自己的余额')
        return True, '当前%s账户余额为：%s' % (username, user_data.get('balance'))
    return False, '查不到当前用户信息'


def withdraw_interface(username, money):
    user_data = db_handler.select(username)
    if not user_data:
        return False, '查不到当前登录用户'
    money = float(money)
    current_balance = user_data.get('balance')
    if current_balance >= money * (1 + settings.MONEY_RATE):
        current_balance -= money * (1 + settings.MONEY_RATE)
        msg = '%s提现成功,提现金额：%s,手续费扣除:%s,当前余额剩余:%s' % (user_data.get('username'), money, money * settings.MONEY_RATE, current_balance)
        user_data['flow'].append(msg)
        db_handler.save(user_data)
        logger.info(msg)
        return True, msg
    else:
        return False, '余额不足,您的当前余额为: %s' % current_balance


def recharge_interface(username, money):
    money = float(money)
    user_data = db_handler.select(username)
    if not user_data:
        return False, '查不到当前登录用户'
    user_data['balance'] += money
    msg = '%s充值成功,当前余额为%s' % (user_data['username'], user_data['balance'])
    user_data['flow'].append(msg)
    db_handler.save(user_data)
    logger.info(msg)
    return True, msg


def transfer_interface(username, to_username, money):
    money = float(money)
    user_data = db_handler.select(username)
    if not user_data:
        return False, '查不到当前登录用户'
    to_user_data = db_handler.select(to_username)
    if not to_user_data:
        return False, '转账用户不存在'
    if user_data['balance'] >= money:
        user_data['balance'] -= money
        to_user_data['balance'] += money
        msg = '%s向%s成功转账%s,您当前余额为%s' % (user_data['username'], to_user_data['username'], money, user_data['balance'])
        user_data['flow'].append(msg)
        db_handler.save(user_data)
        db_handler.save(to_user_data)
        logger.info(msg)
        return True, msg
    else:
        return False, '余额不足,转账失败,您的当前余额为: %s' % user_data['balance']


def check_flow_interface(username):
    user_data = db_handler.select(username)
    if not user_data:
        return False, '查不到当前登录用户'
    logger.info(f'{username}查看了自己的账单信息')
    return True, user_data.get('flow')
