import os
import c_two as cc
from pathlib import Path
from icrms.isolution import ISolution,NeData,NsData,RainfallData,SluiceGateData,TideData
import logging
logger = logging.getLogger(__name__)

@cc.iicrm
class Solution(ISolution):
    def __init__(self,path: Path,ne_path: Path,ns_path: Path,rainfall_path: Path, or_sluice_gate: list,tide_path: Path):
        self.path = path
        self.or_ne = ne_path
        self.or_ns = ns_path
        self.rainfall_path = rainfall_path
        self.or_sluice_gate = or_sluice_gate
        self.tide_path = tide_path
            
    def get_imp(self) -> str:
        with open(self.path / '.imp', 'r', encoding='utf-8') as f:
            data = f.read()
        return data
    
    def get_ne(self) -> NeData:
        grid_id_list = []
        nsl1_list = []
        nsl2_list = []
        nsl3_list = []
        nsl4_list = []
        isl1_list = []
        isl2_list = []
        isl3_list = []
        isl4_list = []
        xe_list = []
        ye_list = []
        ze_list = []
        under_suf_list = []
        with open(self.or_ne, 'r', encoding='utf-8') as f:
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
                break       
        ne_data = NeData(grid_id_list,nsl1_list,nsl2_list,nsl3_list,nsl4_list,isl1_list,isl2_list,isl3_list,isl4_list,xe_list,ye_list,ze_list,under_suf_list)
        return ne_data
    
    def get_ns(self) -> NsData:
        edge_id = []
        ise = []
        dis = []
        x_side = []
        y_side = []
        z_side = []
        under_suf = []
        nbd_ie = []
        ibd_ie = []
        with open(self.or_ns,'r',encoding='utf-8') as f:
            for rowdata in f:
                rowdata = rowdata.strip().split(",")
                edge_id.append(int(float(rowdata[0].strip())))
                ise.append(int(float(rowdata[1].strip())))
                dis.append(float(rowdata[2].strip()))
                x_side.append(float(rowdata[3].strip()))
                y_side.append(float(rowdata[4].strip()))
                z_side.append(float(rowdata[5].strip()))
                under_suf.append(float(rowdata[6].strip()))
                nbd_ie.append(int(float(rowdata[7].strip())))
                ibd_ie.append(int(float(rowdata[8].strip())))
                break
        ns_data = NsData(
            edge_id,
            ise,
            dis,
            x_side,
            y_side,
            z_side,
            under_suf,
            nbd_ie,
            ibd_ie
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
                break
        rainfall = RainfallData(
            rainfall_date_list,
            rainfall_station_list,
            rainfall_value_list
        )
        return rainfall
    
    def get_sluice_gate(self) -> SluiceGateData:
        sluice_gate = SluiceGateData(
            grid_id = self.or_sluice_gate[0],
            closed_height = self.or_sluice_gate[1],
            runtime_height = self.or_sluice_gate[2],
            is_active = True,
        )
        return sluice_gate
    
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
                break
        tide = TideData(
            tide_date_list,
            tide_time_list,
            tide_value_list
        )
        return tide
 
    def terminate(self) -> None:
        # Do something need to be saved
        pass
    
    
