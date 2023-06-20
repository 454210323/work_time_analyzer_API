from typing import List, Dict, Optional, Union
from database import db
from flask import jsonify


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(1000))
    team_id = db.Column(db.String(2))

    def add_user(self) -> None:
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_conditions(**kwargs):
        return User.query.filter_by(**kwargs).all()

    @staticmethod
    def update_user(_id: str, _name: str, _password: str) -> None:
        user_to_update = User.query.filter_by(id=_id).first()
        user_to_update.name = _name
        user_to_update.password = _password
        db.session.commit()

    @staticmethod
    def delete_user(_id: str) -> None:
        User.query.filter_by(id=_id).delete()
        db.session.commit()

    def json(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "team_id": self.team_id,
        }
