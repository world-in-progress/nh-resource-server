from fastapi import APIRouter
import c_two as cc
from ...core.config import settings
from fastapi import APIRouter, Response, HTTPException, Body
import logging
from ...core.bootstrapping_treeger import BT
from ...schemas.project import ResourceCRMStatus
from ...schemas.base import BaseResponse
from ...schemas.simulation import FileData, ResultResponse
from pathlib import Path
from icrms.isimulation import ISimulation, CreateSimulationBody
import base64

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/simulation', tags=['simulation / operation'])
   
@router.get('/{simulation_name}', response_model=ResourceCRMStatus)
def check_simulation_ready(simulation_name: str):
    """
    Description
    --
    Check if the simulation runtime resource is ready.
    """
    try:
        node_key = f'root.simulations.{simulation_name}'
        tcp_address = BT.instance.get_node_info(node_key).server_address
        flag = cc.rpc.Client.ping(tcp_address)

        return ResourceCRMStatus(
            status='ACTIVATED' if flag else 'DEACTIVATED',
            is_ready=flag
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to check CRM of the simulation: {str(e)}')
    
   
@router.post('/create', response_model=BaseResponse)
def create_simulation(body: CreateSimulationBody=Body(..., description='create simulation')):
    """
    Description
    --
    Create a simulation.
    """
    try:
        node_key = f'root.simulations.{body.solution_name}_{body.name}'
        BT.instance.mount_node("simulation", node_key, body.model_dump())
        return BaseResponse(
            success=True,
            message=node_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to set patch as the current resource: {str(e)}')
    
@router.get('/result/{simulation_name}/{step}', response_model=ResultResponse)
def get_result(simulation_name: str, step: str):
    """
    Description
    --
    Get simulation result files for a specific step.
    Checks if .done file exists and returns all files in the step folder.
    """
    try:
        # 构建资源路径
        simulation_base = Path(settings.SIMULATION_DIR)
        step_folder = simulation_base / simulation_name / 'result' / step
        
        # 检查文件夹是否存在
        if not step_folder.exists():
            return ResultResponse(
                success=False,
                message=f'Step folder not found: {step_folder}',
                is_ready=False
            )
        
        # 检查是否有 .done 文件
        done_files = list(step_folder.glob('*.done'))
        if not done_files:
            return ResultResponse(
                success=True,
                message='Result not ready yet',
                is_ready=False
            )
        
        files_data = {}
        for file_path in step_folder.iterdir():
            if file_path.is_file() and not file_path.name.endswith('.done'):
                try:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            f.read(1024)  # 尝试读取前1024字符
                        is_binary = False
                    except UnicodeDecodeError:
                        is_binary = True
                    
                    # 读取文件内容
                    if is_binary:
                        with open(file_path, 'rb') as f:
                            content = base64.b64encode(f.read()).decode('utf-8')
                    else:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    
                    files_data[file_path.name] = FileData(
                        filename=file_path.name,
                        content=content,
                        is_binary=is_binary,
                        size=file_path.stat().st_size
                    )
                    
                except Exception as file_error:
                    logger.warning(f'Failed to read file {file_path}: {str(file_error)}')
                    continue
        
        return ResultResponse(
            success=True,
            message=f'Found {len(files_data)} files in step {step}',
            is_ready=True,
            files=files_data
        )
        
    except Exception as e:
        logger.error(f'Failed to get simulation result: {str(e)}')
        raise HTTPException(status_code=500, detail=f'Failed to get simulation result: {str(e)}')