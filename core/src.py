import os
import json
from conf import settings
from interface import user_interface, bank_interface, shop_interface
from lib import common

user_status = {
    'username': '',
    'is_login': False,
}

base_path = settings.BASE_DIR
db_path = settings.DB_PATH


def register():
    while True:
        # 获取用户名数据
        username = input('请输入用户名(输入q退出)>>:').strip()
        if username == 'q':
            break
        if username:
            # 用户数据文件路径
            password = input('请输入密码>>:').strip()
            confirm_password = input('请再次输入密码>>:').strip()
            # 判断两次密码是否一致
            if not password == confirm_password:
                print('两次密码不一致')
                return
            res = user_interface.register_interface(username, password)
            print(res)
            break


def login():
    while True:
        username = input('请输入用户名(输入q退出)>>:').strip()
        if username == 'q':
            break
        if username:
            if username == user_status['username']:
                if user_status['is_login']:
                    print('%s用户已登录' % username)
                    continue
            res = user_interface.login_interface(username)
            print(res)
            break
        else:
            print('输入不能为空')


from lib import common


@common.auth_user
def check_balance():
    balance = bank_interface.check_balance_interface(user_status['username'])
    print('%s,您的余额为：%s' % (user_status['username'], balance))


@common.auth_user
def withdraw():
    money = input('请输入提现金额>>:').strip()
    res = bank_interface.withdraw_interface(user_status['username'], money)
    print(res)


@common.auth_user
def recharge():
    money = input('请输入充值的金额>>:').strip()
    res = bank_interface.recharge_interface(user_status['username'], money)
    print(res)


@common.auth_user
def transfer():
    to_username = input('请输入收款人姓名>>:').strip()
    money = input('请输入转账的金额>>:').strip()
    res = bank_interface.transfer_interface(user_status['username'], to_username, money)
    print(res)


@common.auth_user
def check_bill():
    res = bank_interface.check_flow_interface(user_status.get('username'))
    print('-' * 40)
    for i in res:
        print(i)
    print('-' * 40)


goods_list = [
    ['挂壁面', 3],
    ['印度飞饼', 10],
    ['土耳其土豆', 22],
    ['伊拉克拌面', 50],
    ['董卓戏张飞公仔', 100],
    ['极品木瓜', 200],
    ['蓝牙耳机', 666],
    ['手机', 5000],
    ['电脑', 10000],
]


@common.auth_user
def add_shopping_cards():
    shop_car = {}
    while True:
        for i, j in enumerate(goods_list):
            print(f"商品编号:{i} , 商品名称：{j[0]} , 商品价格：{j[1]}")
        goods_choice = input('请输入你想要的商品编号(输入q退出)>>:').strip()
        if goods_choice == 'q':
            break
        elif int(goods_choice) in range(len(goods_list)):
            goods = goods_list[int(goods_choice)][0]
            goods_count = input('请输入你想要的商品数量>>:').strip()
            goods_price = goods_list[int(goods_choice)][1]
            shop_car[goods] = [goods_count, goods_price]
            file_path = os.path.join(settings.USER_DB_PATH, user_status['username'])
            shop_interface.add_shopping_cards_interface(shop_car, file_path)
        else:
            print('请输入正确的编号')


@common.auth_user
def check_shop_car():
    shop_card_info = shop_interface.check_shop_car_interface(user_status['username'])
    if not shop_card_info:
        return
    for item in shop_card_info.items():
        print(f"商品名称:{item[0]}  |  商品数量:{item[1][0]}  |  商品单价:{item[1][1]}")


@common.auth_user
def Edit_Shopping_Cart():
    username = user_status.get('username')
    shop_interface.Edit_Shopping_Cart_interface(username)


@common.auth_user
def settlement_shopping_cards():
    shop_interface.settlement_shopping_cards_interface(user_status['username'])


@common.auth_user
def admin():
    from interface import admin_interface
    flag = admin_interface.check_admin(user_status.get('username'))
    if not flag:
        print('你不是管理员')
        return
    print('管理员%s登录成功' % user_status['username'])
    while True:
        function_dict = {
            '1': ['锁定用户账户', admin_interface.lock_user],
            '2': ['重置用户密码', admin_interface.reset_pwd],
            '3': ['清理用户数据', admin_interface.clear_user],
        }
        for k, v in function_dict.items():
            print(k, v[0])
        choice = input('请输入功能编号(输入q退出)>>:').strip()
        if choice == 'q':
            break
        elif choice in function_dict:
            function_dict[choice][1]()
        else:
            print('编号超出范围，请重新输入')


command_dict = {
    '1': ['用户注册', register],
    '2': ['用户登录', login],
    '3': ['查看余额', check_balance],
    '4': ['账户提现', withdraw],
    '5': ['充值功能', recharge],
    '6': ['转账功能', transfer],
    '7': ['查看账单', check_bill],
    '8': ['添加购物车', add_shopping_cards],
    '9': ['查看购物车', check_shop_car],
    '10': ['修改购物车', Edit_Shopping_Cart],
    '11': ['结算购物车', settlement_shopping_cards],
    '12': ['管理员功能', admin],
}


def run():
    while True:
        for k, v in command_dict.items():
            print(k, v[0])
        choice = input('请输入功能编号>>:').strip()
        if choice == 'q':
            break
        elif choice in command_dict:
            command_dict[choice][1]()
        else:
            print('编号超出范围，请重新输入')
