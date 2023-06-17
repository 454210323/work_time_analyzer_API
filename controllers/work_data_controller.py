from flask import Blueprint, jsonify, request
from datetime import datetime

bp_work_data = Blueprint("work_data", __name__, url_prefix="/work_data")


@bp_work_data.route('/month/<string:date_str>', methods=["GET"])
def get_work_data_by_month(date_str):
    # date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return jsonify([
        {
            "date": "2023-06-10",
            "data": "Already completed"
        },
        {
            "date": "2023-06-11",
            "data": "Already completed"
        }
    ])


@bp_work_data.route('', methods=["POST"])
def modify_work_data():
    data = request.json
    print(data)
    if data:
        return 'OK', 200
    else:
        return "fail", 404
