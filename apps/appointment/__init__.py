from flask import Blueprint

# 建立预约蓝图，主要负责预约相关的逻辑处理
appointment_bp = Blueprint(
    "appointment_bp",
    __name__,
    url_prefix="/appointment",
)

from .views import *
