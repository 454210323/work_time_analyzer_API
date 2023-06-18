from flask import Blueprint, jsonify, request
from services.work_data_service import (
    add_work_data,
    modify_work_data,
    get_work_data_by_month,
    get_work_data_by_day,
)

bp_work_data = Blueprint("work_data", __name__, url_prefix="/work_data")


@bp_work_data.route("/month/<string:date_str>", methods=["GET"])
def get_month_work_data(date_str):
    # date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    # return jsonify(
    #     [
    #         {
    #             "date": "2023-06-10",
    #             "data": [
    #                 {"seq": 1,
    #                  "type": "success",
    #                  'major_category': {
    #                     "id": "1",
    #                     "category_name": "category_1"
    #                  },
    #                  'sub_category': {
    #                      "id": "5",
    #                      "category_name": "category_1_5"
    #                  },
    #                  'sub_sub_category': {
    #                      "id": "1",
    #                      "category_name": "category_1_5_9"
    #                  },
    #                  'work_time': 2,
    #                  "work_content": "success"},
    #                 {"seq": 2,
    #                  "type": "warning",
    #                  'major_category': {
    #                      "id": "1",
    #                      "category_name": "category_1"
    #                  },
    #                  'sub_category': {
    #                      "id": "5",
    #                      "category_name": "category_1_5"
    #                  },
    #                  'sub_sub_category': {
    #                      "id": "9",
    #                      "category_name": "category_1_5_9"
    #                  },
    #                  'work_time': 3,
    #                  "work_content": "warning"},
    #                 {"seq": 3,
    #                  "type": "error",
    #                  'major_category': {
    #                      "id": "1",
    #                      "category_name": "category_1"
    #                  },
    #                  'sub_category': {
    #                      "id": "5",
    #                      "category_name": "category_1_5"
    #                  },
    #                  'sub_sub_category': {
    #                      "id": "9",
    #                      "category_name": "category_1_5_9"
    #                  },
    #                  'work_time': 2,
    #                  "work_content": "error"},
    #             ],
    #         },
    #         {
    #             "date": "2023-06-11",
    #             "data": [
    #                 {"seq": 1,
    #                  "type": "success",
    #                  'major_category': {
    #                     "id": "1",
    #                     "category_name": "category_1"
    #                  },
    #                  'sub_category': {
    #                      "id": "5",
    #                      "category_name": "category_1_5"
    #                  },
    #                  'sub_sub_category': {
    #                      "id": "9",
    #                      "category_name": "category_1_5_9"
    #                  },
    #                  'work_time': 2,
    #                  "work_content": "success"},
    #             ],
    #         },
    #     ]
    # )
    data = get_work_data_by_month(date_str)
    return jsonify(data), 200


@bp_work_data.route("/day/<string:date_str>")
def get_day_work_data(date_str):
    data = get_work_data_by_day(date_str)
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
