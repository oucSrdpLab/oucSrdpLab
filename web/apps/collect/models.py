from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Boolean,
    Text,
    Date,
)

from sqlalchemy.orm import relationship

from web.apps.exts import db
import datetime


UserToAward = db.Table(
    # 获奖人和奖项是多对多关系，需要手动建一个中间表，
    "user_to_award",
    Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    Column(
        "award_id", db.Integer, db.ForeignKey("award.id"), primary_key=True
    ),  # 注意大小写
)


class Award(db.Model):
    """奖项名称、获得日期、颁奖机构、获奖等级"""

    __tablename__ = "award"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    # 奖项名称，不空，长度最大256, 不唯一，一个奖项有多个人同时获得,每个人可能获得多个奖项。
    # 感觉一对多和多对多都行
    name = Column(String(256), unique=False, nullable=False, comment="奖项名称")

    # 获奖日期, 默认为当前时间
    date = Column(Date, default=datetime.date.today, comment="获奖日期")

    # 颁奖机构，长度低于256，不空
    institution = Column(String(256), nullable=False, comment="颁奖机构")

    # 获奖等级，不空，字符串长度低于64
    level = Column(String(64), nullable=False, comment="获奖等级")

    # 获奖人ID, 一个用户是可以获得多个奖，一个奖也会被多个人获得
    users = relationship("User", backref="awards", secondary=UserToAward)

    def __repr__(self):
        #  重写__repr__，为了print时好看，“自我描述” 功能
        return "<Award %s>" % self.name