import os
import sys
import logging
import c_two as cc
import multiprocessing as mp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from icrms.isolution import ISolution
# from icrms.isolution import HumanAction, ActionType, AddFenceParams, TransferWaterParams, LanduseType,AddGateParams, GridResult

ADDRESS = 'http://localhost:9000/api/proxy/relay?node_key=root.solutions.test-solution'

if __name__ == '__main__':
    
    with cc.compo.runtime.connect_crm(ADDRESS, ISolution) as solution:
        # inp = solution.get_inp()
        # with open('test.inp', 'w', encoding='utf-8') as f:
        #     f.write(inp)
        # logger.info(inp)
        # logger.info('--------------------------------')
        # ne = solution.get_ne()
        # with open('ne.txt', 'w', encoding='utf-8') as f:
        #     for i in range(len(ne.grid_id_list)):
        #         f.write(f'{ne.grid_id_list[i]},{ne.nsl1_list[i]},{ne.nsl2_list[i]},{ne.nsl3_list[i]},{ne.nsl4_list[i]},')
        #         for j in range(len(ne.isl1_list[i])):
        #             f.write(f'{ne.isl1_list[i][j]},')
        #         for j in range(len(ne.isl2_list[i])):
        #             f.write(f'{ne.isl2_list[i][j]},')
        #         for j in range(len(ne.isl3_list[i])):
        #             f.write(f'{ne.isl3_list[i][j]},')
        #         for j in range(len(ne.isl4_list[i])):
        #             f.write(f'{ne.isl4_list[i][j]},')
        #         f.write(f'{ne.xe_list[i]},{ne.ye_list[i]},{ne.ze_list[i]},{ne.under_suf_list[i]}\n')
        # logger.info(ne)
        # logger.info('--------------------------------')
        # ns = solution.get_ns()
        # with open('ns.txt', 'w', encoding='utf-8') as f:
        #     for i in range(len(ns.edge_id)):
        #         f.write(f'{ns.edge_id[i]},{ns.ise[i]},{ns.dis[i]},{ns.x_side[i]},{ns.y_side[i]},{ns.z_side[i]},{ns.under_suf[i]},{ns.nbd_ie[i]},{ns.ibd_ie[i]}\n')
        
        # rainfall = solution.get_rainfall()
        # with open('rainfall.txt', 'w', encoding='utf-8') as f:
        #     for i in range(len(rainfall.rainfall_date_list)):
        #         f.write(f'{rainfall.rainfall_date_list[i]},{rainfall.rainfall_station_list[i]},{rainfall.rainfall_value_list[i]}\n')
        
        # gate = solution.get_gate()
        # logger.info(gate)

        # tide = solution.get_tide()

        # with open('tide.txt', 'w', encoding='utf-8') as f:
        #     for i in range(len(tide.tide_date_list)):
        #         f.write(f'{tide.tide_date_list[i]},{tide.tide_time_list[i]},{tide.tide_value_list[i]}\n')
        
        # action1 = HumanAction(
        #     action_type=ActionType.ADD_FENCE,
        #     params=AddFenceParams(
        #         elevation_delta=1.0,
        #         landuse_type=LanduseType.FENCE,
        #         feature={
        #             'type': 'Feature',
        #             'geometry': {
        #                 'type': 'Point',
        #                 'coordinates': [120.123456, 30.123456]
        #             }
        #         }
        #     )
        # )
        # result1 = solution.add_human_action(1, action1)
        # logger.info(result1)

        # action2 = HumanAction(
        #     action_type=ActionType.ADD_FENCE,
        #     params=AddFenceParams(
        #         landuse_type=LanduseType.FENCE,
        #         feature={
        #             'type': 'Feature',
        #             'geometry': {
        #                 'type': 'Point',
        #                 'coordinates': [120.123456, 30.123456]
        #             }
        #         }
        #     )
        # )
        # result2 = solution.add_human_action(1, action2)
        # logger.info(result2)

        # action3 = HumanAction(
        #     action_type=ActionType.ADD_FENCE,
        #     params=AddFenceParams(
        #         elevation_delta=5.0,
        #         feature={
        #             'type': 'Feature',
        #             'geometry': {
        #                 'type': 'Point',
        #                 'coordinates': [120.123456, 30.123456]
        #             }
        #         }
        #     )
        # )
        # result3 = solution.add_human_action(1, action3)
        # logger.info(result3)

        # action4 = HumanAction(
        #     action_type=ActionType.TRANSFER_WATER,
        #     params=TransferWaterParams(
        #         from_grid=1,
        #         to_grid=2,
        #         q=1.0
        #     )
        # )
        # result4 = solution.add_human_action(1, action4)
        # logger.info(result4)

        # action5 = HumanAction(
        #     action_type=ActionType.TRANSFER_WATER,
        #     params=TransferWaterParams(
        #         from_grid=1,
        #         to_grid=2,
        #         q=1.0
        #     )
        # )
        # result5 = solution.add_human_action(2, action5)
        # logger.info(result5)
        
        # action6 = HumanAction(
        #     action_type=ActionType.ADD_GATE,
        #     params=AddGateParams(
        #         gate_num=3,
        #         grid_id_list=[1,2,3], 
        #         ud_stream=1,
        #         gate_height=1
        #     )
        # )
        # result6 = solution.add_human_action(3, action6)
        # logger.info(result6)

        # logger.info('--------------------------------')

        # actions = solution.get_human_actions(3)
        # logger.info(actions)

        # result = solution.send_result(
        #     1, 
        #     [
        #         [1, 1.0, 3.2, 1.0, 1.0],
        #         [2, 2.0, 2.0, 2.0, 2.0]
        #     ],
        #     [1, 2, 3]
        # )
        # logger.info(result)

        solution_data = solution.get_solution_data()
        logger.info(solution_data)