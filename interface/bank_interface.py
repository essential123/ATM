from db import db_handler
from lib import common
logger = common.get_logger('银行业务')


def check_balance_interface(username):
    user_data = db_handler.select(username)
    return user_data['balance']


def withdraw_interface(username,money):
    user_data = db_handler.select(username)
    money = int(money)
    if user_data['balance']>= money:
        user_data['balance'] -= money * 1.11
        info= '%s提现成功,提现金额：%s,手续费扣除:%s,当前余额剩余:%s' % (user_data['username'],money,money*0.11,user_data['balance'])
        user_data['flow'].append(info)
        db_handler.save(user_data)
        logger.debug(info)
        return info
    else:
        return '余额不足,您的当前余额为: %s' % user_data['balance']


def recharge_interface(username,money):
    money = int(money)
    user_data = db_handler.select(username)
    user_data['balance'] += money
    info = '%s充值成功,当前余额为%s' % (user_data['username'],user_data['balance'])
    user_data['flow'].append(info)
    db_handler.save(user_data)
    logger.debug(info)
    return info


def transfer_interface(username,to_username,money):
    money = int(money)
    user_data = db_handler.select(username)
    to_user_data = db_handler.select(to_username)
    if user_data['balance'] >= money:
        user_data['balance'] -= money
        to_user_data['balance'] += money
        info = '%s向%s成功转账%s,您当前余额为%s' % (user_data['username'],to_user_data['username'],money,user_data['balance'])
        user_data['flow'].append(info)
        db_handler.save(user_data)
        db_handler.save(to_user_data)
        logger.debug(info)
        return info
    else:
        return '余额不足,转账失败,您的当前余额为: %s' % user_data['balance']

def check_flow_interface(username):
    user_data = db_handler.select(username)
    return user_data.get('flow')