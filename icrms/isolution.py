import c_two as cc
from dataclasses import dataclass
from typing import Any
from src.nh_resource_server.schemas.solution import HumanAction

@dataclass
class NeData:
    grid_id_list: list[int]
    nsl1_list:list[int]
    nsl2_list:list[int]
    nsl3_list:list[int]
    nsl4_list:list[int]
    isl1_list:list[list[int]]
    isl2_list:list[list[int]]
    isl3_list:list[list[int]]
    isl4_list:list[list[int]]
    xe_list:list[float]
    ye_list:list[float]
    ze_list:list[float]
    under_suf_list:list[int]

@dataclass
class NsData:
    edge_id_list: list[int]
    ise_list: list[int]
    dis_list: list[float]
    x_side_list: list[float]
    y_side_list: list[float]
    z_side_list: list[float]
    under_suf_list: list[int]
    nbd_ie_list: list[int]
    ibd_ie_list: list[int]

@dataclass
class RainfallData:
    rainfall_date_list:list[str]
    rainfall_station_list:list[str]
    rainfall_value_list:list[float]

@dataclass
class SluiceGateData:
    grid_id: int                    # 网格号
    closed_height: float            # 关闭时的高度（4/5m）
    runtime_height: float = 0.0     # 运行时高度（变成0）
    is_active: bool = True

@dataclass
class TideData:
    tide_date_list:list[str]          
    tide_time_list:list[str]           
    tide_value_list:list[float]

@cc.icrm
class ISolution:


    # Model Server to Resource Server
    def get_imp(self)-> str:
        """
        获取模型参数
        :return: str
        """
        ...
        
    
    def get_ne(self)-> NeData:
        """
        获取网格数据
        :return: NeData对象列表
        """
        ...
    
    def get_ns(self)-> NsData:
        """
        获取边数据
        :return: NsData对象
        """
        ...
    
    def get_rainfall(self)-> RainfallData:
        """
        获取降雨数据
        :return: RainfallData对象
        """
        ...
    
    def get_sluice_gate(self)-> SluiceGateData:
        """
        获取闸门数据
        :return: SluiceGateData对象
        """
        ...
    
    def get_tide(self)-> TideData:
        """
        获取潮位数据
        :return: TideData对象
        """
        ...

    def get_human_actions(self, step: int) -> list[HumanAction]:
        """
        获取人类行为
        :param step: 步骤
        :return: HumanAction对象列表
        """
        ...

    # ------------------------------------------------------------
    # Front to Resource Server
    def add_human_action(self, step: int, action: HumanAction) -> str:
        """
        添加人类行为
        :param action: HumanAction对象
        """
        ...