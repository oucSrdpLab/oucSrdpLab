# 数据库相关
HOSTNAME="localhost"
PORT=3306
USERNAME="root"
PASSWORD="Publicitstudio"
DATABASE="welab"
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True  # 追踪修改
# SQLALCHEMY_ECHO=True
SECRET_KEY = "dev"
WTF_CSRF_ENABLED = False  # 开发阶段先关闭csrf_token，不然没法调试

# 邮件相关的
MAIL_SERVER = "smtp.qq.com"  # 邮件服务地址，这里以QQ邮箱为例
MAIL_PORT = 465  # QQ邮件端口
MAIL_USERNAME = "1205194626@qq.com"  # 发送邮件的账号名
MAIL_PASSWORD = "tqlltwniqwexjieh"  # 授权码
MAIL_DEFAULT_SENDER = MAIL_USERNAME  # 邮件默认发件人
MAIL_USE_SSL = True  # 使用SSL
MAIL_DEBUG = False

# 缓存相关的配置
CACHE_DEFAULT_TIMEOUT = 60 * 30  # 单位：秒
CACHE_TYPE = "simple"

# flask相关
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True
TEMPLATES_AUTO_RELOAD = True