from flask import Flask
from flask_migrate import Migrate
from web.apps.exts import db, mail, cache

from web.apps.appointment import appointment_bp
from web.apps.web import web_bp
from web.apps.user import user_bp
from web.apps.equipment import equipment_bp
from web.apps.sign import sign_bp
from web.apps.collect import collect_bp


# 这里用as重命名是为了用户启动时不用区分是dev_config还是pro_config
from configs import dev_config as config

# 实例化flask
app = Flask(__name__)

# 从文件里面加载配置项
app.config.from_object(config)

# 注册蓝图
app.register_blueprint(web_bp)  # 注册web蓝图
app.register_blueprint(user_bp)  # 注册user蓝图
app.register_blueprint(appointment_bp)
app.register_blueprint(equipment_bp)
app.register_blueprint(sign_bp)
app.register_blueprint(collect_bp)

# 将app和SQLAlchemy关联起来，初始数据库
db.init_app(app)

# 数据迁移文件
migrate = Migrate(app, db)

# 发邮箱
mail.init_app(app)

# 缓存
cache.init_app(app)
