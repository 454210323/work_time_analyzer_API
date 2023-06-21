from typing import List, Dict, Optional, Union, Any
from flask import Blueprint, jsonify, request
# from services.user_service import get_user_infos, authenticate_user
from services import user_service

bp_user = Blueprint("user", __name__, url_prefix="/users")


@bp_user.route("/<string:id>", methods=["GET"])
def get_users(id: str):
    users = user_service.get_user_infos(id=id)
    return jsonify(users), 200


@bp_user.route("/auth", methods=["POST"])
def auth_user():
    data: Dict = request.json
    user = user_service.authenticate_user(data.get("user_id"), data.get("password"))
    return jsonify(user), 200

@bp_user.route("",methods=["POST"])
def register_user():
    data:Dict=request.json
    result=user_service.register_user(data)
    return jsonify(result),200