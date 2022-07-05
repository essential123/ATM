def outter(func):
    from core import src
    def wrapper(*args,**kwargs):
        if src.status_data['is_login']:
            res = func(*args,**kwargs)
            return res
        else:
            src.login()
    return wrapper
