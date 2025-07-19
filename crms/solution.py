import os
import time
import json
import c_two as cc
from pathlib import Path
from icrms.isolution import ISolution
from src.nh_resource_server.core.config import settings
import logging
logger = logging.getLogger(__name__)

@cc.iicrm
class Solution(ISolution):
    def __init__(self, name: str, env: dict, action_types: list[str]):
        self.name = name
        self.env = env
        self.action_types = action_types
        self.path = Path(f'{settings.SOLUTION_DIR}{self.name}')
        self.actions_path = self.path / 'actions' / 'human_actions'

        self.path.mkdir(parents=True, exist_ok=True)
        self.actions_path.mkdir(parents=True, exist_ok=True)

    def clone_env(self) -> dict:
        env_data = {}
        for key, value in self.env.items():
            if isinstance(value, str) and os.path.isfile(value):
                try:
                    with open(value, 'r', encoding='utf-8') as f:
                        content = f.readlines()
                except UnicodeDecodeError:
                    with open(value, 'rb') as f:
                        content = f.read()
                env_data[key] = {
                    'file_name': os.path.basename(value),
                    'content': content
                }
            else:
                env_data[key] = value
        return env_data
    
    def get_env(self) -> dict:
        return self.env

    def get_action_types(self) -> list[str]:
        return self.action_types
    
    def add_human_action(self, action_type: str, params: dict) -> str:
        action_id = str(int(time.time() * 1000))
        action_path = self.actions_path / f'{action_id}.json'
        
        # 获取params数据并去掉action_type字段
        params_data = params.model_dump()
        params_data.pop('action_type', None)  # 安全地移除action_type字段
            
        with open(action_path, 'w', encoding='utf-8') as f:
            json.dump({
                'action_type': action_type,
                'params': params_data
            }, f, ensure_ascii=False, indent=4)
        return action_id

    def update_human_action(self, action_id, params):
        action_path = self.actions_path / f'{action_id}.json'
        if not action_path.exists():
            raise FileNotFoundError(f'Action file {action_path} does not exist.')
        
        # 获取params数据并去掉action_type字段
        params_data = params.model_dump()
        params_data.pop('action_type', None)  # 安全地移除action_type字段
        
        with open(action_path, 'w', encoding='utf-8') as f:
            json.dump({
                'action_type': params.action_type,
                'params': params_data
            }, f, ensure_ascii=False, indent=4)

    def delete_human_action(self, action_id):
        action_path = self.actions_path / f'{action_id}.json'
        if action_path.exists():
            action_path.unlink()
        else:
            logger.warning(f'Action file {action_path} does not exist.')
    
    def get_human_actions(self) -> list[dict]:
        actions = []
        try:
            # 检查actions目录是否存在
            if not self.actions_path.exists():
                logger.warning(f'Actions path {self.actions_path} does not exist')
                return actions
            
            # 遍历actions目录下的所有JSON文件
            for action_file in self.actions_path.glob('*.json'):
                try:
                    with open(action_file, 'r', encoding='utf-8') as f:
                        action_data = json.load(f)
                        # 添加action_id（从文件名提取）
                        action_id = action_file.stem  # 去掉.json后缀
                        action_data['action_id'] = action_id
                        actions.append(action_data)
                except (json.JSONDecodeError, IOError) as e:
                    logger.error(f'Failed to read action file {action_file}: {str(e)}')
                    continue
            
            # 按action_id排序（时间戳顺序）
            actions.sort(key=lambda x: x.get('action_id', '0'))
            
        except Exception as e:
            logger.error(f'Failed to get human actions: {str(e)}')
        
        return actions

    def terminate(self) -> None:
        # Do something need to be saved
        pass