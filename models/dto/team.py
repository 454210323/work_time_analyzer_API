from typing import List, Dict, Optional, Union, Any
from database import db


class Team(db.Model):
    __tablename__ = "team"

    team_id = db.Column(db.String(2), primary_key=True)
    team_name = db.Column(db.String(100))
    team_manager_id = db.Column(db.String(100))

    def add_team(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_teams():
        return Team.query.all()

    @staticmethod
    def get_team_by_conditions(**kwargs):
        return Team.query.filter_by(**kwargs).all()

    @staticmethod
    def update_team(_team_id: str, _team_name: str, _team_manager_id: str) -> None:
        team_to_update = Team.query.filter_by(team_id=_team_id).first()
        team_to_update.team_parent_id = _team_name
        team_to_update.team_manager_id = _team_manager_id
        db.session.commit()

    @staticmethod
    def delete_team(_team_id):
        Team.query.filter_by(team_id=_team_id).delete()
        db.session.commit()

    def json(self) -> Dict[str, Union[int, str]]:
        return {
            "team_id": self.team_id,
            "team_name": self.team_name,
            "team_manager_id": self.team_manager_id,
        }
