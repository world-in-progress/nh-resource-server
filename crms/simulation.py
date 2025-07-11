import c_two as cc
from icrms.isimulation import FenceParams, GateParams, ISimulation, HumanAction, GridResult,ActionType
from src.nh_resource_server.core.config import settings
import json
from datetime import datetime
from pathlib import Path
from typing import Any

@cc.iicrm
class Simulation(ISimulation):

    def __init__(self, simulation_name: str, solution_name: str):
        self.name = simulation_name
        self.solution_name = solution_name
        self.path = Path(f'{settings.SIMULATION_DIR}{self.name}')
        self.human_action_path = self.path / 'human_action'
        self.result_path = self.path / 'result'
        self.solution_path = Path(f'{settings.SOLUTION_DIR}{self.solution_name}')

        # Create simulation directory
        self.path.mkdir(parents=True, exist_ok=True)
        self.human_action_path.mkdir(parents=True, exist_ok=True)
        self.result_path.mkdir(parents=True, exist_ok=True)
        
    def get_human_actions(self, step: int) -> list[HumanAction]:
        step_path = self.human_action_path / str(step)
        action_files = step_path.glob('*.json')
        actions = []

        # 按时间排序，基于文件名中的时间戳
        action_files = sorted(action_files, key=lambda x: datetime.strptime(x.stem.split('_')[-1], "%Y-%m-%d-%H-%M-%S-%f"))
        
        for action_file in action_files:
            with open(action_file, 'r', encoding='utf-8') as f:
                action = HumanAction.model_validate_json(f.read())
                actions.append(action)
        
        return actions

    def send_result(self, step: int, result_data: dict[str, Any], file_types: list[str], file_suffix: dict[str, str]) -> dict[str, bool | str]:
        try:
            step_path = self.result_path / str(step)
            step_path.mkdir(parents=True, exist_ok=True)
            
            for file_type in file_types:
                if file_type in result_data:
                    data = result_data[file_type]
                    suffix = file_suffix.get(file_type, '')
                    filename = f'{file_type}{suffix}'
                    file_path = step_path / filename
                    
                    # 处理二进制数据
                    if isinstance(data, bytes):
                        with open(file_path, 'wb') as f:
                            f.write(data)
                    # 处理非二进制数据（按行写入）
                    else:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            if isinstance(data, list):
                                # 如果是列表，逐行写入
                                for line in data:
                                    f.write(str(line) + '\n')
                            else:
                                # 如果是其他类型，转换为字符串后写入
                                f.write(str(data))

            done_file_path = step_path / f'{step}.done'
            with open(done_file_path, 'w', encoding='utf-8') as f:
                f.write('done')

            return {'success': True, 'message': 'success'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
    # Front to Resource Server
    def add_human_action(self, step: int, action: HumanAction) -> dict[str, bool | str]:
        try:
            step_path = self.human_action_path / str(step)
            step_path.mkdir(parents=True, exist_ok=True)

            # 使用毫秒级别的时间戳生成唯一时间标识
            time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
            action_path = step_path / f'action_{time}.json'

            if(action.action_type == ActionType.ADD_FENCE | ActionType.ADD_GATE):
                feature = action.params.feature
                # TODO: 获取 feature 的所有 grid_id
                grid_id_list = []
                if(action.action_type == ActionType.ADD_FENCE):
                    params = FenceParams(action.params.elevation_delta, action.params.landuse_type, grid_id_list)
                else:
                    params = GateParams(action.params.ud_stream, action.params.gate_height, grid_id_list)
                action.params = params
            with open(action_path, 'w', encoding='utf-8') as f:
                json.dump(action.model_dump(), f, ensure_ascii=False, indent=4)

            return {'success': True, 'message': 'success'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        