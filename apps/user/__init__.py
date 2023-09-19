from flask import Blueprint

# 建立user蓝图，主要负责用户相关的逻辑处理
user_bp = Blueprint(
    "user_bp",
    __name__,
    url_prefix="/user",  # url前缀
)

from ..user.views import *
