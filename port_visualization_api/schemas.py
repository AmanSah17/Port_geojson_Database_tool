from pydantic import BaseModel
from typing import Optional, Any, Dict

class PortBase(BaseModel):
    name: str
    country: str
    type: str
    lat: float
    lon: float
    details: Optional[str] = None

class PortCreate(PortBase):
    pass

class Port(PortBase):
    id: int
    geojson: Optional[Dict[str, Any]] = None

    class Config:
        orm_mode = True

class BoundaryBase(BaseModel):
    name: str
    geojson_data: Dict[str, Any]

class BoundaryCreate(BoundaryBase):
    pass

class Boundary(BoundaryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
