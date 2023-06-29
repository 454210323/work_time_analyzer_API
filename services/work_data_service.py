import logging
from datetime import datetime
from typing import Dict, List
from collections import defaultdict
from functools import reduce
from pathlib import Path

import pandas as pd
from sqlalchemy import and_, extract, func
from sqlalchemy.orm import aliased

from database import db
from models.dto.team import Team
from models.dto.user import User
from models.dto.work_category import WorkCategory
from models.dto.work_data import WorkData
from services import work_category_service

from flask import current_app


def parse_json(work_data):
    user_id = work_data.get("user_id")
    work_date = datetime.strptime(work_data.get("work_date"), "%Y-%m-%d")
    seq = work_data.get("seq")
    major_category_id = work_data.get("major_category_id")
    sub_category_id = work_data.get("sub_category_id")
    sub_sub_category_id = work_data.get("sub_sub_category_id")
    work_time = work_data.get("work_time")
    work_content = work_data.get("work_content")
    return (
        user_id,
        work_date,
        seq,
        major_category_id,
        sub_category_id,
        sub_sub_category_id,
        work_time,
        work_content,
    )


def modify_work_data(work_data):
    try:
        (
            user_id,
            work_date,
            seq,
            major_category_id,
            sub_category_id,
            sub_sub_category_id,
            work_time,
            work_content,
        ) = parse_json(work_data)
        WorkData.update_work_data(
            user_id,
            work_date,
            seq,
            major_category_id,
            sub_category_id,
            sub_sub_category_id,
            work_time,
            work_content,
        )
    except Exception as e:
        logging.exception(e)
        return str(e)


def add_work_data(work_data):
    (
        user_id,
        work_date,
        seq,
        major_category_id,
        sub_category_id,
        sub_sub_category_id,
        work_time,
        work_content,
    ) = parse_json(work_data)

    max_seq = (
        db.session.query(func.max(WorkData.seq))
        .filter_by(user_id=user_id, work_date=work_date)
        .scalar()
        or 0
    )

    new_work_data = WorkData(
        user_id=user_id,
        work_date=work_date,
        seq=max_seq + 1,
        major_category_id=major_category_id,
        sub_category_id=sub_category_id,
        sub_sub_category_id=sub_sub_category_id,
        work_time=work_time,
        work_content=work_content,
    )
    new_work_data.add_work_data()
    return "add successfully"


def get_work_data_by_month_and_user(user_id, date_str):
    work_date = datetime.strptime(date_str, "%Y-%m").date()

    def modify_query(query):
        return query.filter(
            and_(
                WorkData.user_id == user_id,
                extract("year", WorkData.work_date) == work_date.year,
                extract("month", WorkData.work_date) == work_date.month,
            )
        )

    return query_work_data(modify_query)


def get_work_data_by_month_and_team(data: Dict):
    work_date = datetime.strptime(data.get("date"), "%Y-%m").date()
    team_id = data.get("team_id")

    def modify_query(query):
        return query.filter(
            and_(
                User.team_id == team_id,
                extract("year", WorkData.work_date) == work_date.year,
                extract("month", WorkData.work_date) == work_date.month,
            )
        )

    return query_work_data(modify_query)


def get_work_data_by_day_and_user(user_id, date_str):
    work_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    def modify_query(query):
        return query.filter(
            and_(WorkData.user_id == user_id, WorkData.work_date == work_date)
        )

    return query_work_data(modify_query)


def query_work_data(modify_query) -> List[Dict]:
    MajorCategory = aliased(WorkCategory)
    SubCategory = aliased(WorkCategory)
    SubSubCategory = aliased(WorkCategory)

    query = (
        db.session.query(
            WorkData,
            User.name.label("user_name"),
            MajorCategory.category_name.label("major_category_name"),
            SubCategory.category_name.label("sub_category_name"),
            SubSubCategory.category_name.label("sub_sub_category_name"),
        )
        .outerjoin(User, WorkData.user_id == User.id)
        .outerjoin(MajorCategory, WorkData.major_category_id == MajorCategory.id)
        .outerjoin(SubCategory, WorkData.sub_category_id == SubCategory.id)
        .outerjoin(SubSubCategory, WorkData.sub_sub_category_id == SubSubCategory.id)
        .order_by(WorkData.work_date, WorkData.seq)
    )

    work_data = modify_query(query).all()

    result = []
    current_date_data = None
    current_date = None

    for (
        data,
        user_name,
        major_category_name,
        sub_category_name,
        sub_sub_category_name,
    ) in work_data:
        if data.work_date != current_date:
            if current_date_data is not None:
                result.append(current_date_data)

            current_date = data.work_date
            current_date_data = {"date": current_date.isoformat(), "data": []}

        current_date_data["data"].append(
            {
                "seq": data.seq,
                "type": "success",
                "major_category": {
                    "id": data.major_category_id,
                    "category_name": major_category_name,
                },
                "sub_category": {
                    "id": data.sub_category_id,
                    "category_name": sub_category_name,
                },
                "sub_sub_category": {
                    "id": data.sub_sub_category_id,
                    "category_name": sub_sub_category_name,
                },
                "work_time": float(data.work_time) if data.work_time else None,
                "work_content": data.work_content,
                "user_name": user_name,
            }
        )

    if current_date_data is not None:
        result.append(current_date_data)

    return result


def generate_work_data_excel(data: Dict):
    selected_date = data.get("date")
    work_data = get_work_data_by_month_and_team(data)

    pivot_work_df = pd.DataFrame()

    major_sub_categories = {}
    parent_categories = work_category_service.get_category("")

    for parent_category in parent_categories:
        parent_category_id = parent_category.get("id")
        parent_category_name = parent_category.get("category_name")
        sub_categories = work_category_service.get_category(parent_category_id)

        # extract sub-category names and store them as a list associated with the parent category
        major_sub_categories[parent_category_name] = [
            category.get("category_name") for category in sub_categories
        ]

    # major_sub_categories = {
    #     '保守': ['AB票', '情報交換票', '管理・その他', '障害票'],
    #     '新会員制度': ['基本設計', '移行・リリース', '管理・その他', '結合テスト', '総合テスト', '製造・単体', '詳細設計', '調査']
    # }
    multi_index_columns = pd.MultiIndex.from_tuples(
        [(major, sub) for major, subs in major_sub_categories.items() for sub in subs]
    )
    if work_data:
        flattened_data_list = []
        for item in work_data:
            date = item["date"]
            for work_item in item["data"]:
                flattened_data_list.append(
                    {
                        "date": date,
                        "user_name": work_item["user_name"],
                        "major_category": work_item["major_category"]["category_name"],
                        "sub_category": work_item["sub_category"]["category_name"],
                        "sub_sub_category": work_item["sub_sub_category"][
                            "category_name"
                        ],
                        "work_time": work_item["work_time"],
                    }
                )
        work_df = pd.DataFrame(flattened_data_list)

        grouped_work_df = (
            work_df.groupby(["user_name", "major_category", "sub_category"])[
                "work_time"
            ]
            .sum()
            .reset_index()
        )

        pivot_work_df = grouped_work_df.pivot_table(
            values="work_time",
            index="user_name",
            columns=["major_category", "sub_category"],
        )

    pivot_work_df = pivot_work_df.reindex(multi_index_columns, axis=1)
    pivot_work_df.fillna("", inplace=True)

    file_name = f"{current_app.config['GENERATED_FOLDER']}/{selected_date}.xlsx"

    file_path = Path(file_name)
    if file_path.exists():
        file_path.unlink()

    # Save to Excel
    pivot_work_df.to_excel(file_name)
    return file_name


def parse_upload_file(file):
    work_time_df = pd.read_excel(file, usecols="A:D,G", skiprows=1)
    work_time_df.columns = [
        "date",
        "major_category",
        "sub_category",
        "work_content",
        "work_time",
    ]

    category_dict = {
        category.category_name: category.id
        for category in WorkCategory.get_all_categories()
    }

    work_time_df.replace(category_dict)
    print(category_dict)
    print(work_time_df)
