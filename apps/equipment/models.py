from sqlalchemy import Column, Integer, String, Boolean, Text

from sqlalchemy.orm import relationship

from apps.exts import db


class Equipment(db.Model):
    """设备表"""

    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    # 设备名，唯一、不空
    name = Column(String(256), unique=True, nullable=False, comment="设备名")
    # 型号，不唯一、可空
    model = Column(String(64), nullable=True, comment="型号")
    # 种类，不唯一、可空
    kind = Column(String(64), nullable=True, comment="种类")
    # 说明书、不唯一、可空
    instructions = Column(Text, nullable=True, default="还没有说明书", comment="说明书")

    # 设备是否在使用、默认有
    is_used = Column(Boolean, default=False, comment="设备是否在使用")

    # 设备是否删除、默认没有。
    is_delete = Column(Boolean, default=True, comment="设备是否删除")

    # 通过设备反查预约, 这里考虑的一个型号设备只有一个，如果有个相同设备，应该往设备表里面多次添加
    appointments = relationship("Appointment", backref="equipment", uselist=True)

    def __repr__(self):
        #  重写__repr__，为了更好的区分
        return "<Equipment %s>" % self.name
