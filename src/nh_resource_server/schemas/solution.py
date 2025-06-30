from enum import Enum
from typing import Any
from pydantic import BaseModel

class ObjectEnum(str, Enum):
    dem = 'dem'
    sluice_gate = 'sluice_gate'
    tide = 'tide'

class ActionEnum(str, Enum):
    increase = 'increase'  # 增加
    decrease = 'decrease'  # 减少

class HumanAction(BaseModel):
    object: ObjectEnum  # 行为客体，枚举值
    action: ActionEnum  # 行为谓词，枚举值（增加/减少）
    value: float  # 修改值
    feature: dict[str, Any]  # 修改空间范围，GeoJSON