import logging
import uvicorn
from src.nh_resource_server.core.config import settings

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    
    import os
    import sys
    if sys.platform.startswith('win') or sys.platform.startswith('linux'):
        venv_path = sys.prefix
        os.environ['PROJ_LIB'] = os.path.join(venv_path, 'Lib', 'site-packages', 'osgeo', 'data', 'proj')
    
    uvicorn.run("src.nh_resource_server.main:app", host=settings.SERVER_HOST, port=settings.SERVER_PORT, reload=True)
    