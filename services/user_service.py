from typing import List, Dict, Optional, Union, Any
from models.dto.user import User
from werkzeug.security import check_password_hash


def get_user_by_id(id: str) -> List[User]:
    users: List[User] = User.get_user_by_conditions(id=id)
    return users


def authenticate_user(id: str, password: str) -> Optional[User]:
    users = User.get_user_by_conditions(id=id)
    print(users[0].password)
    print(password)
    if users and check_password_hash(users[0].password, password):
        return users[0]
    else:
        return None
