from enum import Enum
from typing import Any
from pydantic import BaseModel

class ObjectEnum(int, Enum):
    dem = 0 
    sluice_gate = 1
    tide = 2

class ActionEnum(int, Enum):
    increase = 0
    decrease = 1

class HumanAction(BaseModel):
    object: ObjectEnum
    action: ActionEnum
    value: float
    feature: dict[str, Any]

class Gate(BaseModel):
    gate_id_list: list[int]
    gate_num_list: list[int]
    grid_id_list: list[int]
    ud_stream_list:list[int]
    gate_height_list:list[int]


    