from fastapi import APIRouter
from . import topo
from . import schema
from . import project
from . import patch
from . import topo
from . import feature
from . import scene
from . import proxy
from . import hello

router = APIRouter(prefix='/api', tags=['api'])

router.include_router(schema.router)
router.include_router(project.router)
router.include_router(patch.router)
router.include_router(topo.router)
router.include_router(feature.router)
router.include_router(scene.router)
router.include_router(proxy.router)
router.include_router(hello.router)