from models.dto.work_data import WorkData
from models.dto.work_category import WorkCategory
from datetime import datetime
from sqlalchemy import func, extract, and_
from database import db
import logging
from typing import List, Dict

from sqlalchemy.orm import aliased


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
    # try:
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
    return "insert successfully"
    # except Exception as e:
    #     logging.exception(e)
    #     return str(e)


def get_work_data_by_month(date_str):
    work_date = datetime.strptime(date_str, "%Y-%m").date()
    return query_work_data(
        and_(
            extract("year", WorkData.work_date) == work_date.year,
            extract("month", WorkData.work_date) == work_date.month,
        )
    )


def get_work_data_by_day(date_str):
    work_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    return query_work_data(WorkData.work_date == work_date)


def query_work_data(filter_condition) -> List[Dict]:
    # 创建别名以进行多次联接
    MajorCategory = aliased(WorkCategory)
    SubCategory = aliased(WorkCategory)
    SubSubCategory = aliased(WorkCategory)

    # 加载WorkData并联接WorkCategory
    work_data = (
        db.session.query(
            WorkData,
            MajorCategory.category_name.label("major_category_name"),
            SubCategory.category_name.label("sub_category_name"),
            SubSubCategory.category_name.label("sub_sub_category_name"),
        )
        .outerjoin(MajorCategory, WorkData.major_category_id == MajorCategory.id)
        .outerjoin(SubCategory, WorkData.sub_category_id == SubCategory.id)
        .outerjoin(SubSubCategory, WorkData.sub_sub_category_id == SubSubCategory.id)
        .filter(
            filter_condition,
        )
        .order_by(WorkData.work_date, WorkData.seq)
        .all()
    )

    # 初始化结果列表
    result = []

    # 初始化变量用于存储当前日期的数据
    current_date_data = None
    current_date = None

    for (
        data,
        major_category_name,
        sub_category_name,
        sub_sub_category_name,
    ) in work_data:
        if data.work_date != current_date:
            # 一个新的日期开始，将前一天的数据添加到结果中
            if current_date_data is not None:
                result.append(current_date_data)

            # 开始新的日期
            current_date = data.work_date
            current_date_data = {"date": current_date.isoformat(), "data": []}

        # 添加当前数据
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
            }
        )

    # 添加最后一天的数据
    if current_date_data is not None:
        result.append(current_date_data)

    return result
