from typing import List, Dict, Optional, Union, Any
from models.dto.user import User
from models.dto.team import Team
from services import user_service


def get_team_member_info(**kwargs):
    users = user_service.get_user_infos(**kwargs)
    return users

def get_all_teams():
    teams:List[Team]=Team.get_all_teams()
    return [{k:v for k,v in team.json().items() if k != "team_manager_id"} for team in teams]