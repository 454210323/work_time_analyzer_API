from typing import List, Dict, Optional, Union, Any
from models.dto.user import User
from services.user_service import get_user_infos


def get_team_member_info(**kwargs):
    users = get_user_infos(**kwargs)
    return users
