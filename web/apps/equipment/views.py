import base64
import os
from flask import request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from .models import Equipment
from . import equipment_bp
from .forms import AddEquipmentForm, DeleteEquipmentForm, EditEquipmentForm
from web.my_utils import login_required
from web.apps.exts import db


@equipment_bp.route("/all", methods=["GET"])
def all():
    """获取所有的设备ID和名字"""
    response_data = {"msg": "获取失败"}
    equipments_obj = Equipment.query.all()
    equipments_list = []

    if equipments_obj:
        # 在数据库查到了设备，才提取名字
        for equipment in equipments_obj:
            # 设备是未删除，并且没有使用，才可以去提取返回数据
            equipments_list.append(
                {
                    "id": equipment.id,
                    "name": equipment.name,
                    "location": equipment.location,
                    "kind": equipment.kind,
                    "capacity": equipment.capacity,
                    "image_url": equipment.image_url,
                    "image_inside":equipment.image_inside,
                    "brief":equipment.brief,
                    "disable":equipment.disable
                }
            )

    if equipments_list:
        response_data["msg"] = "获取成功"
    else:
        response_data["msg"] = "没有设备"

    response_data["data"] = equipments_list

    return response_data


@equipment_bp.route("/add", methods=["POST"])
# @login_required
def add():
    """添加一个设备，必须要登录，且只有老师才能添加"""

    response_data = {"msg": "添加失败"}

    form = AddEquipmentForm()
    if form.validate_on_submit():
        # 通过form校验，存数据库
        equipment = Equipment(**form.data)
        db.session.add(equipment)
        db.session.commit()

        # 构建返回字段
        response_data["equipment_id"] = equipment.id
        response_data["equipment_name"] = equipment.name
        response_data["msg"] = "添加成功"
    else:
        response_data.update(form.errors)

    return jsonify(response_data)


@equipment_bp.route("/delete", methods=["POST"])
# @login_required
def delete():
    """删除一个设备，必须要登录，且只有老师才能删除"""
    response_data = {"msg": "删除失败"}
    form = DeleteEquipmentForm()
    if form.validate_on_submit():
        equipment = Equipment.query.get(form.equipment_id.data)
        if equipment:
            db.session.delete(equipment)
            db.session.commit()
            response_data["msg"] = "成功删除设备, 设备名: %s " % equipment.name
        else:
            response_data["msg"] = "输入的设备ID有误，需要删除的设备不存在或已删除"
    else:
        response_data.update(form.errors)

    return jsonify(response_data)


@equipment_bp.route("/edit", methods=["POST"])
# @login_required
def edit():
    """修改设备信息，必须要登录，且只有老师才能修改
    可修改：设备名、型号、种类、说明书、设备剩余情况、设备是否删除
    """

    response_data = {"msg": "修改设备信息失败"}

    form = EditEquipmentForm()
    if form.validate_on_submit():
        equipment = Equipment.query.get(form.equipment_id.data)

        if equipment:
            # 数据库中存在这个设备,就去修改数据
            for key, value in form.data.items():
                if key == "equipment_id" or not value:
                    # 如果是ID字段或者没有值，那就不更新数据。 任何人都不能去预约ID被修改
                    continue

                # 拼接更新语句
                exec("equipment.%s = '%s'" % (key, value))
            # 提交保存到数据库
            db.session.commit()
            # 构建返回数据
            response_data["msg"] = "成功修改设备信息"
            # 将修改后的数据返回
            response_data.update(
                {
                    "id": equipment.id,
                    "name": equipment.name,
                    "location": equipment.location,
                    "kind": equipment.kind,
                    "capacity": equipment.capacity,
                    "image_url": equipment.image_url,
                }
            )

        else:
            response_data["msg"] = "找不到equipment_id对应的设备"
    else:
        response_data.update(form.errors)
    return jsonify(response_data)


@equipment_bp.route("/upload_image", methods=["POST"])
def upload_image():
    """接收并保存小程序端发送的image，并返回image_url"""

    response_data = {"msg": "上传失败"}

    # 检查文件是否在请求中
    if 'image' not in request.files:
        response_data["msg"] = "未找到上传的图片"
        return jsonify(response_data)

    image = request.files['image']

    # 检查文件名和文件类型是否合法
    if image and allowed_file(image.filename):
        # 为了确保安全，使用secure_filename方法对文件名进行处理
        filename = secure_filename(image.filename)
        # 保存文件到指定路径
        save_path = "/home/itstudio/apache-tomcat-10.1.13/webapps/equip_cover/"+filename

        # 创建目录（如果不存在）
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        image.save(save_path)

        base_url = "http://10.140.33.49:28888/equip_cover"
        # 构建返回的image_url
        image_url = f"{base_url}/{filename}"
        response_data["msg"] = "上传成功"
        response_data["image_url"] = image_url

    else:
        response_data["msg"] = "文件格式不支持或文件名非法"

    return jsonify(response_data)


@equipment_bp.route("/upload_inside_image", methods=["POST"])
def upload_inside_image():
    """接收并保存小程序端发送的image，并返回image_url"""

    response_data = {"msg": "上传失败"}

    # 检查文件是否在请求中
    if 'image' not in request.files:
        response_data["msg"] = "未找到上传的图片"
        return jsonify(response_data)

    image = request.files['image']

    # 检查文件名和文件类型是否合法
    if image and allowed_file(image.filename):
        # 为了确保安全，使用secure_filename方法对文件名进行处理
        filename = secure_filename(image.filename)
        # 保存文件到指定路径
        save_path = "/home/itstudio/apache-tomcat-10.1.13/webapps/equip_inside/"+filename

        # 创建目录（如果不存在）
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        image.save(save_path)

        base_url = "http://10.140.33.49:28888/equip_inside"
        # 构建返回的image_url
        image_url = f"{base_url}/{filename}"
        response_data["msg"] = "上传成功"
        response_data["image_url"] = image_url

    else:
        response_data["msg"] = "文件格式不支持或文件名非法"

    return jsonify(response_data)

@equipment_bp.route("/disable", methods=["POST"])
def diable_equipment():
    response_data = {"msg":"禁用失败"}
    form = DeleteEquipmentForm()
    if form.validate_on_submit():
        equipment = Equipment.query.get(form.equipment_id.data)
        if equipment:
            equipment.disable = 1
            db.session.commit()
            response_data = "成功禁用设备，设备名: %s" % equipment.name
        else:
            response_data["msg"] = "输入的设备ID有误，需要禁用的设备不存在或已禁用"
    else:
        response_data.update(form.errors)

    return jsonify(response_data)

@equipment_bp.route("/enable", methods=["POST"])
def enable_equipment():
    response_data = {"msg": "解除禁用失败"}
    form = DeleteEquipmentForm()
    if form.validate_on_submit():
        equipment = Equipment.query.get(form.equipment_id.data)
        if equipment:
            equipment.disable = 0  # 将 disable 设置为 0，表示解除禁用
            db.session.commit()
            response_data = "成功解除禁用设备，设备名：%s" % equipment.name
        else:
            response_data["msg"] = "输入的设备ID有误，需要解除禁用的设备不存在或未被禁用"
    else:
        response_data.update(form.errors)

    return jsonify(response_data)

def allowed_file(filename):
    """检查文件扩展名是否支持"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
