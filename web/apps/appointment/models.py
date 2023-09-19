from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean

from sqlalchemy.orm import relationship

from web.apps.exts import db

from datetime import datetime


class Appointment(db.Model):
    """预约表，目前有id、start_time 、end_time、is_sign、ceate_time、user_id、is_delete、manager_id、equipment_id"""

    __tablename__ = "appointment"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    # 预约开始时间、不空，这个地方是否要唯一待考虑
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    # 预约结束时间、不空
    end_time = Column(DateTime, nullable=False, comment="结束时间")
    # 预约人是否签到、默认没有
    is_sign = Column(Boolean, default=False, comment="是否签到")
    # 预约人是否签退
    is_sign_out = Column(Boolean, default=False, comment="是否签退")
    # 预约创建时间、自动取当前系统时间
    ceate_time = Column(DateTime, default=datetime.now, comment="预约创建时间")
    # 预约是否删除，默认没有
    is_delete = Column(Boolean, default=False, comment="是否删除")

    # 外键字段，一个预约对应一个学生，一个学生对应多个预约。
    user_id = Column(Integer, ForeignKey("user.id"), comment="预约人ID")
    # 外键字段，一个预约对应一个经办人，一个经办人对应多个预约。
    manager_id = Column(Integer, ForeignKey("user.id"), comment="经办人ID")
    # 外键字段，一个设备应该对应一个预约，每个设备只能被一个人在同一时间段内使用，避免冲突。
    # 这里考虑的一个型号设备只有一个，如果有个相同设备，应该往设备表里面多次添加
    equipment_id = Column(Integer, ForeignKey("equipment.id"), comment="设备ID")

    user = relationship("User", backref="appointment_user", foreign_keys=[user_id],uselist=True)
    manager = relationship(
        "User", backref="appointment_manager", foreign_keys=[manager_id],uselist=True
    )

    def __repr__(self):
        #  重写__repr__，为了更好的区分
        return "<Appointment %s——%s>" % (self.start_time, self.end_time)