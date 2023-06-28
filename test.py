from collections import defaultdict
from functools import reduce
import pandas as pd
from pathlib import Path

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


# Convert the data to DataFrame
df = pd.DataFrame(data)

print(df)

# Group by 'user_name', 'major_category' and 'sub_category' and sum 'work_time'
df = df.groupby(['user_name', 'major_category', 'sub_category'])['work_time'].sum().reset_index()

print(df)

# Define the specific sub categories for each major category
major_sub_categories = {
    '保守': ['AB票', '情報交換票', '管理・その他', '障害票'],
    '新会員制度': ['基本設計', '移行・リリース', '管理・その他', '結合テスト', '総合テスト', '製造・単体', '詳細設計', '調査']
}

# Create MultiIndex with all possible combinations of major and specific sub categories
columns = pd.MultiIndex.from_tuples([(major, sub) for major, subs in major_sub_categories.items() for sub in subs])

# Pivot table to get the format you want
df_pivot = df.pivot_table(values='work_time', index='user_name', columns=['major_category', 'sub_category'])

print(df_pivot)

# Reindex the columns of the pivot table with the new MultiIndex
df_pivot = df_pivot.reindex(columns, axis=1)

print(df_pivot)

# Replace NaN values with an empty string
df_pivot.fillna("", inplace=True)

file_path=Path('output.xlsx')
if file_path.exists():
    file_path.unlink()

# Save to Excel
df_pivot.to_excel('output.xlsx')