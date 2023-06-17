from typing import List, Dict, Optional, Union, Any
from database import db


class WorkCategory(db.Model):
    __tablename__ = "work_category"

    id = db.Column(db.Integer, primary_key=True)
    category_parent_id = db.Column(db.String(2))
    category_name = db.Column(db.String(100))

    def add_category(self) -> None:
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_categories():
        return WorkCategory.query.all()

    @staticmethod
    def get_category_by_conditions(fields=None, **kwargs):
        if fields is None:
            fields = [WorkCategory.id, WorkCategory.category_name,
                      WorkCategory.category_parent_id]
        return WorkCategory.query(*fields).filter_by(**kwargs).all()

    @staticmethod
    def update_category(_id: int, _category_parent_id: str, _category_name: str) -> None:
        category_to_update = WorkCategory.query.filter_by(id=_id).first()
        category_to_update.category_parent_id = _category_parent_id
        category_to_update.category_name = _category_name
        db.session.commit()

    @staticmethod
    def delete_category(_id: int) -> None:
        WorkCategory.query.filter_by(id=_id).delete()
        db.session.commit()

    def json(self) -> Dict[str, Union[int, str]]:
        return {"id": self.id, "category_parent_id": self.category_parent_id, "category_name": self.category_name}
