import logging
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException

from ...core.bootstrapping_treeger import BT
from icrms.ihello import IHello
from ...schemas.base import BaseResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/hello', tags=['hello'])

@router.get('/', response_model=BaseResponse)
def hello():
    try:
        logger.info('hello1')
        with BT.instance.connect('root.hello', IHello) as hello:
            res = hello.hello()
            logger.info('hello2')
            logger.info(f'res: {res}')
            return BaseResponse(
                success=True,
                message=res
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to get hello: {str(e)}')
