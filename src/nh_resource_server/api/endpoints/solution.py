from ast import Delete
from fastapi import APIRouter
from icrms.isolution import ISolution
from ...schemas.base import BaseResponse
from ...core.bootstrapping_treeger import BT
from fastapi import APIRouter, HTTPException, Body
from ...schemas.solution import CreateSolutionBody, ActionType, ActionTypeResponse, AddHumanActionBody, DeleteHumanActionBody

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/solution', tags=['solution / operation'])    

@router.get('/action_type_list', response_model=ActionTypeResponse)
def get_action_type_list():
    """
    Description
    --
    Get all action types with complete information.
    """
    try:
        action_types = [
            {
                "value": action_type.action_value,
                "name": action_type.display_name,
                "description": action_type.description
            }
            for action_type in ActionType
        ]
        return ActionTypeResponse(
            success=True,
            data=action_types
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to get action types: {str(e)}')

@router.post('/create', response_model=BaseResponse)
def create_solution(body: CreateSolutionBody=Body(..., description='create solution')):
    """
    Description
    --
    Create a solution.
    """
    try:
        node_key = f'root.solutions.{body.name}'
        BT.instance.mount_node("solution", node_key, body.model_dump())
        BT.instance.mount_node("actions", f'{node_key}.actions')
        BT.instance.mount_node("human_actions", f'{node_key}.actions.human_actions')
        return BaseResponse(
            success=True,
            message=node_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to set patch as the current resource: {str(e)}')
    
@router.post('/add_human_action', response_model=BaseResponse)
def add_human_action(body: AddHumanActionBody=Body(..., description='add human action')):
    """
    Description
    --
    Add a human action.
    """
    try:
        node_key = f'root.solutions.{body.solution_name}'
        with BT.instance.connect(node_key, ISolution) as solution:
            action_id = solution.add_human_action(body.action_type, body.params)
        BT.instance.mount_node("human_action", f'{node_key}.actions.human_actions.{action_id}')
        return BaseResponse(
            success=True,
            message="Action added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to add human action: {str(e)}')
    
@router.delete('/delete_human_action', response_model=BaseResponse)
def delete_human_action(body: DeleteHumanActionBody=Body(..., description='delete human action')):
    """
    Description
    --
    Delete a human action.
    """
    try:
        node_key = f'root.solutions.{body.solution_name}'
        with BT.instance.connect(node_key, ISolution) as solution:
            solution.delete_human_action(body.action_id)
        BT.instance.unmount_node(f'{node_key}.actions.human_actions.{body.action_id}')
        return BaseResponse(
            success=True,
            message="Action deleted successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to delete human action: {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to add human action: {str(e)}')