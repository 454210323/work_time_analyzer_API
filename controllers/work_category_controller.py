from flask import Blueprint, jsonify, request
from services.work_category_service import get_category

bp_category = Blueprint("category", __name__, url_prefix="/category")


@bp_category.route("/<string:category_id>", methods=["GET"])
def get_sub_category(category_id):
    return jsonify(get_category(category_id)), 200
