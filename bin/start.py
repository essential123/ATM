from core.src import main_body
file_name = 'userinfo.txt'
import os

if __name__ == '__main__':

    if os.path.exists(file_name):
        pass
    else:
        with open(file_name, 'a', encoding='utf-8') as f:
            pass
        # os.mknod(file_name)

    main_body()