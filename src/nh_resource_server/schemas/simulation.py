from pydantic import BaseModel
from typing import Dict, Optional

class FileData(BaseModel):
    """Schema for file data"""
    filename: str
    content: str  # Base64 encoded for binary files, plain text for text files
    is_binary: bool
    size: int

class ResultResponse(BaseModel):
    """Response schema for simulation results"""
    success: bool
    message: str
    is_ready: bool
    files: Optional[Dict[str, FileData]] = None