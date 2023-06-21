from typing import List, Dict, Optional, Union, Any
from flask import Blueprint, jsonify, request
from services import team_service

bp_team = Blueprint("team", __name__, url_prefix="/team")


@bp_team.route("/member")
def get_team_member():
    data = request.args.to_dict()
    users = team_service.get_team_member_info(**data)
    return jsonify(users),200

@bp_team.route("")
def get_all_teams():
    teams=team_service.get_all_teams()
    return jsonify(teams),200