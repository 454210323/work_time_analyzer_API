from typing import List, Dict, Optional, Union, Any
from models.dto.work_category import WorkCategory


def get_category(parent_id):
    return WorkCategory.get_category_by_conditions(fields=[WorkCategory.id, WorkCategory.category_name], category_parent_id=parent_id)
