from flask import Blueprint

# 建立 设备 蓝图，主要负责 设备 相关的逻辑处理
equipment_bp = Blueprint(
    "equipment_bp",
    __name__,
    url_prefix="/equipment",
)


from .views import *
