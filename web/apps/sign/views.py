from datetime import datetime
from flask import jsonify, request

from ..appointment.models import Appointment
from web.my_utils import timeStr_to_dataTime
from . import sign_bp
from web.apps.exts import db


@sign_bp.route("/signature", methods=["POST"])
def signature():
    """学生签到，必须要登录
    学生根据预约信息进行签到，需要appointment_id、需要登陆
    签到最晚时间不能超过预约的结束时间
    """
    response_data = {"msg": "签到失败"}

    appointment_id = request.json.get("appointment_id")
    if appointment_id:
        appointment = Appointment.query.get(int(appointment_id))
        # 限制签到最晚时间不能超过预约的结束时间
        if appointment.end_time >= datetime.now():
            # 还没有到结束时间，进行签到
            appointment.is_sign = True
            db.session.commit()

            response_data["msg"] = "签到成功"
        else:
            response_data["msg"] = "签到失败。你错过了签到时间，联系老师进行补签"
    else:
        response_data["msg"] = "需要提供appointment_id字段"
    return jsonify(response_data)


@sign_bp.route("/supplementary_signature", methods=["POST"])
def supplementary_signature():
    """补签，必须要登录，且只有老师才能补签
    教师帮学生补签，需要appointment_ID、登录身份为teacher才可以补签
    """

    response_data = {"msg": "签到失败"}

    appointment_id = request.json.get("appointment_id")
    identification = request.json.get("identification")
    if appointment_id and identification == "teacher":
        # 有appointment_id字段，且身份是教师
        appointment = Appointment.query.get(int(appointment_id))
        # 进行签到
        appointment.is_sign = True
        # 将预约的设备置为有人使用
        appointment.equipment.is_used = True
        db.session.commit()
        # 返回签到结果
        response_data["msg"] = "补签成功"
    else:
        response_data["msg"] = "签到失败，请检查appointment_id和identification"

    return jsonify(response_data)


@sign_bp.route("/sign_out", methods=["POST"])
def sign_out():
    """签退，需要appointment_ID、必须要登录
    签退应该是在预约结束之后，且已经签到的学生才能够签退,
    签退完成之后，需要对设备进行归还
    """
    response_data = {"msg": "签退失败"}

    appointment_id = request.json.get("appointment_id")
    if appointment_id:
        appointment = Appointment.query.get(int(appointment_id))
        # 这里限制签到最晚时间不能超过预约的结束时间
        if appointment.end_time <= datetime.now():
            if appointment.is_sign:
                # 预约的结束时间到了，且进行了签到，进行签退
                appointment.is_sign_out = True
                # 将预约的设备归还,需要通过预约查预约设备
                appointment.equipment.is_used = False
                db.session.commit()
                response_data["msg"] = "签退成功，预约设备已归还"
            else:
                response_data["msg"] = "签退失败，未签到的用户不能签退，需要找老师进行补签到和补签退"
        else:
            response_data["msg"] = "签退失败，还没有到签退时间"
    else:
        response_data["msg"] = "签退失败，需要提供appointment_id字段"
    return jsonify(response_data)


@sign_bp.route("/supplementary_sign_out", methods=["POST"])
def supplementary_sign_out():
    """补签退，需要appointment_ID、必须要登录才可以操作，且登陆者的身份是teacher
    签退完成之后，需要对设备进行归还
    """
    response_data = {"msg": "签退失败"}

    appointment_id = request.json.get("appointment_id")
    identification = request.json.get("identification")
    if appointment_id and identification == "teacher":
        # 有appointment_id字段，且身份是教师
        appointment = Appointment.query.get(int(appointment_id))
        # 进行签到
        appointment.is_sign = True
        # 进行签退
        appointment.is_sign_out = True
        # 将预约的设备置为无人使用
        appointment.equipment.is_used = False
        db.session.commit()
        # 返回签退结果
        response_data["msg"] = "补签退成功"
    else:
        response_data["msg"] = "签退失败，请检查appointment_id和identification"

    return jsonify(response_data)


@sign_bp.route("/get_sign_status", methods=["GET"])
def get_sign_status():
    """根据日期，获取当天签到情况，无须登录"""
    response_data = {
        "msg": "签退失败",
        "has_sign": [],
        "sign_count": 0,
        "not_sign": [],
        "not_sign_count": 0,
    }
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")
    if start_time and end_time:
        # 前端传入了查找的起止时间
        start_time = timeStr_to_dataTime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = timeStr_to_dataTime(end_time, "%Y-%m-%d %H:%M:%S")
        if start_time and end_time:
            sign_status = Appointment.query.filter(
                # 未删除的签到
                Appointment.is_delete == False,
                # 查询的开始时间小于预约的开始时间,
                start_time <= Appointment.start_time,
                # 查询的结束时间大于预约的结束时间
                end_time >= Appointment.end_time,
            ).all()
            if sign_status:
                # 查到了预约数据，就提取
                for item in sign_status:
                    temp = {
                        "id": item.id,
                        "start_time": item.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "end_time": item.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "equipment_id": item.equipment_id,
                        "equipment_name": item.equipment.name,
                        "is_sign": item.is_sign,
                        "is_sign_out": item.is_sign_out,
                        "user_id": item.user.id,
                        "user_name": item.user.username,
                    }
                    if item.is_sign:
                        response_data["has_sign"].append(temp)
                        response_data["sign_count"] += 1
                    else:
                        response_data["not_sign"].append(temp)
                        response_data["not_sign_count"] += 1

                response_data["msg"] = "成功获取当天的签到情况"
            else:
                response_data["msg"] = "该时间段没有预约数据"
        else:
            response_data["msg"] = "时间格式错误，格式应该为 YYYY-MM-DD HH:MM:SS"

    else:
        response_data["msg"] = "缺少start_time或end_time字段数据"

    return response_data
