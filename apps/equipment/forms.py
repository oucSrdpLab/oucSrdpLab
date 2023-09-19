from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from .models import Equipment


class add_equipment_form(FlaskForm):
    """增加一个设备的验证表单"""

    # 名字，不空
    name = StringField(
        "name",
        validators=[DataRequired("设备名不能为空"), Length(max=256, message="设备名不能超过256位")],
    )
    # 型号,可空
    model = StringField(
        "model",
        validators=[Length(max=64, message="型号名不能超过64位")],
    )
    # 种类，可空
    kind = StringField(
        "kind",
        validators=[Length(max=64, message="种类名不能超过64位")],
    )
    # 说明书、可空
    instructions = StringField("instructions")

    def validate_name(self, field):
        """检验设备名字是否存在"""
        equipment = Equipment.query.filter_by(name=field.data).first()
        if equipment:
            raise ValidationError("设备名在数据库中已有，请重新更换")


class delete_equipment_form(FlaskForm):
    """删除一个设备，必须要设备ID"""

    equipment_id = IntegerField("equipment_id", validators={DataRequired("设备ID不能为空")})


class edit_equipment_form(FlaskForm):
    """修改设备信息
    可修改：设备名、型号、种类、说明书、设备剩余情况、设备是否删除
    """

    # id, 不空，不能修改
    equipment_id = IntegerField("equipment_id", validators={DataRequired("设备ID不能为空")})

    # 名字，可空，长度小于256
    name = StringField(
        "name",
        validators=[Length(max=256, message="设备名不能超过256位")],
    )

    # 型号,可空，不能超过64位
    model = StringField(
        "model",
        validators=[Length(max=64, message="型号名不能超过64位")],
    )

    # 种类，可空，不能超过64位
    kind = StringField(
        "kind",
        validators=[Length(max=64, message="种类名不能超过64位")],
    )

    # 说明书、可空
    instructions = TextAreaField("instructions")

    def validate_name(self, field):
        """校验名字是否存在"""
        equipment = Equipment.query.filter_by(name=field.data).first()
        if equipment:
            raise ValidationError("设备名已存在")
