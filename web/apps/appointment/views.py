from .models import Appointment
from ..equipment.models import Equipment
from . import appointment_bp
from flask import g, jsonify, request, url_for, redirect
from .forms import (
    add_appointment_form,
    get_appointment_form,
    edit_appointment_form,
    allow_appointment_form
)

from web.my_utils import login_required

from web.apps.exts import db


@appointment_bp.route("/all", methods=["POST"])
#@login_required
def all():
    """根据时间获取用户所有的预约ID、开始时间、结束时间、是否签到、预约人信息"""
    response_data = {"msg": "请选择提供预约的起止时间", "data": []}

    form = get_appointment_form()

    # GET方式提交的数据，不要用validate_on_submit，用validate
    # `POST', `PUT', `PATCH', 或 `DELETE'，才可以用validate_on_submit
    if form.validate_on_submit():
        # filter内传的是表达式,逗号分隔,默认为and,
        appointment_list = (
            db.session.query(Appointment)
            .filter(
                Appointment.is_delete == False,
                # 查询的开始时间小于预约的开始时间, 这里要注意前面是.data，后面不能加.data。这个bug我找了接近一个小时
                form.start_time.data <= Appointment.end_time,
                # 查询的结束时间大于预约的结束时间
                form.end_time.data >= Appointment.end_time,
            )
            .all()
        )

        if appointment_list:
            # 在数据库查到了预约，才提取数据
            for item in appointment_list:
                response_data["data"].append(
                    {
                        "id": item.id,
                        "start_time": item.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "end_time": item.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "equipment_id": item.equipment_id,
                        "equipment_name": item.equipment.name,
                        "is_sign": item.is_sign,
                        "is_sign_out": item.is_sign_out,
                        "user_id": item.user_id,
                    }
                )
        if response_data["data"]:
            response_data["msg"] = "获取预约数据成功"
        else:
            response_data["msg"] = "该时间段没有预约"

    else:
        response_data.update(form.errors)

    return response_data


@appointment_bp.route("/add", methods=["POST"])
#@login_required
def add():
    """创建预约,必须要给出起止时间、用户要先登录
    TODO 查时间校验算法，同一个设备的预约起止时间不能重叠
    """
    response_data = {"msg": "预约失败"}
    form = add_appointment_form()
    if form.validate_on_submit():
        # 校验合法，创建预约
        validate_data = form.data


        appointment = Appointment(**validate_data)
        db.session.add(appointment)
        db.session.commit()
        response_data["msg"] = "预约成功"
        response_data["appointment_id"] = appointment.id

    else:
        # 返回错误字段信息
        response_data.update(form.errors)

    return jsonify(response_data)



@appointment_bp.route("/delete", methods=["POST"])
#@login_required
def delete():
    """删除预约,必须要先登录"""
    response_data = {"msg": "删除失败"}
    # 获取预约id
    appointment_id = request.json.get('appointment_id')
    if appointment_id:
        appointment = Appointment.query.get(appointment_id)
        if appointment:
            # 直接从数据库中删除
            db.session.delete(appointment)
            # 保存到数据库
            db.session.commit()
            response_data["msg"] = "删除成功"
        else:
            response_data["msg"] = "找不到对应的预约"
    else:
        response_data["msg"] = "删除失败，缺少预约id"

    return jsonify(response_data)




@appointment_bp.route("/edit", methods=["POST"])
#@login_required
def edit():
    """编辑预约,必须要先登录，学生只能修改自己，老师可以修改任何人的预约"""
    """可编辑的数据有: start_time、end_time、equipment_id"""

    response_data = {"msg": "修改失败"}
    # 验证提交的数据
    form = edit_appointment_form()
    if form.validate_on_submit():
        appointment = Appointment.query.get(form.appointment_id.data)
        if appointment:
            # 数据库中存在这个预约,就去校验这个预约是不是自己，或者当前登录的用户是老师
            if appointment.user == g.user or g.user == "teacher":

                for key, value in form.data.items():
                    if key == "appointment_id" or not value:
                        # 如果是ID字段或者没有值，那就不更新数据。
                        continue
                    # 拼接更新语句
                    excc_str = "appointment.%s = '%s'" % (key, value)
                    exec(excc_str)
                # 提交保存到数据库
                db.session.commit()
                # 构建返回数据
                response_data["msg"] = "成功修改预约中值"
                # 将修改后的数据返回
                response_data.update(
                    {
                        "id": appointment.id,
                        "start_time": appointment.start_time.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "end_time": appointment.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "is_sign": appointment.is_sign,
                        "user_id": appointment.user.id,
                        "user_name": appointment.user.username,
                    }
                )
            else:
                response_data["msg"] = "无权编辑这个预约"

        else:
            response_data["msg"] = "找不到appointment_id对应的预约信息"
    else:
        response_data.update(form.errors)
    return jsonify(response_data)


@appointment_bp.route("/serch_by_user", methods=["POST"])
#@login_required
def serch_by_user():
    """查询此user所有的预约，必须要登录"""

    response_data = {"msg": "查询成功", "data": []}
    user_id = request.json.get('user_id')
    all_appointment_list = Appointment.query.filter_by(
        user_id=user_id, is_delete=False
    ).all()

    for item in all_appointment_list:
        response_data["data"].append(
            {
                "appointment_id": item.id,
                "start_time": item.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": item.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "equipment_id": item.equipment_id,
                "equipment_name": item.equipment.name,
                "is_sign": item.is_sign,
                "is_sign_out": item.is_sign_out,
            }
        )


    return jsonify(response_data)




@appointment_bp.route("/serch_by_equipment", methods=["POST"])
def serch_by_equipment():
    """根据设备查询当前已经预约的时间段，无须登录"""
    response_data = {"msg": "查询成功", "data": []}
    equipment_id = int(request.json.get("equipment_id"))
    if equipment_id:
        equipment = Equipment.query.get(equipment_id)
        # 通过equipment.appointments查询出所有关联的预约
        all_appointment_list = equipment.appointments

        for item in all_appointment_list:
            response_data["data"].append(
                {
                    "appointment_id": item.id,
                    "start_time": item.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "end_time": item.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "equipment_id": item.equipment_id,
                    "equipment_name": item.equipment.name,
                    "is_sign": item.is_sign,
                    "is_sign_out": item.is_sign_out,
                }
            )
    else:
        response_data["msg"] = "查询失败，缺少equipment_id"

    return jsonify(response_data)


@appointment_bp.route("/allow", methods=["POST"])
def allow():
    """显示每种设备在当天还可以预约的时间阶段，需要传入起止时间、需要预约的设备ID，无须登录
    算法分为三步，第一步是根据设备获取当天的已经预约时间段
    第二步将所有的时间段从小到大排序
    第三步将两个预约时间段之间的空隙返回
    """
    response_data = {"msg": "查询失败", "data": []}
    # 先验证起止时间是否合理
    form = allow_appointment_form()
    if form.validate_on_submit():
        # 根据设备查询当前已经预约的时间段

        # 通过equipment查询出与此设备关联的预约
        equipment = Equipment.query.get(form.equipment_id.data)
        if equipment:
            all_appointment_list = equipment.appointments
        else:
            response_data["msg"] = "当前equipment_id不存在"
            return jsonify(response_data)
        # 将所有的时间段依照开始时间从小到大排序
        all_appointment_list.sort(key=lambda item: item.start_time)
        # 将两个预约时间段之间的空隙返回
        if all_appointment_list:
            for i in range(len(all_appointment_list)):
                _temp_dic = {}
                if i == 0:
                    # 查询的开始时间-->第一个预约结束时间，这段为空闲时间
                    _temp_dic["start_time"] = form.start_time.data.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    _temp_dic["end_time"] = all_appointment_list[i].start_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    response_data["data"].append(_temp_dic)
                    _temp_dic = {}
                    # 第一个预约结束----->第二个预约开始，这段为空闲时间
                    _temp_dic["start_time"] = all_appointment_list[i].end_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    _temp_dic["end_time"] = all_appointment_list[
                        i + 1
                        ].start_time.strftime("%Y-%m-%d %H:%M:%S")
                elif i == len(all_appointment_list) - 1:
                    # 如果为最后一个预约，那么最后一个预约结束时间----->查询的结束时间，这段为空闲时间
                    _temp_dic["start_time"] = all_appointment_list[i].end_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    _temp_dic["end_time"] = form.end_time.data.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                else:
                    # 其余的是上一个预约的结束时间------>下一个预约开始的时间，这段为空闲时间
                    _temp_dic["start_time"] = all_appointment_list[i].end_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    _temp_dic["end_time"] = all_appointment_list[
                        i + 1
                        ].start_time.strftime("%Y-%m-%d %H:%M:%S")
                response_data["data"].append(_temp_dic)
        else:
            # 如果查询的这台设备在查询时间段里面没有预约，那么查询的开始时间----->查询的结束时间都是空闲时间
            _temp_dic = {}
            _temp_dic["start_time"] = form.start_time.data.strftime("%Y-%m-%d %H:%M:%S")
            _temp_dic["end_time"] = form.end_time.data.start_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            response_data["data"].append(_temp_dic)
        response_data["msg"] = "成功查询出当前设备可预约的时间段"
    else:
        response_data.update(form.errors)
    return jsonify(response_data)
