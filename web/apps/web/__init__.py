from flask import Blueprint

# 建立蓝图,传递参数
web_bp = Blueprint(
    'web_bp',
    __name__,
    template_folder="web_templates",
    static_folder='web_static',
    url_prefix='',  # url前缀
)

from .views import *
