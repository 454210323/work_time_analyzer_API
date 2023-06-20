from typing import List, Dict, Optional, Union, Any
from flask import Blueprint, jsonify, request
from services.user_service import get_user_infos, authenticate_user

bp_user = Blueprint("user", __name__, url_prefix="/users")


@bp_user.route("/<string:id>", methods=["GET"])
def get_users(id: str):
    users = get_user_infos(id=id)
    return jsonify(users), 200


@bp_user.route("/auth", methods=["POST"])
def auth_user():
    data: Dict = request.json
    user = authenticate_user(data.get("user_id"), data.get("password"))
    return jsonify(user), 200
