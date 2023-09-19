import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from ..equipment.models import Equipment
from flask import g


class add_appointment_form(FlaskForm):
    """创建预约的表单验证"""

    # start_time需要使用DateTime
    start_time = DateTimeField(
        "start_time",
        validators=[
            DataRequired("开始时间不能为空"),
        ],
    )
    end_time = DateTimeField(
        "end_time",
        validators=[
            DataRequired("结束时间不能为空"),
        ],
    )
    equipment_id = StringField("equipment_id", validators=[DataRequired("预约器材ID不能为空")])
    user_id = StringField("user_id", validators=[DataRequired("预约ID不能为空")])

    def validate_user_id(self, field):
        """检查是不是本人在操作"""
        if g.user.id != field.data:
            raise ValidationError("user_id错误")

    def validate_equipment_id(self, field):
        """检查器材ID是否正确"""
        equipment = Equipment.query.get(field.data)
        if not equipment:
            raise ValidationError("equipment_id错误")

    def validate_end_time(self, field):
        """end_time要大于start_time，如果 field.data <= self.start_time.data 就是一个无效的预约"""
        if field.data <= self.start_time.data:
            raise ValidationError("start_time大于了end_time")


class get_appointment_form(FlaskForm):
    start_time = DateTimeField(
        "start_time",
        format="%Y-%m-%d %H:%M:%S",
        validators=[
            DataRequired("开始时间不能为空"),
        ],
    )
    end_time = DateTimeField(
        "end_time",
        format="%Y-%m-%d %H:%M:%S",
        validators=[
            DataRequired("结束时间不能为空"),
        ],
    )


class edit_appointment_form(FlaskForm):
    """编辑预约，可编辑的有：start_time、end_time、equipment_id"""

    # 预约id
    appointment_id = IntegerField("appointment_id", validators=[DataRequired("无预约的ID")])
    # 预约开始时间
    start_time = DateTimeField("start_time", format="%Y-%m-%d %H:%M:%S")
    # 预约结束时间
    end_time = DateTimeField("end_time", format="%Y-%m-%d %H:%M:%S")
    # 预约设备ID
    equipment_id = IntegerField("equipment_id")

    def validate_equipment_id(self, field):
        if field.data and not Equipment.query.get(field.data):
            raise ValidationError("修改的设备ID不存在")


class allow_appointment_form(FlaskForm):
    start_time = DateTimeField(
        "start_time",
        format="%Y-%m-%d %H:%M:%S",
        validators=[
            DataRequired("开始时间不能为空"),
        ],
    )
    end_time = DateTimeField(
        "end_time",
        format="%Y-%m-%d %H:%M:%S",
        validators=[
            DataRequired("结束时间不能为空"),
        ],
    )
    equipment_id = IntegerField("equipment_id", validators=[DataRequired("预约设备ID不能为空")])

