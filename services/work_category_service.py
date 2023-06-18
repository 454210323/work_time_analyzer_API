from typing import List, Dict, Optional, Union, Any
from models.dto.work_category import WorkCategory


def get_category(category_id):
    categories = WorkCategory.get_category_by_conditions(category_parent_id=category_id)
    return [category.json() for category in categories]
