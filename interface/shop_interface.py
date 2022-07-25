from db import db_handler
import json
from lib import common

logger = common.get_logger('购物车业务')


def add_shopping_cards_interface(shop_car, file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        user_data = json.load(f)
        old_shop_car = user_data.get('shopping_cards')
    for goods in shop_car:
        if goods in old_shop_car:
            old_shop_car.get(goods)[0] += shop_car.get(goods)[0]
        else:
            old_shop_car[goods] = shop_car.get(goods)
    db_handler.save(user_data)
    logger.debug(f"{user_data['username']}成功添加购物车")
    return '%s添加购物车成功' % user_data['username']


def check_shop_car_interface(username):
    user_data = db_handler.select(username)
    shop_card_info = user_data.get('shopping_cards')
    if not shop_card_info:
        print('购物车未添加任何物品')
    else:
        return shop_card_info


def Edit_Shopping_Cart_interface(username):
    user_dict = db_handler.select(username)  # 大字典
    shop_card_info = user_dict.get('shopping_cards')  # 大字典的购物车
    if not shop_card_info:
        print('购物车未添加任何物品')
    while True:
        goods_info = {}
        for i, j in enumerate(shop_card_info):
            goods_info[i] = j
            print(
                f"商品编号:{i} , 商品名称：{j} , 商品数量：{shop_card_info[j][0]},商品单价：{shop_card_info[j][1]}")  # 商品编号:0 , 商品名称：伊拉克拌面 , 商品数量：111,商品单价：1000

        id = input('请输入想要修改的商品编号(输入q退出)>>:').strip()
        if id == 'q':
            break
        for i in goods_info:
            goods = goods_info[i]
        if int(id) not in goods_info:
            print('商品编号不存在')
            continue
        if goods in shop_card_info:
            print('1:增加, 2：减少, 3:移除商品')
            command = input('请输入功能编号(输入q退出)>>:').strip()
            goods_count = shop_card_info[goods][0]
            goods_count = int(goods_count)
            if command == 'q':
                break
            if command == '1':
                count = input('请输入想要增加的数量>>:').strip()
                goods_count += int(count)
                shop_card_info[goods][0] = goods_count
            elif command == '2':
                count = input('请输入想要减少的数量>>:').strip()
                goods_count -= int(count)
                shop_card_info[goods][0] = goods_count
                if goods_count == 0:
                    del shop_card_info[goods]
            elif command == '3':
                del shop_card_info[goods]
            else:
                print('输入错误')
            db_handler.save(user_dict)
            logger.debug(f"{user_dict['username']}成功修改购物车")


def settlement_shopping_cards_interface(username):
    user_dict = db_handler.select(username)
    shop_card_info = user_dict.get('shopping_cards')
    if not shop_card_info:
        print('购物车未添加任何物品')
    for item in shop_card_info.items():
        print(f"商品名称:{item[0]}  |  商品数量:{item[1][0]}  |  商品单价:{item[1][1]}")
    total_money = 0
    current_balance = user_dict.get('balance')
    for values in shop_card_info.values():
        values[0] = int(values[0])
        total_money += values[0] * values[1]
    if current_balance > total_money:
        current_balance -= total_money
        user_dict['balance'] = current_balance
        user_dict['shopping_cards'] = {}
        print(f'您今日消费：{total_money},您的余额为:{current_balance}')
        db_handler.save(user_dict)
        logger.debug(f"{user_dict['username']}结算购物车")
    else:
        print(f'当前余额不足，请充值')
        return
