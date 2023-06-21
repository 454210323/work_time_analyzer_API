import logging
from datetime import datetime
from typing import Dict, List

import pandas as pd
from sqlalchemy import and_, extract, func
from sqlalchemy.orm import aliased

from database import db
from models.dto.team import Team
from models.dto.user import User
from models.dto.work_category import WorkCategory
from models.dto.work_data import WorkData


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

def get_work_data_by_month_and_team_excel(data: Dict):
    work_data=get_work_data_by_month_and_team(data)
    data_list = []
    for item in work_data:
        date = item['date']
        for data in item['data']:
            data_list.append({
                'date': date,
                'user_name': data['user_name'],
                'major_category': data['major_category']['category_name'],
                'sub_category': data['sub_category']['category_name'],
                'sub_sub_category': data['sub_sub_category']['category_name'],
                'work_time': data['work_time']
            })

    return data_list
    # # ?建 DataFrame
    # df = pd.DataFrame(data_list)

    # # 根据 major_category、user_name 和 sub_category ?建多?索引
    # df.set_index(['major_category', 'user_name', 'sub_category'], inplace=True)

    # # 根据索引? work_time ?行聚合
    # # 使用 lambda 函数?理相同 major_category 和 sub_category 的情况
    # df['work_time'] = df.groupby(level=df.index.names)['work_time'].transform(lambda x: ', '.join(f'{i[0]}+{i[1]}' for i in zip(df.loc[x.index, 'sub_sub_category'], x)))

    # # ?除重?的行
    # df = df.loc[~df.index.duplicated(keep='first')]

    # df.to_excel("output.xlsx",sheet_name="123")
