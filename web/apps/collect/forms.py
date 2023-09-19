import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, FieldList
from wtforms.validators import DataRequired, ValidationError

from flask import g

from ..user import User


class commit_award_form(FlaskForm):
    """提交获奖信息的表单验证类、需要登陆才可以访问的接口、没必要验证user_id，为了简单就不考虑别人帮忙提交的情况
    前端必须提交奖项名称、获奖日期、颁奖机构、获奖等级、获奖人（列表）
    """

    name = StringField("name", validators=[DataRequired("奖项名称不能为空")])
    date = DateField("date", validators=[DataRequired("获奖日期不能为空")])
    institution = StringField("level", validators=[DataRequired("颁奖机构不能为空")])
    level = StringField("level", validators=[DataRequired("获奖等级不能为空")])

    users = StringField("users", validators=[DataRequired("获奖人id不能为空，用'-'分割每个id")])

    def validate_users(self, field):
        """检查这些人在不在数据库里面"""

        # 检查提交的数据里面是不是只有数字和逗号
        for ch in field.data:
            if ch == "-" or ch == " " or ch.isalnum():
                # 如果是逗号，空格，数字就忽略
                continue
            raise ValidationError("获奖人ID的格式有误，只能用英文逗号分割每个id")
        # 数据格式符合要求，那么就用-分割出数字，保存到field.data里面去
        field.data = [int(_.strip()) for _ in field.data.split("-")]
        # print(field.data)

        # 先过滤出所有在users里面的获奖信息, 然后再根据ID分租
        exists_user = User.query.filter(User.id.in_(field.data)).group_by(User.id).all()

        # 检查组数和users长度是否一致
        if len(exists_user) != len(field.data):
            raise ValidationError("有获奖人ID不中数据库里面")

        # 把查到的这些人保存一份
        self._my_exists_user = exists_user


class get_award_form(FlaskForm):
    pass


class edit_award_form(FlaskForm):
    pass
