from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from web.apps.exts import db


class Equipment(db.Model):
    """设备表"""

    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")

    # 设备名称，唯一、不为空
    name = Column(String(256), unique=True, nullable=False, comment="设备名称")

    # 设备种类（仪器、房间）
    kind = Column(String(64), nullable=False, comment="设备种类")

    # 设备位置
    location = Column(String(256), nullable=True, comment="设备位置")

    # 设备人数
    capacity = Column(Integer, nullable=True, comment="设备人数")

    # 设备简图，用来存放图片URL
    image_url = Column(Text, nullable=True, comment="设备简图")

    image_inside = Column(Text, nullable=True, comment="inside")

    brief = Column(String(256), unique=True, nullable=False, comment="brief")

    disable = Column(Integer, nullable=True, comment="是否禁用")

    # 通过设备反查预约, 这里考虑的一个型号设备只有一个，如果有个相同设备，应该往设备表里面多次添加
    appointments = relationship("Appointment", backref="equipment", uselist=True)

    def __repr__(self):
        return "<Equipment %s>" % self.name
