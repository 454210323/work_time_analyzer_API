from typing import List, Dict, Optional, Union, Any
from flask import Blueprint, jsonify, request
from models.dto.user import User
from services.team_service import get_team_member_info

bp_team = Blueprint("team", __name__, url_prefix="/team")


@bp_team.route("/member")
def get_team_member():
    data = request.args.to_dict()
    users = get_team_member_info(**data)
    return users
