import c_two as cc
from icrms.isimulation import ISimulation, HumanAction, GridResult
from src.nh_resource_server.core.config import settings
import json
from datetime import datetime
from pathlib import Path

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

    def send_result(self, step: int, result: list[GridResult], highlight_grids: list[int], hsf: bytes) -> dict[str, bool | str]:
        try:
            step_path = self.result_path / str(step)
            step_path.mkdir(parents=True, exist_ok=True)
            result_path = step_path / 'result.json'
            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            if highlight_grids:
                highlight_path = step_path / 'highlight_grids.json'
                with open(highlight_path, 'w', encoding='utf-8') as f:
                    json.dump(highlight_grids, f, ensure_ascii=False, indent=4)
            if hsf:
                hsf_path = step_path / 'hsf.hsf'
                with open(hsf_path, 'wb') as f:
                    f.write(hsf)
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

            # 存储时直接使用 datetime 对象
            with open(action_path, 'w', encoding='utf-8') as f:
                json.dump(action.model_dump(), f, ensure_ascii=False, indent=4)

            return {'success': True, 'message': 'success'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        