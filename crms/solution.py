import os
import json
from datetime import datetime
import c_two as cc
from pathlib import Path
from icrms.isolution import ISolution,NeData,NsData,RainfallData,TideData,Gate
import logging
from src.nh_resource_server.core.config import settings
logger = logging.getLogger(__name__)

@cc.iicrm
class Solution(ISolution):
    def __init__(self, solution_name: str, ne_path: str, ns_path: str, inp_path: str, rainfall_path: str, gate_path: str, tide_path: str):
        self.name = solution_name
        self.path = Path(f'{settings.SOLUTION_DIR}{self.name}')
        self.ne_path = ne_path
        self.ns_path = ns_path
        self.inp_path = inp_path
        self.rainfall_path = rainfall_path
        self.gate_path = gate_path
        self.tide_path = tide_path

        # Create solution directory
        self.path.mkdir(parents=True, exist_ok=True)
        # # Create ref json file
        # ref_path = self.path / 'ref.json'
        # with open(ref_path, 'w', encoding='utf-8') as f:
        #     json.dump(body.model_dump(), f, ensure_ascii=False, indent=4)

    def get_inp(self) -> str:
        with open(self.inp_path, 'r', encoding='utf-8') as f:
            data = f.read()
        return data
    
    def get_ne(self) -> NeData:
        grid_id_list = [0]
        nsl1_list = [0]
        nsl2_list = [0]
        nsl3_list = [0]
        nsl4_list = [0]
        isl1_list = [[0,0,0,0,0,0,0,0,0,0]]
        isl2_list = [[0,0,0,0,0,0,0,0,0,0]]
        isl3_list = [[0,0,0,0,0,0,0,0,0,0]]
        isl4_list = [[0,0,0,0,0,0,0,0,0,0]]
        xe_list = [0.0]
        ye_list = [0.0]
        ze_list = [0.0]
        under_suf_list = [0]
        with open(self.ne_path, 'r', encoding='utf-8') as f:
            for row_data in f:
                row_data = row_data.split(',')
                # 创建NeData对象
                grid_id_list.append(int(row_data[0]))
                nsl1 = int(row_data[1])
                nsl2 = int(row_data[2])
                nsl3 = int(row_data[3])
                nsl4 = int(row_data[4])
                nsl1_list.append(nsl1)
                nsl2_list.append(nsl2)
                nsl3_list.append(nsl3)
                nsl4_list.append(nsl4)
                isl1 = [0 for _ in range(nsl1)]
                isl2 = [0 for _ in range(nsl2)]
                isl3 = [0 for _ in range(nsl3)]
                isl4 = [0 for _ in range(nsl4)]
                for i in range(nsl1): 
                    isl1[i] = int(row_data[5+i]) 
                for i in range(nsl2): 
                    isl2[i] = int(row_data[5+nsl1+i])
                for i in range(nsl3): 
                    isl3[i] = int(row_data[5+nsl1+nsl2+i])
                for i in range(nsl4): 
                    isl4[i] = int(row_data[5+nsl1+nsl2+nsl3+i])
                isl1_list.append(isl1)
                isl2_list.append(isl2)
                isl3_list.append(isl3)
                isl4_list.append(isl4)
                xe_list.append(float(row_data[-4]))
                ye_list.append(float(row_data[-3]))
                ze_list.append(float(row_data[-2]))
                under_suf_list.append(int(row_data[-1]))       
        ne_data = NeData(grid_id_list,nsl1_list,nsl2_list,nsl3_list,nsl4_list,isl1_list,isl2_list,isl3_list,isl4_list,xe_list,ye_list,ze_list,under_suf_list)
        return ne_data
    
    def get_ns(self) -> NsData:
        edge_id_list = [0]
        ise_list = [[0,0,0,0,0]]
        dis_list = [0.0]
        x_side_list = [0.0]
        y_side_list = [0.0]
        z_side_list = [0.0]
        s_type_list = [0]
        with open(self.ns_path,'r',encoding='utf-8') as f:
            for rowdata in f:
                ise_row = []
                rowdata = rowdata.strip().split(",")
                edge_id_list.append(int(float(rowdata[0].strip())))
                ise_row = [
                    int(rowdata[1].strip()),
                    int(rowdata[2].strip()),
                    int(rowdata[3].strip()),
                    int(rowdata[4].strip()),
                    int(rowdata[5].strip())
                ]
                ise_list.append(ise_row)
                dis_list.append(float(rowdata[6].strip()))
                x_side_list.append(float(rowdata[7].strip()))
                y_side_list.append(float(rowdata[8].strip()))
                z_side_list.append(float(rowdata[9].strip()))
                s_type_list.append(float(rowdata[10].strip()))
        ns_data = NsData(
            edge_id_list,
            ise_list,
            dis_list,
            x_side_list,
            y_side_list,
            z_side_list,
            s_type_list
        )
        return ns_data
    
    def get_rainfall(self) -> RainfallData:
        rainfall_date_list = []
        rainfall_station_list = []
        rainfall_value_list = []
        with open(self.rainfall_path,'r',encoding='utf-8') as f:
            # 跳过第一行
            next(f)
            for row_data in f:
                row_data = row_data.split(',')
                rainfall_date_list.append(row_data[0])
                rainfall_station_list.append(row_data[1])
                rainfall_value_list.append(float(row_data[2]))
        rainfall = RainfallData(
            rainfall_date_list,
            rainfall_station_list,
            rainfall_value_list
        )
        return rainfall
    
    def get_gate(self) -> Gate:
        ud_stream_list = []
        gate_height_list = []
        grid_id_list = []
        with open(self.gate_path,'r',encoding='utf-8') as f:
            for row_data in f:
                row_data = row_data.strip().split(',')
                ud_stream_list.append(int(row_data[0]))
                ud_stream_list.append(int(row_data[1]))
                gate_height_list.append(int(row_data[2]))
                grid_id_row = []
                for value in row_data[3:]:
                    grid_id_row.append(int(value))
                grid_id_list.append(grid_id_row)
        gate = Gate(
            ud_stream_list=ud_stream_list,
            gate_height_list=gate_height_list,
            grid_id_list=grid_id_list
        )
        return gate
    
    def get_tide(self) -> TideData:
        tide_date_list = []
        tide_time_list = []
        tide_value_list = []
        with open(self.tide_path,'r',encoding='utf-8') as f:
            # 跳过第一行
            next(f)
            for row_data in f:
                row_data = row_data.split(',')
                tide_date_list.append(row_data[0])
                tide_time_list.append(row_data[1])
                tide_value_list.append(float(row_data[2]))
        tide = TideData(
            tide_date_list,
            tide_time_list,
            tide_value_list
        )
        return tide
 
    def get_solution_data(self)-> dict:
        solution_data = {}
        solution_data['ne_data'] = self.get_ne()
        solution_data['ns_data'] = self.get_ns()
        solution_data['inp_data'] = self.get_inp()
        solution_data['rainfall_data'] = self.get_rainfall()
        solution_data['gate_data'] = self.get_gate()
        solution_data['tides_data'] = self.get_tide()
        return solution_data
 
    def terminate(self) -> None:
        # Do something need to be saved
        pass