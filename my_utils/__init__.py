"""一些常使用的工具函数"""
import functools
import random
from datetime import datetime
from flask import g


def login_required(func):
    """
    最基本的登录权限校验
    """

    @functools.wraps(func)
    def wrapper_view(*args, **kwargs):
        if not g.get("user") or g.user.is_delete:
            # 如果全局g里面没有user，或者user是被注销了的，那就重定向到login接口
            return {
                "msg": "请先登录"
            }
        else:
            # 否则就允许使用视图函数，把参数给视图函数
            return func(*args, **kwargs)

    return wrapper_view


def get_random():
    """生成三个8位二进制数，颜色的三原色"""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def generate_verification_code():
    # 生成一个六位随机数作为验证码
    return random.randint(100000, 999999)


def timeStr_to_dataTime(date_string, format):
    # 把时间字符串尝试根据格式转为datetime
    result = None
    try:
        # 尝试转换，如果格式不符合，抛出ValueError异常，
        result = datetime.strptime(date_string, format)
    except ValueError as e:
        result = None
        print(e)
    return result
