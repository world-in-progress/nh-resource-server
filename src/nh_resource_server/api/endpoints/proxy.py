import logging
import socket
import asyncio
from fastapi import APIRouter, Body, HTTPException, Query
from ...schemas.proxy import DiscoverBody, DiscoverResponse, RelayResponse
from ...core.bootstrapping_treeger import BT
from ...core.config import settings
from ...schemas.project import ResourceCRMStatus
import c_two as cc
from starlette.responses import Response

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/proxy', tags=['proxy'])

@router.get('/', response_model=ResourceCRMStatus)
def check_crm_ready(node_key: str=Query(..., description='node_key')):
    """
    Description
    --
    Check if the crm is ready.
    """
    try:
        address = BT.instance.get_node_info(node_key).server_address
        flag = cc.rpc.Client.ping(address)

        return ResourceCRMStatus(
            status='ACTIVATED' if flag else 'DEACTIVATED',
            is_ready=flag
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to check CRM of the node {node_key}: {str(e)}')
    

@router.post('/discover', response_model=DiscoverResponse)
def discover(body: DiscoverBody=Body(..., description='discover')):
    """
    Description
    --
    Discover the scene node.
    """

    node_key = body.node_key
    try:
        BT.instance.activate_node(node_key)
        # 获取本机IP
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        port = settings.SERVER_PORT
        address = f'http://{ip}:{port}/api/proxy/relay?node_key={node_key}'
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to set patch as the current resource: {str(e)}')
    return DiscoverResponse(
        success=True,
        message=f'Node {node_key} activated successfully',
        address=address
    )

@router.post('/relay', response_model=RelayResponse)
async def relay(node_key: str=Query(..., description='node_key'), body: bytes=Body(..., description='relay')):
    """
    Description
    --
    Relay the message to the node.
    """
    try:
        node_info = BT.instance.get_node_info(node_key)
        if node_info is None:
            raise HTTPException(status_code=404, detail=f'Node {node_key} not found')
        res = asyncio.run(cc.rpc.routing(node_info.server_address, body, 1000))
        return Response(res, media_type='application/octet-stream')
    except Exception as e:
        logger.error(f'Failed to relay message: {str(e)}')
        raise HTTPException(status_code=500, detail=f'Failed to relay message: {str(e)}')

