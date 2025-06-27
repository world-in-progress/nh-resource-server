import logging
import socket
from fastapi import APIRouter, Body, HTTPException, Query
from ...schemas.base import BaseResponse
from ...schemas.proxy import DiscoverBody, DiscoverResponse, RelayBody, RelayResponse
from ...core.bootstrapping_treeger import BT
from ...core.config import settings
from pathlib import Path

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/proxy', tags=['proxy'])

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
        address = f'tcp://{ip}:{port}/api/proxy/relay?node_key={node_key}'
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to set patch as the current resource: {str(e)}')
    return DiscoverResponse(
        success=True,
        message=f'Node {node_key} activated successfully',
        address=address
    )

#  
    
