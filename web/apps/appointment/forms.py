import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, IntegerField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Length, Optional, NumberRange
from ..equipment.models import Equipment
from flask import g


from datetime import datetime


class add_appointment_form(FlaskForm):
    """创建预约的表单验证"""

    def validate_start_time(self, field):
        """检查开始时间是否有效"""
        if field.data and isinstance(field.data, datetime):
            field.data = field.data.replace(second=0)  # 将秒数置为0

    def validate_end_time(self, field):
        """检查结束时间是否有效"""
        if field.data and isinstance(field.data, datetime):
            field.data = field.data.replace(second=0)  # 将秒数置为0

    start_time = StringField("start_time", validators=[DataRequired("开始时间不能为空"), validate_start_time])
    end_time = StringField("end_time", validators=[DataRequired("结束时间不能为空"), validate_end_time])
    equipment_id = StringField("equipment_id", validators=[DataRequired("预约器材ID不能为空")])
    user_id = StringField("user_id", validators=[DataRequired("预约ID不能为空")])
    equipment_name = StringField("equipment_name",validators=[DataRequired("仪器名不能为空")])
    telephone = StringField("telephone", validators=[DataRequired("电话不能为空")])
    review_reason = StringField("review_reason", validators=[DataRequired("预约原因不能为空"), Length(max=255)])
    number_of_applicants = IntegerField("number_of_applicants", validators=[DataRequired("预约人数不能为空"), NumberRange(min=1)])
    applicant_name = StringField("applicant_name", validators=[DataRequired("预约人姓名不能为空"), Length(max=255)])
    applicant_student_id = StringField("applicant_student_id", validators=[DataRequired("预约人学号不能为空"), Length(max=255)])

    def validate_equipment_id(self, field):
        """检查器材ID是否正确"""
        equipment = Equipment.query.get(field.data)
        if not equipment:
            raise ValidationError("equipment_id错误")

    def validate_end_time(self, field):
        """检查是否大于start_time"""
        if field.data <= self.start_time.data:
            raise ValidationError("开始时间大于了结束时间")


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
    #start_time = DateTimeField("start_time", format="%Y-%m-%d %H:%M:%S")
    # 预约结束时间
    #end_time = DateTimeField("end_time", format="%Y-%m-%d %H:%M:%S")
    # 预约设备ID
    #equipment_id = IntegerField("equipment_id")
    is_checked = IntegerField("is_checked", validators=[DataRequired("是否审核不能为空")])

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

