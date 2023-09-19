import functools
from io import BytesIO
from flask import jsonify, make_response, session, request, g, redirect, url_for
from apps.user import user_bp
from my_utils import generate_verification_code, get_random, login_required
from .models import User
from apps.exts import db, mail, cache
from werkzeug.security import generate_password_hash
from flask_mail import Message
from .forms import (
    change_password_form,
    change_userinfo_form,
    login_form,
    register_form,
    reset_password_form,
)
from PIL import Image, ImageDraw, ImageFont

import os
import random


# 获取当前views.py路径，然后将当前目录下static/ttf里面的字体加入进来
current_path = os.path.dirname(__file__)
ttf_file_path = os.path.join(current_path, "static", "ttf", "ziti.ttf")


@user_bp.route("/login", methods=["POST"])
def login():
    """用户登录, 访问链接是/user/login，只能POST"""
    form = login_form()
    response_data = {"msg": "登录失败"}

    if form.validate_on_submit():
        # 验证通过了，就在从form取出在校验字段时间存储的user
        user = form._my_user

        response_data["msg"] = "登陆成功"
        response_data["user_id"] = user.id
        response_data["username"] = user.username
        response_data["email"] = user.email
        response_data["phone"] = user.phone
        response_data["identification"] = user.identification

        session.clear()
        # 将ID保存
        session["user_id"] = user.id
    else:
        # 返回错误字段信息
        response_data.update(form.errors)

    return jsonify(response_data)


@user_bp.route("/register", methods=["POST"])
def register():
    """用户注册, 访问链接是/user/register，只能POST"""
    """小bug，不管是调用了注册接口还是登录接口，这里都需要先把session清空"""
    form = register_form()
    response_data = {"msg": "注册失败"}

    if form.validate_on_submit():
        # 检验合格，就在数据库里面创建user

        # 验证通过了，就在从form取出在校验字段
        validate_data = form.data
        validate_data.pop("code")  # 删除验证码
        validate_data.pop("confirm_password")  # 删除确认密码

        validate_data["password"] = generate_password_hash(form.password.data)

        validate_data.update(form._my_type_data)

        user = User(**validate_data)
        db.session.add(user)
        db.session.commit()

        session.clear()
        # 将ID保存
        session["user_id"] = user.id
        # 构造返回数据
        response_data["user_id"] = user.id
        response_data["msg"] = "注册成功"
        response_data["username"] = user.username
        response_data["email"] = user.email
        response_data["phone"] = user.phone
        response_data["identification"] = user.identification

    else:
        # 返回错误字段信息
        response_data.update(form.errors)

    return jsonify(response_data)


@user_bp.route("/login_out", methods=["GET"])
def login_out():
    """退出登录"""
    session.clear()
    return jsonify({"msg": "退出登录"})


@user_bp.before_app_request
def load_user():
    """根据session中的user_id加载user，因为后面的操作都需要user，所以需要让他在每次请求前就执行这个函数"""
    # 从session中获取user_id
    user_id = session.get("user_id")

    if user_id:
        # 如果有user_id，那么就去数据库查找对应的user
        user = User.query.get(user_id)
        if user:
            g.user = user
        else:
            # 这个user_id不在数据库里面，就把g中的user销毁
            g.user = None
    else:
        g.user = None


@user_bp.route("/get_image_code", methods=["GET"])
def get_image_code():
    "获取图片验证码"
    # 设置图片模式。大小，颜色
    img_obj = Image.new("RGB", (430, 35), get_random())
    img_draw = ImageDraw.Draw(img_obj)  # 产生一个画笔对象
    img_font = ImageFont.truetype(ttf_file_path, 30)  # 字体样式 大小

    # 随机验证码  六位数的随机验证码  数字 小写字母 大写字母
    code = ""
    for i in range(6):
        random_upper = chr(random.randint(65, 90))
        random_lower = chr(random.randint(97, 122))
        random_int = str(random.randint(0, 9))
        # 从上面三个里面随机选择一个
        tmp = random.choice([random_lower, random_upper, random_int])
        # 将产生的随机字符串写入到图片上
        """
        一个个写能够控制每个字体的间隙 而生成好之后再写的话间隙就没法控制了
        """
        img_draw.text((i * 60 + 60, -2), tmp, get_random(), img_font)
        # 拼接随机字符串
        code += tmp
    # print("图形验证码：", code)
    session["image_code"] = code
    # 返回图片给前端
    io_obj = BytesIO()
    img_obj.save(io_obj, "png")
    # 获取缓冲区里面的值，即图片的二进制数据返回给前端
    response = make_response(io_obj.getvalue())
    # print(io_obj.getvalue())

    response.headers["Content-Type"] = "image/png"
    return response


@user_bp.route("/send_code_by_email", methods=["POST"])
def send_code_by_email():
    """'用邮箱发送验证码"""
    response_data = {"msg": "发送失败"}

    # 第一步从request获取邮箱地址
    email_addr = request.json.get("email", None)
    if not email_addr:
        # 如果没有邮件地址，直接返回
        return jsonify(response_data)

    # 否则先生成6位验证码，
    code = generate_verification_code()
    message = Message("web网站的验证码", recipients=[email_addr])
    message.body = "您的验证码为:%s，有效时间为30分钟，请不要告诉他人!" % code

    # 通过是否出现异常判断发生成功与否
    try:
        mail.send(message)
        response_data["msg"] = "发送成功"
        mail_code_key_word = "mail_%s_code" % email_addr  # 由发送邮箱地址作为key
        cache.set(mail_code_key_word, code)

    except Exception as e:
        response_data["msg"] = "发送失败"
        print(str(e))
    finally:
        return jsonify(response_data)


@user_bp.route("/reset_password", methods=["POST"])
def reset_password():
    """找回密码（未登录的情况）"""
    response_data = {"msg": "密码找回失败"}
    form = reset_password_form()
    if form.validate_on_submit():
        # 验证通过了，就在从form取出在校验字段时间存储的user
        user = form._my_user
        user.password = generate_password_hash(form.data.get("new_password"))
        db.session.commit()
        response_data["msg"] = "成功重置密码"
    else:
        # 返回错误字段信息
        response_data.update(form.errors)
    return response_data


@user_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    """修改密码（已登录的情况）"""
    response_data = {"msg": "密码修改失败"}
    form = change_password_form()
    if form.validate_on_submit():
        # 验证通过了，就在从form取出在校验字段时间存储的user
        user = form._my_user
        user.password = generate_password_hash(form.data.get("new_password"))
        db.session.commit()
        response_data["msg"] = "成功修改密码"
    else:
        # 返回错误字段信息
        response_data.update(form.errors)
    return response_data


@user_bp.route("/change_userinfo", methods=["POST"])
@login_required
def change_userinfo():
    """修改用户信息（已登录的情况）"""
    form = change_userinfo_form()
    response_data = {"msg": "信息更新失败"}
    if form.validate_on_submit():
        # 字段检查没问题，现在取出g里面的user,核对id

        if g.user.id == form.data["user_id"]:
            for key, value in form.data.items():
                if key == "user_id" or not value:
                    # 如果是ID字段或者没有值，那就不更新数据。
                    continue
                # 拼接更新语句
                excc_str = "g.user.%s = '%s'" % (key, value)
                exec(excc_str)
            # 提交数据库
            db.session.commit()
            # 构造返回数据
            response_data["msg"] = "信息更新成功"
            response_data["user_id"] = g.user.id
            response_data["username"] = g.user.username
            response_data["email"] = g.user.email
            response_data["phone"] = g.user.phone
            response_data["identification"] = g.user.identification
        else:
            response_data["msg"] = "不是本人"
    else:
        # 返回错误字段信息
        response_data.update(form.errors)

    return jsonify(response_data)