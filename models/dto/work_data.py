from datetime import date
from decimal import Decimal
from typing import Dict, Union
from database import db


class WorkData(db.Model):
    __tablename__ = "work_data"

    user_id = db.Column(db.String(100), primary_key=True)
    work_date = db.Column(db.Date, primary_key=True)
    seq = db.Column(db.Integer, primary_key=True)
    major_category_id = db.Column(db.String(2))
    sub_category_id = db.Column(db.String(2))
    sub_sub_category_id = db.Column(db.String(2))
    work_time = db.Column(db.Numeric(4, 2))
    work_content = db.Column(db.String(1000))

    def add_work_data(self) -> None:
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_work_data():
        return WorkData.query.all()

    @staticmethod
    def get_work_data_by_conditions(**kwargs):
        return WorkData.query.filter_by(**kwargs).all()

    @staticmethod
    def update_work_data(
        user_id: str,
        work_date: date,
        seq: int,
        major_category_id: str = None,
        sub_category_id: str = None,
        sub_sub_category_id: str = None,
        work_time: Decimal = None,
        work_content: str = None,
    ) -> None:
        work_data_to_update = WorkData.query.filter_by(
            user_id=user_id, work_date=work_date, seq=seq
        ).first()
        if major_category_id is not None:
            work_data_to_update.major_category_id = major_category_id
        if sub_category_id is not None:
            work_data_to_update.sub_category_id = sub_category_id
        if sub_sub_category_id is not None:
            work_data_to_update.sub_sub_category_id = sub_sub_category_id
        if work_time is not None:
            work_data_to_update.work_time = work_time
        if work_content is not None:
            work_data_to_update.work_content = work_content
        db.session.commit()

    @staticmethod
    def delete_work_data(user_id: str, work_date: date, seq: int) -> None:
        WorkData.query.filter_by(
            user_id=user_id, work_date=work_date, seq=seq).delete()
        db.session.commit()

    def json(self) -> Dict[str, Union[str, date, int, Decimal]]:
        return {
            "user_id": self.user_id,
            "work_date": self.work_date,
            "seq": self.seq,
            "major_category_id": self.major_category_id,
            "sub_category_id": self.sub_category_id,
            "sub_sub_category_id": self.sub_sub_category_id,
            "work_time": self.work_time,
            "work_content": self.work_content,
        }
