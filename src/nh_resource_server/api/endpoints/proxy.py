import logging
import socket
from fastapi import APIRouter, Body, HTTPException, Query
from ...schemas.proxy import DiscoverBody, DiscoverResponse, RelayResponse
from ...core.bootstrapping_treeger import BT
from ...core.config import settings
import c_two as cc
from starlette.responses import Response

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
        address = f'http://{ip}:{port}/api/proxy/relay?node_key={node_key}'
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to set patch as the current resource: {str(e)}')
    return DiscoverResponse(
        success=True,
        message=f'Node {node_key} activated successfully',
        address=address
    )

@router.post('/relay', response_model=RelayResponse)
def relay(node_key: str=Query(..., description='node_key'), body: bytes=Body(..., description='relay')):
    """
    Description
    --
    Relay the message to the node.
    """
    try:
        node_info = BT.instance.get_node_info(node_key)
        if node_info is None:
            raise HTTPException(status_code=404, detail=f'Node {node_key} not found')
        client = cc.rpc.Client(node_info.server_address)
        res = client.relay(body)
    except Exception as e:
        logger.error(f'Failed to relay message: {str(e)}')
        raise HTTPException(status_code=500, detail=f'Failed to relay message: {str(e)}')
    return Response(res, media_type='application/octet-stream')

