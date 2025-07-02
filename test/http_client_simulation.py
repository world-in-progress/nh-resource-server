import os
import sys
import logging
import c_two as cc
import multiprocessing as mp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from icrms.isimulation import ISimulation, HumanAction, ActionType, AddFenceParams, TransferWaterParams, LanduseType,AddGateParams, GridResult

ADDRESS = 'http://localhost:9000/api/proxy/relay?node_key=root.simulations.test-simulation'

if __name__ == '__main__':
    
    with cc.compo.runtime.connect_crm(ADDRESS, ISimulation) as simulation:
        
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
        # result1 = simulation.add_human_action(1, action1)
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
        # result2 = simulation.add_human_action(1, action2)
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
        # result3 = simulation.add_human_action(1, action3)
        # logger.info(result3)

        # action4 = HumanAction(
        #     action_type=ActionType.TRANSFER_WATER,
        #     params=TransferWaterParams(
        #         from_grid=1,
        #         to_grid=2,
        #         q=1.0
        #     )
        # )
        # result4 = simulation.add_human_action(1, action4)
        # logger.info(result4)

        # action5 = HumanAction(
        #     action_type=ActionType.TRANSFER_WATER,
        #     params=TransferWaterParams(
        #         from_grid=1,
        #         to_grid=2,
        #         q=1.0
        #     )
        # )
        # result5 = simulation.add_human_action(2, action5)
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
        # result6 = simulation.add_human_action(3, action6)
        # logger.info(result6)

        # logger.info('--------------------------------')

        # actions = simulation.get_human_actions(3)
        # logger.info(actions)

        result = simulation.send_result(
            1, 
            [
                [1, 1.0, 3.2, 1.0, 1.0],
                [2, 2.0, 2.0, 2.0, 2.0]
            ],
            [1, 2, 3]
        )
        logger.info(result)