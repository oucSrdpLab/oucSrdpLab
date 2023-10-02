from .models import Award

from flask import g, jsonify, request, url_for, redirect
from .forms import commit_award_form, get_award_form, edit_award_form

from web.my_utils import login_required

from web.apps.exts import db
from . import collect_bp


@collect_bp.route("/all_award", methods=["get"])
#@login_required
def all_award():
    """获取用户所有的奖项名称、获得日期、获奖人信息、颁奖机构、获奖等级"""
    response_data = {"msg": "获取成功", "data": []}
    award_list = g.user.awards
    # print(award_list)
    for item in award_list:
        _temp_dict = {}
        _temp_dict["name"] = item.name
        _temp_dict["date"] = (item.date.strftime("%Y-%m-%d"),)
        _temp_dict["level"] = item.level
        _temp_dict["institution"] = item.institution

        _temp_dict["users"] = []
        for user in item.users:
            _temp_dict["users"].append(user.id)

        response_data["data"].append(_temp_dict)

    return response_data


@collect_bp.route("/commit", methods=["POST"])
#@login_required
def commit():
    """提交获奖信息"""
    response_data = {"msg": "提交获奖信息"}
    form = commit_award_form()
    if form.validate_on_submit():
        # 校验合法，创建获奖
        award = Award(
            name=form.name.data,
            date=form.date.data,
            institution=form.institution.data,
            level=form.level.data,
        )
        for user in form._my_exists_user:
            award.users.append(user)
        # 别忘了把award也要提交到数据库
        db.session.add(award)
        db.session.commit()

    else:
        # 返回错误字段信息
        response_data.update(form.errors)

    return jsonify(response_data)
