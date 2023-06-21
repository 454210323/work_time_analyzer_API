from typing import List, Dict, Optional, Union, Any
from models.dto.user import User
from models.dto.team import Team
from werkzeug.security import check_password_hash,generate_password_hash


def get_user_infos(**kwargs) -> List[User]:
    users: List[User] = User.get_user_by_conditions(**kwargs)
    if users:
        return [
            {k: v for k, v in user.json().items() if k != "password"} for user in users
        ]
    return {"error": "User not found"}


def authenticate_user(id: str, password: str) -> Optional[User]:
    users: List[User] = User.get_user_by_conditions(id=id)
    if users and check_password_hash(users[0].password, password):
        user: User = users[0]
        teams: List[Team] = Team.get_team_by_conditions(team_id=user.team_id)
        if teams:
            team = teams[0]
            return {**user.json(), **team.json()}
        return user.json()
    else:
        return {"error": "User not found or password was worng"}

def register_user(data:Dict):
        user=User(
            id=data.get("id"),
            name=data.get("name"),
            password=generate_password_hash(data.get("password")),
            team_id=data.get("team_id")
        )
        user.add_user()
        return "add successfully"