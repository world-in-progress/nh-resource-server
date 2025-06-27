import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

from ....core.config import settings
from ....schemas.base import NumberResponse
from ....schemas.schema import ProjectSchema, ResponseWithProjectSchemas

# APIs for multiple project schemas ################################################

router = APIRouter(prefix='/schemas')

@router.get('/', response_model=ResponseWithProjectSchemas)
def get_schemas(startIndex: int = 0, endIndex: int = None):
    """
    Description
    --
    Get project schemas within the specified range (startIndex inclusive, endIndex exclusive).  
    If endIndex is not provided, returns all schemas starting from startIndex.  
    
    Order
    --
    The order of schemas is based on the starred status and then alphabetically by name.
    """
    try:
        schema_files = list(Path(settings.GRID_SCHEMA_DIR).glob('*.json'))
        
        if startIndex < 0:
            startIndex = 0
        if endIndex is None:
            endIndex = startIndex + 1 if startIndex + 1 < len(schema_files) else startIndex
            
        schema_files = schema_files[startIndex:endIndex]
            
        schemas = []
        for file in schema_files:
            with open(file, 'r') as f:
                data = json.load(f)
                schemas.append(ProjectSchema(**data))
        
        # Sort schemas: first by starred (True first), then alphabetically by name within each group
        schemas.sort(key=lambda schema: (not schema.starred, schema.name.lower()))
        return ResponseWithProjectSchemas(
            project_schemas=schemas
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to retrieve schemas: {str(e)}')

@router.get('/num', response_model=NumberResponse)
def get_schema_num():
    """
    Description
    --
    Get the number of project schemas.
    """
    
    schema_files = list(Path(settings.GRID_SCHEMA_DIR).glob('*.json'))
    num = len(schema_files)
    
    return NumberResponse(
        number=num
    )
