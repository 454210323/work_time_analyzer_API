from typing import List, Dict, Optional, Union, Any
from flask import Blueprint, jsonify, request
from services.user_service import get_user_by_id, authenticate_user

bp_user = Blueprint("user", __name__, url_prefix="/users")


@bp_user.route("/<string:id>", methods=["GET"])
def get_user(id: str):
    users = get_user_by_id(id)
    if not users:
        return jsonify({"error": "User not found"}), 404
    return jsonify([user.json() for user in users]), 200


@bp_user.route("/auth", methods=["POST"])
def auth_user():
    data:Dict = request.json
    user = authenticate_user(data.get("user_id"), data.get("password"))
    if user:
        return jsonify(user.json()), 200
    return jsonify({"error": "User not found or password was worng"}), 404
