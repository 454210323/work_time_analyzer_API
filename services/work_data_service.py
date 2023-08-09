import logging
from datetime import datetime
from typing import Dict, List
from collections import defaultdict
from functools import reduce
from pathlib import Path
import re

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


def get_max_seq(user_id, work_date):
    max_seq = (
        db.session.query(func.max(WorkData.seq))
        .filter_by(user_id=user_id, work_date=work_date)
        .scalar()
        or 0
    )
    return max_seq


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

    max_seq = get_max_seq(user_id, work_date)

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
    pivot_work_df.fillna(0, inplace=True)
    pivot_work_df['TOTAL']=pivot_work_df.sum(axis=1)

    file_name = f"{current_app.config['GENERATED_FOLDER']}/{selected_date}.xlsx"

    file_path = Path(file_name)
    if file_path.exists():
        file_path.unlink()

    # Save to Excel
    pivot_work_df.to_excel(file_name)
    return file_name


def parse_upload_file(file):
    file_name = file.filename

    user_id = get_user_id_from_file_name(file_name)

    work_time_df = pd.read_excel(file, usecols="A:F", skiprows=1).fillna("")
    work_time_df.columns = [
        "date",
        "major_category",
        "sub_category",
        "work_content",
        "work_time_1",
        "work_time_2",
    ]
    work_time_df["date"] = work_time_df["date"].apply(decimal_to_time)
    work_time_df["work_time_1"] = work_time_df["work_time_1"].apply(time_to_decimal)
    work_time_df["work_time_2"] = work_time_df["work_time_2"].apply(time_to_decimal)

    work_time_df["work_time"] = (
        work_time_df["work_time_1"] + work_time_df["work_time_2"]
    )

    category_dict = {
        category.category_name: category.id
        for category in WorkCategory.get_all_categories()
    }

    work_time_df.replace(category_dict, inplace=True)

    for index, row in work_time_df.iterrows():
        max_seq = get_max_seq(user_id, row["date"])
        work_data = WorkData(
            user_id=user_id,
            work_date=row["date"],
            seq=max_seq + 1,
            major_category_id=row["major_category"],
            sub_category_id=row["sub_category"],
            sub_sub_category_id="",
            work_time=row["work_time"],
            work_content=row["work_content"],
        )
        db.session.add(work_data)
    db.session.commit()


def get_user_id_from_file_name(file_name):
    pattern_str = r"[0-9]{6}_(.*)\.xlsx"
    pattern = re.compile(pattern_str)
    _user_name = pattern.findall(file_name)[0]
    result: List[User] = User.get_user_by_conditions(name=_user_name)
    if not len(result) == 1:
        raise Exception("multi user name or user not exist")
    return result[0].id


def time_to_decimal(time: datetime):
    if time == "":
        return 0

    hours = time.hour
    minutes = time.minute
    seconds = time.second

    # hours, minutes, seconds = map(int, time.split(":"))

    total_hours = hours + minutes / 60 + seconds / 3600

    return round(total_hours, 2)


def decimal_to_time(time: int):
    base_date = pd.Timestamp("1899-12-30")
    date = base_date + pd.Timedelta(days=time)
    return date
