import os
from lib import common
import pickle
file_name = 'userinfo.txt'


status_data = {
    'username': None,
    'is_login': False
}


def register():
    info=[]
    if status_data['is_login']:
        print('%s已登录' % status_data['username'])
        return
    while True:
        username = input('请输入您的用户名>>:').strip()
        with open(file_name, 'r') as f:
            for line in f:
                print(line,type(line))
                # real_name = line['username']
                real_name = pickle.load(f)
                print(real_name,type(real_name))
                if username == real_name:
                    print('用户名已存在')
                    break
            else:
                password = input('请输入您的密码>>:').strip()
                if password:
                    # user_info = '%s,%s\n' % (username, password)
                    user_info = {'username': username, 'password': password, 'balance': 0}
                    with open(file_name, 'a') as f:
                        # json.dump(user_info, f,end='\n')
                        info_dic = pickle.dump(user_info, f)
                        info.append(info_dic)
                        # f.write(user_info)
                    print(f'{username}注册成功')
                    break
                else:
                    print('输入不能为空')


def login():
    while True:
        if status_data['is_login']:
            print('%s已登录' % status_data['username'])
            return
        username = input('请输入您的用户名>>:').strip()
        password = input('请输入您的密码>>:').strip()
        with open(file_name, 'r') as f:
            data = pickle.load(f)
            user,pwd = data['username'],data['password']
            if user == username and pwd == password:
                status_data['is_login'] = True
                status_data['username'] = username
                print('%s成功登录' % status_data['username'])
                break
            else:
                print('用户名或者密码错误')


@common.outter
def pay():
    while True:
        money = input('请输入充值金额>>:').strip()
        if not money.isdigit:
            print('请输入正确数字')
        money = int(money)
        with open(file_name,  encoding='utf-8')as f:
            user_info = pickle.load(f)
        user_info['balance'] += money
        with open(file_name, 'w', encoding='utf-8')as f:
            pickle.dump(user_info, f)
            print('%s充值成功%s元' %(status_data['username'],money))
            break
@common.outter
def check_balance():
    pass


@common.outter
def withdraw():
    pass


@common.outter
def shopping():
    pass


@common.outter
def transfer_accounts():
    pass


def out():
    exit()


command_dict = {
    '1': ['注册', register],
    '2': ['登录', login],
    '3': ['支付', pay],
    '4': ['查看余额', check_balance],
    '5': ['提现', withdraw],
    '6': ['购物', shopping],
    '7': ['转账', transfer_accounts],
    'q': ['退出', out],
}


def main_body():
    while True:
        for choice, command in command_dict.items():
            print(choice, command_dict[choice][0])
        choice = input('请输入您的指令>>:').strip()
        if choice in command_dict:
            command_dict[choice][1]()
        else:
            print('输入有误，请重新输入')



