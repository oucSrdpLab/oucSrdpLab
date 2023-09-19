from flask import Blueprint

# 建立 设备 蓝图，主要负责 设备 相关的逻辑处理
sign_bp = Blueprint(
    "sign_bp",
    __name__,
    url_prefix="/sign",
)

# 这个导入必须要放在最下面
from .views import *
