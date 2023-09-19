from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from apps.exts import db


class User(db.Model):
    """用户表，目前有id、username、password、email、phone、identification、is_delete、avatar（暂时还不能使用）"""

    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    # 用户名字段，唯一，不能空。可以用邮箱、手机号、普通字符作为用户名
    # 如果用户没有传入username，那就Email或者Phone作为默认用户名

    username = Column(String(32), unique=True, nullable=False, comment="用户名")
    # 密码，不能空。
    password = Column(String(256), nullable=False, comment="密码")

    # 邮箱字段，唯一，可空
    email = Column(String(32), nullable=True, unique=True, comment="邮箱")
    # 手机号字段，唯一，可空
    phone = Column(String(32), nullable=True, unique=True, comment="手机号")
    # 身份，默认学生
    identification = Column(String(32), default="student", comment="身份")

    # 账号是否删除，用标记Flase的方式删除
    is_delete = Column(Boolean, default=False, comment="账号是否删除")

    def __repr__(self):
        return "<User %s>" % self.username
