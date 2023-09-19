from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache

# 创建SQL alchemy
db = SQLAlchemy()
# 创建邮件
mail = Mail()
# 创建缓存
cache = Cache()
