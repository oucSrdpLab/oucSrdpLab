from .models import Equipment
from . import equipment_bp
from flask import jsonify, g
from .forms import add_equipment_form, delete_equipment_form, edit_equipment_form
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
            if equipment.is_delete and not equipment.is_used:
                equipments_list.append(
                    {
                        "id": equipment.id,
                        "name": equipment.name,
                        "model": equipment.model,
                        "kind": equipment.kind,
                        "instructions": equipment.instructions,
                        "is_used": equipment.is_used,
                        "is_delete": equipment.is_delete,
                    }
                )

    if equipments_list:
        response_data["msg"] = "获取成功"
    else:
        response_data["msg"] = "没有设备"

    response_data["data"] = equipments_list

    return response_data


@equipment_bp.route("/add", methods=["POST"])
#@login_required
def add():
    """添加一个设备，必须要登录，且只有老师才能添加"""

    response_data = {"msg": "添加失败"}


    form = add_equipment_form()
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
#@login_required
def delete():
    """删除一个设备，必须要登录，且只有老师才能删除"""

    response_data = {"msg": "删除失败"}

    form = delete_equipment_form()
    if form.validate_on_submit():
        equipment = Equipment.query.get(form.equipment_id.data)
        if equipment and equipment.is_delete:
            db.session.delete(equipment)
            db.session.commit()
            response_data["msg"] = "成功删除设备, 设备名: %s " % equipment.name
        else:
            response_data["msg"] = "输入的设备ID有误，需要删除的设备不存在或已删除"
    else:
        response_data.update(form.errors)

    return jsonify(response_data)


@equipment_bp.route("/edit", methods=["POST"])
#@login_required
def edit():
    """修改设备信息，必须要登录，且只有老师才能修改
    可修改：设备名、型号、种类、说明书、设备剩余情况、设备是否删除
    """

    response_data = {"msg": "修改设备信息失败"}
    if g.user.identification == "student":
        # 先校验身份，只有老师才可以删除设备
        response_data["msg"] = "%s无权修改设备信息" % g.user.identification
        return response_data

    form = edit_equipment_form()
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
                    "model": equipment.model,
                    "kind": equipment.kind,
                    "instructions": equipment.instructions,
                    "is_used": equipment.is_used,
                    "is_delete": equipment.is_delete,
                }
            )

        else:
            response_data["msg"] = "找不到equipment_id对应的设备"
    else:
        response_data.update(form.errors)
    return jsonify(response_data)
