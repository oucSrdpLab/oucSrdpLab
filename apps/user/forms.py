import re
from flask_wtf import FlaskForm
from sqlalchemy import or_
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Regexp
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash
from apps.exts import cache


class register_form(FlaskForm):
    # 注册表单验证

    username = StringField(
        "username",
        validators=[
            DataRequired("用户名不能为空"),
            Length(max=32, message="用户名长度不能超过32位"),
        ],
    )

    # 密码不一定需要，可能是验证码注册
    password = PasswordField(
        "password",
        validators=[
            DataRequired(
                "密码不能为空",
            ),
            Length(max=256, message="密码长度不能超过256位"),
            EqualTo("confirm_password", message="密码不一样"),
        ],
    )
    confirm_password = PasswordField(
        "confirm_password",
        validators=[
            DataRequired("确认密码不能为空"),
            Length(max=256, message="确认密码长度不能超过256位"),
        ],
    )
    # 验证码不一定需要，可能是账号和密码注册
    code = StringField("code", validators=[Length(max=6, message="验证码长度为6位")])
    identification = StringField("identification")

    def validate_username(self, field):
        """局部钩子,前面的validate是标识写法,后面的username是检验的字段名"""
        """检验用户名,并判断用户输入的账号类型"""
        if re.match(r"^1[3-9][0-9]{9}$", field.data):
            # 如果输入的是一个11位的手机号，且首位是1，第二位是3-9，则认为是手机号
            input_type = "phone"
        elif re.match(r"^.+@.+$", field.data):
            # 如果输入的是一个带有@符号的字符串，则认为是邮箱
            input_type = "email"
        else:
            # 否则认为是用户名
            input_type = "username"
        type_data = {input_type: field.data}
        self._my_type_data = type_data
        user = User.query.filter_by(**type_data).first()
        if user:
            # 如果存在用户，就不允许注册，抛出异常
            raise ValidationError("用户已存在")


class login_form(FlaskForm):
    # 登录表单验证
    # 注册表单验证
    username = StringField(
        "username",
        validators=[
            DataRequired("用户名不能为空"),
            Length(max=32, message="用户名长度不能超过32位"),
        ],
    )
    # 验证码不一定需要，可能是账号和密码登录
    code = StringField("code", validators=[Length(max=6, message="验证码长度为6位")])
    password = PasswordField(
        "password",
        validators=[
            Length(max=256, message="密码长度不能超过256位"),
        ],
    )

    def validate_code(self, code):
        # 校验验证码，这里的code只与发往邮箱验证码做校对
        if code.data and re.match(r"^.+@.+$", self.data["username"]):
            # 如果username是邮箱且有验证码，才去校验邮箱验证码
            mail_code_key_word = "mail_%s_code" % self.data["username"]
            mail_code = str(cache.get(mail_code_key_word))
            if (
                code.data != "888888" and mail_code != code.data
            ):  # 888888是为了方便测试的，不然每次都发太麻烦了
                raise ValidationError("邮箱或者验证码错误")
            else:
                self._my_user = User.query.filter_by(
                    email=self.data["username"]
                ).first()
        elif not self.data["password"]:
            # 是邮箱登录，但是验证码或者密码两个里面一个都没有
            raise ValidationError("请输入账号密码，或者验证码")

    def validate_username(self, field):
        """局部钩子,前面的validate是标识写法,后面的username是检验的字段名"""
        """检验用户名,并判断用户输入的账号类型"""
        if re.match(r"^1[3-9][0-9]{9}$", field.data):
            # 如果输入的是一个11位的手机号，且首位是1，第二位是3-9，则认为是手机号
            input_type = "phone"
        elif re.match(r"^.+@.+$", field.data):
            # 如果输入的是一个带有@符号的字符串，则认为是邮箱
            input_type = "email"
        else:
            # 否则认为是用户名
            input_type = "username"
        type_data = {input_type: field.data}

        user = User.query.filter_by(**type_data).first()
        if not user:
            # 如果不存在用户，就不允许登录，抛出异常
            raise ValidationError("账号或密码错误")
        elif self.data["password"]:
            # 有密码字段，就检查密码，没密码就不管
            if not check_password_hash(user.password, self.password.data):
                # 检查密码不对
                raise ValidationError("账号或密码错误")
            else:
                # 密码也对啦
                self._my_user = user
        elif not self.data["code"]:
            # 没密码，也没验证码
            raise ValidationError("请输入账号密码，或者验证码")


class reset_password_form(FlaskForm):
    # 找回密码表单验证

    # 用户名一定要有
    username = StringField(
        "username",
        validators=[
            DataRequired("用户名不能为空"),
            Length(max=32, message="用户名长度不能超过32位"),
        ],
    )
    # 新密码一定要有
    new_password = PasswordField(
        "new_password",
        validators=[
            DataRequired("新密码不能为空"),
            Length(max=256, message="确认密码长度不能超过256位"),
            EqualTo("confirm_password", message="密码不一样"),
        ],
    )
    # 确认新密码一定要有
    confirm_password = PasswordField(
        "confirm_password",
        validators=[
            DataRequired("确认密码不能为空"),
            Length(max=256, message="确认密码长度不能超过256位"),
        ],
    )

    # 验证码一定有，可能是账号和密码找回
    code = StringField(
        "code",
        validators=[Length(max=6, min=6, message="验证码长度为6位"), DataRequired("验证码不能位为空")],
    )

    def validate_username(self, field):
        """局部钩子,前面的validate是标识写法,后面的username是检验的字段名"""
        """检验用户名,并判断用户输入的账号类型"""
        if re.match(r"^1[3-9][0-9]{9}$", field.data):
            # 如果输入的是一个11位的手机号，且首位是1，第二位是3-9，则认为是手机号
            input_type = "phone"
        elif re.match(r"^.+@.+$", field.data):
            # 如果输入的是一个带有@符号的字符串，则认为是邮箱
            input_type = "email"
        else:
            # 否则认为是用户名
            input_type = "username"
        self._my_type_data = {input_type: field.data}

    def validate_code(self, code):
        # 校验验证码，这里的code只与发往邮箱验证码做校对
        if re.match(r"^.+@.+$", self.data["username"]):
            # 如果username是邮箱，再去邮箱验证码
            mail_code_key_word = "mail_%s_code" % self.data["username"]
            mail_code = str(cache.get(mail_code_key_word))
            if (
                code.data != "888888" and mail_code != code.data
            ):  # 888888是为了方便测试的，不然每次都发太麻烦了
                raise ValidationError("邮箱或者验证码错误")
            else:
                user = User.query.filter_by(**self._my_type_data).first()
                if not user:
                    raise ValidationError("用户不存在")
                else:
                    # 将用户返回
                    self._my_user = user
        else:
            raise ValidationError("获取了验证码，但是username并不是邮箱")


class change_password_form(FlaskForm):
    # 修改密码表单验证

    # 用户名一定要
    username = StringField(
        "username",
        validators=[
            DataRequired("用户名不能为空"),
            Length(max=32, message="用户名长度不能超过32位"),
        ],
    )
    # 新密码一定要有
    new_password = PasswordField(
        "new_password",
        validators=[
            DataRequired("新密码不能为空"),
            Length(max=256, message="确认密码长度不能超过256位"),
            EqualTo("confirm_password", message="密码不一样"),
        ],
    )
    # 确认新密码一定要有
    confirm_password = PasswordField(
        "confirm_password",
        validators=[
            DataRequired("确认密码不能为空"),
            Length(max=256, message="确认密码长度不能超过256位"),
        ],
    )
    # 原密码不一定需要，可能是验证码注册
    old_password = PasswordField(
        "password",
        validators=[
            Length(max=256, message="密码长度不能超过256位"),
        ],
    )
    # 验证码不一定有，可能是账号和密码找回
    code = StringField("code", validators=[Length(max=6, message="验证码长度为6位")])

    def validate_username(self, field):
        """局部钩子,前面的validate是标识写法,后面的username是检验的字段名"""
        """检验用户名,并判断用户输入的账号类型"""
        if re.match(r"^1[3-9][0-9]{9}$", field.data):
            # 判断输入为电话号码
            input_type = "phone"
        elif re.match(r"^.+@.+$", field.data):
            # 判断输入为邮箱
            input_type = "email"
        else:
            # 判断输入为用户名
            input_type = "username"
        type_data = {input_type: field.data}
        self._my_type_data = type_data
        user = User.query.filter_by(**type_data).first()
        if not user:
            raise ValidationError("用户不存在")
        else:
            self._my_user = user

    def validate_old_password(self, old_password):
        if "username" in self._my_type_data or not self.data["code"]:
            # username不是Email和phone验证方式，或者没有传输code，那么就需要校验原始密码和用户输入的密码是否一样
            if not check_password_hash(self._my_user.password, old_password.data):
                # 原密码与数据库密码不一样
                raise ValidationError("原密码与数据库密码不一样")

    def validate_code(self, code):
        # 校验验证码，这里的code只与发往邮箱验证码做校对
        if code.data:
            # 如果username是邮箱，再去邮箱验证码
            mail_code_key_word = "mail_%s_code" % self.data["username"]
            mail_code = str(cache.get(mail_code_key_word))
            if code.data != "888888" and mail_code != code.data:
                # 888888是为了方便测试的，不然每次都往邮箱发太麻烦了
                raise ValidationError("邮箱或者验证码错误")


class change_userinfo_form(FlaskForm):
    # 修改用户信息
    # 用户id传入，作为判断当前登录用户和修改用户是不是同一个的依据
    user_id = StringField("user_id", validators=[DataRequired("用户ID不能为空")])

    # 用户名修改
    username = StringField(
        "new_username",
        validators=[
            Length(max=32, message="用户名长度不能超过32位"),
        ],
    )
    # 邮箱修改
    email = EmailField(
        "new_email",
        validators=[
            Length(max=32, message="邮箱长度不能超过32位"),
            Regexp("^.+@.+$", message="邮箱格式不对"),
        ],
    )
    # 手机号修改
    phone = StringField(
        "new_phone",
        validators=[
            Length(max=11, message="手机号不能超过11位"),
            Regexp("^1[3-9][0-9]{9}$", message="手机号格式不对"),
        ],
    )

    def is_exists(self, field):
        """
        调用此函数完成校验
        """

        user = User.query.filter(
            or_(
                User.username == field.data,
                User.email == field.data,
                User.phone == field.data,
            )
        ).first()
        return user != None

    def validate_new_username(self, new_username):
        # 校验username是否存在
        if self.is_exists(new_username):
            raise ValidationError("新用户名已被使用")

    def validate_new_email(self, new_email):
        # 校验username是否存在
        if self.is_exists(new_email):
            raise ValidationError("新邮箱已被使用")

    def validate_new_phone(self, new_phone):
        # 校验username是否存在
        if self.is_exists(new_phone):
            raise ValidationError("新手机号已被使用")