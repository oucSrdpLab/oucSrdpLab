from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from .models import Equipment


class AddEquipmentForm(FlaskForm):
    """增加一个设备的验证表单"""

    # 名字，不为空
    name = StringField(
        "name",
        validators=[DataRequired("设备名不能为空"), Length(max=256, message="设备名不能超过256位")],
    )

    # 种类，可为空
    kind = StringField(
        "kind",
        validators=[Length(max=64, message="种类名不能超过64位")],
    )

    # 设备位置，可为空
    location = StringField(
        "location",
        validators=[Length(max=256, message="设备位置不能超过256位")],
    )

    # 设备人数，可为空
    capacity = IntegerField("capacity")

    # 设备简图，可为空
    image_url = StringField(
        "image_url",
        validators=[Length(max=512, message="设备图片URL不能超过512位")],
    )

    def validate_name(self, field):
        """检验设备名字是否存在"""
        equipment = Equipment.query.filter_by(name=field.data).first()
        if equipment:
            raise ValidationError("设备名在数据库中已有，请重新更换")


class DeleteEquipmentForm(FlaskForm):
    """删除一个设备，必须要设备ID"""

    equipment_id = IntegerField("equipment_id", validators=[DataRequired("设备ID不能为空")])


class EditEquipmentForm(FlaskForm):
    """修改设备信息
    可修改：设备名、种类、位置、人数、简图
    """

    # id, 不为空，不能修改
    equipment_id = IntegerField("equipment_id", validators=[DataRequired("设备ID不能为空")])

    # 名字，可为空，长度小于256
    name = StringField(
        "name",
        validators=[Length(max=256, message="设备名不能超过256位")],
    )

    # 种类，可为空，长度小于64
    kind = StringField(
        "kind",
        validators=[Length(max=64, message="种类名不能超过64位")],
    )

    # 位置，可为空，长度小于256
    location = StringField(
        "location",
        validators=[Length(max=256, message="设备位置不能超过256位")],
    )

    # 人数，可为空
    capacity = IntegerField("capacity")

    # 简图，可为空，长度小于512
    image_url = StringField(
        "image_url",
        validators=[Length(max=512, message="设备图片URL不能超过512位")],
    )

    def validate_name(self, field):
        """校验设备名字是否存在"""
        equipment = Equipment.query.filter_by(name=field.data).first()
        if equipment:
            raise ValidationError("设备名已存在")
