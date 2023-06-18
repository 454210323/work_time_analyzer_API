from flask import Blueprint, jsonify, request
from services.work_category_service import get_category

bp_category = Blueprint("category", __name__, url_prefix="/category")


@bp_category.route("", methods=["GET"])
def get_category_info():
    category_id = request.args.get("parent_category_id")
    categories = get_category(category_id)
    return jsonify(categories), 200
