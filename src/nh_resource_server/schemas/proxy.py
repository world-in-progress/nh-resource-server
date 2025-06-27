from pydantic import BaseModel

class DiscoverBody(BaseModel):
    node_key: str

class DiscoverResponse(BaseModel):
    success: bool
    message: str
    address: str

class RelayBody(BaseModel):
    method: str
    params: dict

class RelayResponse(BaseModel):
    success: bool
    message: str