from flask import Blueprint, jsonify, request
from services.work_data_service import (
    add_work_data,
    modify_work_data,
    get_work_data_by_month,
    get_work_data_by_day,
)

bp_work_data = Blueprint("work_data", __name__, url_prefix="/work_data")


@bp_work_data.route("/month/<string:user_id>/<string:date_str>", methods=["GET"])
def get_month_work_data(user_id, date_str):
    data = get_work_data_by_month(user_id, date_str)
    return jsonify(data), 200


@bp_work_data.route("/day/<string:user_id>/<string:date_str>")
def get_day_work_data(user_id, date_str):
    data = get_work_data_by_day(user_id, date_str)
    return jsonify(data), 200


@bp_work_data.route("", methods=["POST"])
def add():
    data = request.json
    result = add_work_data(data)
    return jsonify(result), 200


@bp_work_data.route("", methods=["PUT"])
def modify():
    data = request.json
    result = modify_work_data(data)
    return jsonify(result), 200
