from collections import defaultdict
from functools import reduce

data = [
    {
        "date": "2023-06-06",
        "major_category": "新会員制度",
        "sub_category": "管理・その他",
        "sub_sub_category": "無",
        "user_name": "123",
        "work_time": 5.0,
    },
    {
        "date": "2023-06-13",
        "major_category": "新会員制度",
        "sub_category": "調査",
        "sub_sub_category": "無",
        "user_name": "123",
        "work_time": 23.0,
    },
    {
        "date": "2023-06-14",
        "major_category": "新会員制度",
        "sub_category": "調査",
        "sub_sub_category": "無",
        "user_name": "123",
        "work_time": 24.0,
    },
    {
        "date": "2023-06-18",
        "major_category": "保守",
        "sub_category": "AB票",
        "sub_sub_category": "総合テスト",
        "user_name": "123",
        "work_time": 3.8,
    },
    {
        "date": "2023-06-18",
        "major_category": "保守",
        "sub_category": "情報交換票",
        "sub_sub_category": "AB票-2",
        "user_name": "123",
        "work_time": 5.0,
    },
    {
        "date": "2023-06-19",
        "major_category": "保守",
        "sub_category": "情報交換票",
        "sub_sub_category": "AB票-3",
        "user_name": "123",
        "work_time": 4.0,
    },
    {
        "date": "2023-06-20",
        "major_category": "保守",
        "sub_category": "AB票",
        "sub_sub_category": "総合テスト",
        "user_name": "123",
        "work_time": 6.0,
    },
    {
        "date": "2023-06-21",
        "major_category": "新会員制度",
        "sub_category": "情報交換票",
        "sub_sub_category": "AB票-1",
        "user_name": "123",
        "work_time": 4.0,
    },
    {
        "date": "2023-06-21",
        "major_category": "保守",
        "sub_category": "情報交換票",
        "sub_sub_category": "AB票-3",
        "user_name": "あああ",
        "work_time": 33.0,
    },
    {
        "date": "2023-06-21",
        "major_category": "新会員制度",
        "sub_category": "製造・単体",
        "sub_sub_category": "無",
        "user_name": "asd",
        "work_time": 2.0,
    },
    {
        "date": "2023-06-21",
        "major_category": "保守",
        "sub_category": "AB票",
        "sub_sub_category": "管理・その他",
        "user_name": "123",
        "work_time": 6.0,
    },
]

results = defaultdict(str)

for item in data:
    key = (item["major_category"], item["sub_category"], item["user_name"])
    # results[key] += f"{item['work_time']} {item['sub_sub_category'] if item['sub_sub_category'] !='無' else ''}"
    sub_sub_category = item["sub_sub_category"]
    n = "\n"
    value = (
        f"{item['work_time']} {sub_sub_category+n if sub_sub_category != '無' else ''}"
    )
    results[key] += value


results_list = [
    {
        "major_category": k[0],
        "sub_category": k[1],
        "user_name": k[2],
        "work_time": reduce(lambda a, b: float(a) + float(b), v.strip().split(" "))
        if "\n" not in v
        else v,
    }
    for k, v in results.items()
]

print(results)

dict1 = {
    ("新会員制度", "管理・その他", "123"): "5.0 ",
    ("新会員制度", "調査", "123"): "23.0 24.0 ",
    ("保守", "AB票", "123"): "3.8 総合テスト\n6.0 総合テスト\n6.0 管理・その他\n",
    ("保守", "情報交換票", "123"): "5.0 AB票-2\n4.0 AB票-3\n",
    ("新会員制度", "情報交換票", "123"): "4.0 AB票-1\n",
    ("保守", "情報交換票", "あああ"): "33.0 AB票-3\n",
    ("新会員制度", "製造・単体", "asd"): "2.0 ",
}
